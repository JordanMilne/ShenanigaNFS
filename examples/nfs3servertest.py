import asyncio
import functools
import stat
import typing

from pynefs.generated.rfc1813 import *
import pynefs.generated.rfc1831 as rpc
from pynefs.server import TCPTransportServer
from pynefs.fs import FileSystemManager, FileType, VerifyingFileHandleEncoder, \
    BaseFS, nfs3_to_date, FSError, FSENTRY
from pynefs.nullfs import NullFS


class WccWrapper(WccData):
    def __init__(self, entry: typing.Optional[FSENTRY] = None):
        super().__init__(None, None)
        self._entry: typing.Optional[FSENTRY] = None
        self.set_entry(entry)

    def set_entry(self, entry: FSENTRY):
        self._entry = entry
        self.before = entry.to_nfs3_wccattr() if entry else None

    @property
    def after(self) -> typing.Optional[FAttr3]:
        if self._entry:
            return self._entry.to_nfs3_fattr()
        return None

    @after.setter
    def after(self, val):
        return


def fs_error_handler(resp_creator: typing.Callable, num_wccs: int = 1):
    def _wrap(f):
        @functools.wraps(f)
        def _inner(*args):
            wccs = [WccWrapper() for _ in range(num_wccs)]
            try:
                return f(*args, *wccs)
            except FSError as e:
                print(e)
                return resp_creator(e.error_code, *wccs)
        return _inner
    return _wrap


class MountV3Service(MOUNT_PROGRAM_3_SERVER):
    def __init__(self, fs_manager):
        self.fs_manager: FileSystemManager = fs_manager

    def NULL(self) -> None:
        pass

    def MNT(self, mount_path: bytes) -> MountRes3:
        fs_mgr = self.fs_manager
        fs = fs_mgr.get_fs_by_root(mount_path)
        if fs is None:
            return MountRes3(MountStat3.MNT3ERR_NOENT)
        return MountRes3(
            MountStat3.MNT3_OK,
            Mountres3OK(
                fs_mgr.entry_to_fh(fs.root_dir),
                auth_flavors=[rpc.AuthFlavor.AUTH_NONE, rpc.AuthFlavor.AUTH_SYS],
            ),
        )

    def DUMP(self) -> typing.List[MountList]:
        # State maintenance is only for informational purposes?
        # Let's just not bother then.
        return []

    def UMNT(self, arg_0: bytes) -> None:
        return

    def UMNTALL(self) -> None:
        return

    def EXPORT(self) -> typing.List[ExportList]:
        return [
            ExportList(fs.root_path, [b"*"])
            for fs in self.fs_manager.filesystems.values()
        ]


def sattr_to_dict(attrs: SAttr3):
    attrs_dict = {}
    for attr_name in ("mode", "uid", "gid", "size"):
        val = getattr(attrs, attr_name)
        if val is not None:
            if attr_name == "mode":
                val = stat.S_IMODE(val)
            attrs_dict[attr_name] = val
    for attr_name in ("atime", "mtime"):
        val: SetTime = getattr(attrs, attr_name)
        if val.set_it == TimeHow.SET_TO_CLIENT_TIME:
            attrs_dict[attr_name] = nfs3_to_date(val.time_val)
        elif val.set_it == TimeHow.SET_TO_SERVER_TIME:
            attrs_dict[attr_name] = None
    return attrs_dict


class NFSV3Service(NFS_PROGRAM_3_SERVER):
    def __init__(self, fs_manager):
        super().__init__()
        self.fs_manager: FileSystemManager = fs_manager

    def _get_named_child(self, dir_fh: bytes, name: bytes, dir_wcc: typing.Optional[WccWrapper] = None) \
            -> typing.Tuple[FSENTRY, typing.Optional[FSENTRY]]:
        dir_entry = self.fs_manager.get_entry_by_fh(dir_fh)
        if not dir_entry:
            raise FSError(NFSStat3.NFS3ERR_STALE)
        if dir_wcc is not None:
            dir_wcc.set_entry(dir_entry)
        if dir_entry.type != FileType.DIR:
            raise FSError(NFSStat3.NFS3ERR_NOTDIR)
        return dir_entry, dir_entry.get_child_by_name(name)

    def NULL(self) -> None:
        pass

    def GETATTR(self, arg_0: GETATTR3Args) -> GETATTR3Res:
        fs_entry = self.fs_manager.get_entry_by_fh(arg_0.obj_handle)
        if not fs_entry:
            return GETATTR3Res(NFSStat3.NFS3ERR_STALE)
        return GETATTR3Res(
            NFSStat3.NFS3_OK,
            resok=GETATTR3ResOK(fs_entry.to_nfs3_fattr()),
        )

    @fs_error_handler(lambda code, obj_wcc: SETATTR3Res(code, resfail=SETATTR3ResFail(obj_wcc)))
    def SETATTR(self, arg_0: SETATTR3Args, obj_wcc: WccWrapper) -> SETATTR3Res:
        entry = self.fs_manager.get_entry_by_fh(arg_0.obj_handle)
        if not entry:
            raise FSError(NFSStat3.NFS3ERR_STALE)
        obj_wcc.set_entry(entry)
        guard = arg_0.guard
        if guard.check:
            if entry.ctime != nfs3_to_date(guard.obj_ctime):
                raise FSError(NFSStat3.NFS3ERR_NOT_SYNC, "guard ctime mismatch")
        fs: BaseFS = entry.fs()
        fs.setattrs(entry, sattr_to_dict(arg_0.new_attributes))
        return SETATTR3Res(
            NFSStat3.NFS3_OK,
            resok=SETATTR3ResOK(obj_wcc)
        )

    @fs_error_handler(lambda code, dir_wcc: LOOKUP3Res(code, resfail=LOOKUP3ResFail(dir_wcc.after)))
    def LOOKUP(self, arg_0: LOOKUP3Args, dir_wcc: WccWrapper) -> LOOKUP3Res:
        directory, child = self._get_named_child(arg_0.what.dir_handle, arg_0.what.name, dir_wcc)
        if not child:
            raise FSError(NFSStat3.NFS3ERR_NOENT)

        fs_mgr = self.fs_manager
        return LOOKUP3Res(
            NFSStat3.NFS3_OK,
            resok=LOOKUP3ResOK(
                obj_handle=fs_mgr.entry_to_fh(child),
                obj_attributes=child.to_nfs3_fattr(),
                dir_attributes=directory.to_nfs3_fattr(),
            )
        )

    @fs_error_handler(lambda code, obj_wcc: ACCESS3Res(code, resfail=ACCESS3ResFail(obj_wcc.after)))
    def ACCESS(self, arg_0: ACCESS3Args, obj_wcc: WccWrapper) -> ACCESS3Res:
        entry = self.fs_manager.get_entry_by_fh(arg_0.obj_handle)
        if not entry:
            raise FSError(NFSStat3.NFS3ERR_STALE)
        obj_wcc.set_entry(entry)
        return ACCESS3Res(
            NFSStat3.NFS3_OK,
            resok=ACCESS3ResOK(
                obj_attributes=obj_wcc.after,
                # Just lie and say they can do everything for now.
                access=0xFF,
            )
        )

    @fs_error_handler(lambda code, obj_wcc: READLINK3Res(code, resfail=READLINK3ResFail(obj_wcc.after)))
    def READLINK(self, arg_0: READLINK3Args, obj_wcc: WccWrapper) -> READLINK3Res:
        fs_entry = self.fs_manager.get_entry_by_fh(arg_0.file_handle)
        if not fs_entry:
            raise FSError(NFSStat3.NFS3ERR_STALE)
        obj_wcc.set_entry(fs_entry)
        fs: BaseFS = fs_entry.fs()
        data = fs.readlink(fs_entry)
        return READLINK3Res(
            NFSStat3.NFS3_OK,
            resok=READLINK3ResOK(
                symlink_attributes=obj_wcc.after,
                data=data,
            )
        )

    @fs_error_handler(lambda code, obj_wcc: READ3Res(code, resfail=READ3ResFail(obj_wcc.after)))
    def READ(self, arg_0: READ3Args, obj_wcc: WccWrapper) -> READ3Res:
        fs_entry = self.fs_manager.get_entry_by_fh(arg_0.file_handle)
        if not fs_entry:
            raise FSError(NFSStat3.NFS3ERR_STALE)
        obj_wcc.set_entry(fs_entry)
        fs: BaseFS = fs_entry.fs()
        data = fs.read(fs_entry, arg_0.offset, min(arg_0.count, 4096))
        return READ3Res(
            NFSStat3.NFS3_OK,
            resok=READ3ResOK(
                file_attributes=obj_wcc.after,
                count=len(data),
                eof=len(data) + arg_0.offset >= fs_entry.size,
                data=data,
            )
        )

    @fs_error_handler(lambda code, obj_wcc: WRITE3Res(code, resfail=WRITE3ResFail(obj_wcc)))
    def WRITE(self, arg_0: WRITE3Args, obj_wcc: WccWrapper) -> WRITE3Res:
        entry = self.fs_manager.get_entry_by_fh(arg_0.file_handle)
        if not entry:
            raise FSError(NFSStat3.NFS3ERR_STALE)
        obj_wcc.set_entry(entry)
        if entry.type != FileType.REG:
            raise FSError(NFSStat3.NFS3ERR_INVAL)
        fs: BaseFS = entry.fs()
        fs.write(entry, arg_0.offset, arg_0.data)
        return WRITE3Res(
            NFSStat3.NFS3_OK,
            resok=WRITE3ResOK(
                file_wcc=obj_wcc,
                count=arg_0.count,
                committed=StableHow.FILE_SYNC,
                verf=b"\x00" * NFS3_WRITEVERFSIZE,
            )
        )

    @fs_error_handler(lambda code, dir_wcc: CREATE3Res(code, resfail=CREATE3ResFail(dir_wcc)))
    def CREATE(self, arg_0: CREATE3Args, dir_wcc: WccWrapper) -> CREATE3Res:
        target_dir, target = self._get_named_child(arg_0.where.dir_handle, arg_0.where.name, dir_wcc)
        # We have no intention of supporting exclusive mode for the moment
        # due to the additional bookkeeping required
        if arg_0.how.mode == Createmode3.EXCLUSIVE:
            raise FSError(NFSStat3.NFS3ERR_NOTSUPP)
        fs: BaseFS = target_dir.fs()
        # Only allowed to clobber files / symlinks, and only in UNCHECKED mode
        if target:
            if arg_0.how.mode != Createmode3.UNCHECKED:
                raise FSError(NFSStat3.NFS3ERR_EXIST)
            if target.type not in (FileType.REG, FileType.LNK):
                raise FSError(NFSStat3.NFS3ERR_INVAL)
            fs.rm(target)

        entry = fs.create_file(target_dir, arg_0.where.name, sattr_to_dict(arg_0.how.obj_attributes))
        return CREATE3Res(
            NFSStat3.NFS3_OK,
            resok=CREATE3ResOK(
                obj_handle=self.fs_manager.entry_to_fh(entry),
                obj_attributes=entry.to_nfs3_fattr(),
                dir_wcc=dir_wcc,
            )
        )

    @fs_error_handler(lambda code, dir_wcc: MKDIR3Res(code, resfail=MKDIR3ResFail(dir_wcc)))
    def MKDIR(self, arg_0: MKDIR3Args, dir_wcc: WccWrapper) -> MKDIR3Res:
        target_dir, target = self._get_named_child(arg_0.where.dir_handle, arg_0.where.name, dir_wcc)
        # We have no intention of supporting exclusive mode for the moment
        # due to the additional bookkeeping required
        fs: BaseFS = target_dir.fs()
        if target:
            raise FSError(NFSStat3.NFS3ERR_EXIST)
        entry = fs.mkdir(target_dir, arg_0.where.name, sattr_to_dict(arg_0.attributes))
        return MKDIR3Res(
            NFSStat3.NFS3_OK,
            resok=MKDIR3ResOK(
                obj_handle=self.fs_manager.entry_to_fh(entry),
                obj_attributes=entry.to_nfs3_fattr(),
                dir_wcc=dir_wcc,
            )
        )

    def SYMLINK(self, arg_0: SYMLINK3Args) -> SYMLINK3Res:
        pass

    def MKNOD(self, arg_0: MKNOD3Args) -> MKNOD3Res:
        pass

    def REMOVE(self, arg_0: REMOVE3Args) -> REMOVE3Res:
        pass

    def RMDIR(self, arg_0: RMDIR3Args) -> RMDIR3Res:
        pass

    def RENAME(self, arg_0: RENAME3Args) -> RENAME3Res:
        pass

    def LINK(self, arg_0: LINK3Args) -> LINK3Res:
        pass

    def _readdir_common(self, dir_handle: bytes, cookie: int, cookie_verf: bytes,
                        dir_wcc: WccWrapper) -> typing.Tuple[bool, typing.List[FSENTRY]]:
        directory = self.fs_manager.get_entry_by_fh(dir_handle)
        dir_wcc.set_entry(directory)
        # We ignore the limits specified in the request for now since
        # size calculations are annoying. This should be under the limits for most
        # reasonable clients
        count = 50
        if not directory:
            raise FSError(NFSStat3.NFS3ERR_STALE)

        child_ids = [e.fileid for e in directory.children]
        cookie_idx = 0
        if cookie:
            cookie_idx = child_ids.index(cookie)
            if cookie_idx == -1:
                raise FSError(NFSStat3.NFS3ERR_NOENT)
            cookie_idx += 1

        children = directory.children[cookie_idx:cookie_idx + count]
        eof = len(children) != count or (children and children[-1].fileid == child_ids[-1])
        return eof, children

    @fs_error_handler(lambda code, dir_wcc: READDIR3Res(code, resfail=READDIR3ResFail(dir_wcc.after)))
    def READDIR(self, arg_0: READDIR3Args, dir_wcc: WccWrapper) -> READDIR3Res:
        eof, children = self._readdir_common(arg_0.dir_handle, arg_0.cookie, arg_0.cookieverf, dir_wcc)
        return READDIR3Res(
            NFSStat3.NFS3_OK,
            resok=READDIR3ResOK(
                dir_attributes=dir_wcc.after,
                cookieverf=b"\x00" * NFS3_COOKIEVERFSIZE,
                reply=DirList3(
                    entries=[Entry3(
                        fileid=child.fileid,
                        name=child.name,
                        cookie=child.fileid,
                    ) for child in children],
                    eof=eof,
                )
            )
        )

    @fs_error_handler(lambda code, dir_wcc: READDIRPLUS3Res(code, resfail=READDIRPLUS3ResFail(dir_wcc.after)))
    def READDIRPLUS(self, arg_0: READDIRPLUS3Args, dir_wcc: WccWrapper) -> READDIRPLUS3Res:
        eof, children = self._readdir_common(arg_0.dir_handle, arg_0.cookie, arg_0.cookieverf, dir_wcc)
        fs_mgr = self.fs_manager
        return READDIRPLUS3Res(
            NFSStat3.NFS3_OK,
            resok=READDIRPLUS3ResOK(
                dir_attributes=dir_wcc.after,
                cookieverf=b"\x00" * NFS3_COOKIEVERFSIZE,
                reply=Dirlistplus3(
                    entries=[Entryplus3(
                        fileid=child.fileid,
                        name=child.name,
                        cookie=child.fileid,
                        name_attributes=child.to_nfs3_fattr(),
                        name_handle=fs_mgr.entry_to_fh(child)
                    ) for child in children],
                    eof=eof,
                )
            )
        )

    @fs_error_handler(lambda code, obj_wcc: FSSTAT3Res(code, resfail=FSSTAT3ResFail(obj_wcc.after)))
    def FSSTAT(self, arg_0: FSSTAT3Args, obj_wcc: WccWrapper) -> FSSTAT3Res:
        entry = self.fs_manager.get_entry_by_fh(arg_0.fsroot_handle)
        if not entry:
            raise FSError(NFSStat3.NFS3ERR_STALE)
        obj_wcc.set_entry(entry)
        if entry.parent_id is not None:
            raise FSError(NFSStat3.NFS3ERR_BADHANDLE)
        return FSSTAT3Res(
            NFSStat3.NFS3_OK,
            resok=FSSTAT3ResOK(
                obj_attributes=obj_wcc.after,
                tbytes=10000,
                fbytes=4000,
                abytes=4000,
                tfiles=100,
                afiles=100,
                invarsec=0,
            )
        )

    @fs_error_handler(lambda code, obj_wcc: FSINFO3Res(code, resfail=FSINFO3ResFail(obj_wcc.after)))
    def FSINFO(self, arg_0: FSINFO3Args, obj_wcc: WccWrapper) -> FSINFO3Res:
        entry = self.fs_manager.get_entry_by_fh(arg_0.fsroot_handle)
        if not entry:
            raise FSError(NFSStat3.NFS3ERR_STALE)
        obj_wcc.set_entry(entry)
        if entry.parent_id is not None:
            raise FSError(NFSStat3.NFS3ERR_BADHANDLE)
        return FSINFO3Res(
            NFSStat3.NFS3_OK,
            resok=FSINFO3ResOK(
                obj_attributes=obj_wcc.after,
                rtmax=1024,
                rtpref=1024,
                rtmult=8,
                wtmax=1024,
                wtpref=1024,
                wtmult=8,
                dtpref=2000,
                maxfilesize=2**32,
                time_delta=NFSTime3(1, 0),
                properties=FSF3_CANSETTIME | FSF3_LINK | FSF3_SYMLINK | FSF3_HOMOGENEOUS
            )
        )

    @fs_error_handler(lambda code, obj_wcc: PATHCONF3Res(code, resfail=PATHCONF3ResFail(obj_wcc.after)))
    def PATHCONF(self, arg_0: PATHCONF3Args, obj_wcc: WccWrapper) -> PATHCONF3Res:
        entry = self.fs_manager.get_entry_by_fh(arg_0.obj_handle)
        if not entry:
            raise FSError(NFSStat3.NFS3ERR_STALE)

        return PATHCONF3Res(
            NFSStat3.NFS3_OK,
            resok=PATHCONF3ResOK(
                obj_attributes=obj_wcc.after,
                linkmax=200,
                name_max=200,
                no_trunc=True,
                chown_restricted=False,
                case_insensitive=False,
                case_preserving=True,
            )
        )

    @fs_error_handler(lambda code, obj_wcc: COMMIT3Res(code, resfail=COMMIT3ResFail(obj_wcc)))
    def COMMIT(self, arg_0: COMMIT3Args, obj_wcc: WccWrapper) -> COMMIT3Res:
        entry = self.fs_manager.get_entry_by_fh(arg_0.file_handle)
        if not entry:
            raise FSError(NFSStat3.NFS3ERR_STALE)
        obj_wcc.set_entry(entry)
        return COMMIT3Res(
            NFSStat3.NFS3_OK,
            resok=COMMIT3ResOK(
                file_wcc=obj_wcc,
                verf=b"\x00" * NFS3_WRITEVERFSIZE,
            )
        )


async def main():
    fs_manager = FileSystemManager(
        VerifyingFileHandleEncoder(b"foobar"),
        filesystems=[
            NullFS(b"/tmp/nfs2", read_only=False),
        ]
    )

    transport_server = TCPTransportServer("127.0.0.1", 2222)
    transport_server.register_prog(MountV3Service(fs_manager))
    transport_server.register_prog(NFSV3Service(fs_manager))
    await transport_server.notify_rpcbind()

    server = await transport_server.start()

    async with server:
        await server.serve_forever()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
