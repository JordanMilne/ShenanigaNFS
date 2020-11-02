import datetime as dt
import functools
import math
import stat
import struct
import typing

from shenaniganfs.generated.rfc1813 import *
import shenaniganfs.generated.rfc1831 as rpc
from shenaniganfs.fs import FileType, BaseFS, FSException, FSENTRY
from shenaniganfs.fs_manager import FileSystemManager
from shenaniganfs.rpchelp import want_ctx
from shenaniganfs.server import CallContext


class WccWrapper(WccData):
    def __init__(self, entry: typing.Optional[FSENTRY] = None):
        super().__init__(None, None)
        self._entry: typing.Optional[FSENTRY] = None
        self.set_entry(entry)

    def set_entry(self, entry: FSENTRY):
        self._entry = entry
        self.before = entry_to_wccattr(entry) if entry else None

    @property
    def after(self) -> typing.Optional[FAttr3]:
        if self._entry:
            return entry_to_fattr(self._entry)
        return None

    @after.setter
    def after(self, val):
        # We're required to have a setter, ignore it.
        pass


def fs_error_handler(resp_creator: typing.Callable, num_wccs: int = 1):
    def _wrap(f):
        @functools.wraps(f)
        async def _inner(*args):
            wccs = [WccWrapper() for _ in range(num_wccs)]
            try:
                return await f(*args, *wccs)
            except FSException as e:
                print(e.error_code, e.message, f, args)
                return resp_creator(e.error_code, *wccs)
        return _inner
    return _wrap


class MountV3Service(MOUNT_PROGRAM_3_SERVER):
    def __init__(self, fs_manager):
        self.fs_manager: FileSystemManager = fs_manager

    async def NULL(self) -> None:
        pass

    @want_ctx
    async def MNT(self, call_ctx: CallContext, mount_path: bytes) -> MountRes3:
        try:
            fs = self.fs_manager.mount_fs_by_root(mount_path, call_ctx)
        except KeyError:
            return MountRes3(MountStat3.MNT3ERR_NOENT)
        print(f"Mounted {call_ctx.transport.client_addr!r}: {fs.fsid!r}: {fs.root_dir}")
        return MountRes3(
            MountStat3.MNT3_OK,
            Mountres3OK(
                self.fs_manager.entry_to_fh(fs.root_dir),
                auth_flavors=[rpc.AuthFlavor.AUTH_NONE, rpc.AuthFlavor.AUTH_SYS],
            ),
        )

    async def DUMP(self) -> typing.List[MountList]:
        # State maintenance is only for informational purposes?
        # Let's just not bother then.
        return []

    async def UMNT(self, mount_name: bytes) -> None:
        return

    async def UMNTALL(self) -> None:
        return

    async def EXPORT(self) -> typing.List[ExportList]:
        return [
            ExportList(path, [b"*"])
            for path in self.fs_manager.fs_factories.keys()
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


def entry_to_fattr(entry: FSENTRY) -> FAttr3:
    return FAttr3(
        type=entry.type,
        mode=entry.mode,
        nlink=entry.nlink,
        uid=entry.uid,
        gid=entry.gid,
        size=entry.size,
        used=entry.blocks,
        rdev=SpecData3(*entry.rdev),
        fsid=entry.fs().fsid,
        fileid=entry.fileid,
        atime=date_to_nfs3(entry.atime),
        mtime=date_to_nfs3(entry.mtime),
        ctime=date_to_nfs3(entry.ctime),
    )


def entry_to_wccattr(entry: FSENTRY) -> WccAttr:
    return WccAttr(
        size=entry.size,
        mtime=date_to_nfs3(entry.mtime),
        ctime=date_to_nfs3(entry.ctime),
    )


def date_to_nfs3(date: dt.datetime) -> NFSTime3:
    ts = date.timestamp()
    frac, whole = math.modf(ts)
    return NFSTime3(math.floor(whole), math.floor(frac * 1e9))


def nfs3_to_date(date: NFSTime3) -> dt.datetime:
    return dt.datetime.fromtimestamp(date.seconds + (date.nseconds / 1e9), tz=dt.timezone.utc)


class NFSV3Service(NFS_PROGRAM_3_SERVER):
    def __init__(self, fs_manager):
        super().__init__()
        self.fs_manager: FileSystemManager = fs_manager

    def _get_named_child(self, dir_fh: bytes, name: bytes, dir_wcc: typing.Optional[WccWrapper] = None) \
            -> typing.Tuple[FSENTRY, typing.Optional[FSENTRY]]:
        dir_entry = self.fs_manager.get_entry_by_fh(dir_fh)
        if not dir_entry:
            raise FSException(NFSStat3.NFS3ERR_STALE)
        if dir_wcc is not None:
            dir_wcc.set_entry(dir_entry)
        if dir_entry.type != FileType.DIR:
            raise FSException(NFSStat3.NFS3ERR_NOTDIR)
        fs: BaseFS = dir_entry.fs()
        return dir_entry, fs.lookup(dir_entry, name)

    async def NULL(self) -> None:
        pass

    async def GETATTR(self, arg_0: GETATTR3Args) -> GETATTR3Res:
        fs_entry = self.fs_manager.get_entry_by_fh(arg_0.obj_handle)
        if not fs_entry:
            return GETATTR3Res(NFSStat3.NFS3ERR_STALE)
        return GETATTR3Res(
            NFSStat3.NFS3_OK,
            resok=GETATTR3ResOK(entry_to_fattr(fs_entry)),
        )

    @fs_error_handler(lambda code, obj_wcc: SETATTR3Res(code, resfail=SETATTR3ResFail(obj_wcc)))
    async def SETATTR(self, arg_0: SETATTR3Args, obj_wcc: WccWrapper) -> SETATTR3Res:
        entry = self.fs_manager.get_entry_by_fh(arg_0.obj_handle)
        if not entry:
            raise FSException(NFSStat3.NFS3ERR_STALE)
        obj_wcc.set_entry(entry)
        if arg_0.guard.check:
            if entry.ctime != nfs3_to_date(arg_0.guard.obj_ctime):
                raise FSException(NFSStat3.NFS3ERR_NOT_SYNC, "guard ctime mismatch")
        fs: BaseFS = entry.fs()
        fs.setattrs(entry, sattr_to_dict(arg_0.new_attributes))
        return SETATTR3Res(
            NFSStat3.NFS3_OK,
            resok=SETATTR3ResOK(obj_wcc)
        )

    @fs_error_handler(lambda code, dir_wcc: LOOKUP3Res(code, resfail=LOOKUP3ResFail(dir_wcc.after)))
    async def LOOKUP(self, arg_0: LOOKUP3Args, dir_wcc: WccWrapper) -> LOOKUP3Res:
        directory, child = self._get_named_child(arg_0.what.dir_handle, arg_0.what.name, dir_wcc)
        if not child:
            raise FSException(NFSStat3.NFS3ERR_NOENT)

        return LOOKUP3Res(
            NFSStat3.NFS3_OK,
            resok=LOOKUP3ResOK(
                obj_handle=self.fs_manager.entry_to_fh(child),
                obj_attributes=entry_to_fattr(child),
                dir_attributes=entry_to_fattr(directory),
            )
        )

    @fs_error_handler(lambda code, obj_wcc: ACCESS3Res(code, resfail=ACCESS3ResFail(obj_wcc.after)))
    async def ACCESS(self, arg_0: ACCESS3Args, obj_wcc: WccWrapper) -> ACCESS3Res:
        entry = self.fs_manager.get_entry_by_fh(arg_0.obj_handle)
        if not entry:
            raise FSException(NFSStat3.NFS3ERR_STALE)
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
    async def READLINK(self, arg_0: READLINK3Args, obj_wcc: WccWrapper) -> READLINK3Res:
        fs_entry = self.fs_manager.get_entry_by_fh(arg_0.file_handle)
        if not fs_entry:
            raise FSException(NFSStat3.NFS3ERR_STALE)
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
    async def READ(self, arg_0: READ3Args, obj_wcc: WccWrapper) -> READ3Res:
        fs_entry = self.fs_manager.get_entry_by_fh(arg_0.file_handle)
        if not fs_entry:
            raise FSException(NFSStat3.NFS3ERR_STALE)
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
    async def WRITE(self, arg_0: WRITE3Args, obj_wcc: WccWrapper) -> WRITE3Res:
        entry = self.fs_manager.get_entry_by_fh(arg_0.file_handle)
        if not entry:
            raise FSException(NFSStat3.NFS3ERR_STALE)
        obj_wcc.set_entry(entry)
        if entry.type != FileType.REG:
            raise FSException(NFSStat3.NFS3ERR_INVAL)
        if arg_0.count > len(arg_0.data):
            # having the separate `count` var doesn't make much sense to me
            # but I guess we have to respect it.
            raise FSException(NFSStat3.NFS3ERR_IO, "Tried to write more data than provided!")
        fs: BaseFS = entry.fs()
        written = fs.write(entry, arg_0.offset, arg_0.data[:arg_0.count])
        return WRITE3Res(
            NFSStat3.NFS3_OK,
            resok=WRITE3ResOK(
                file_wcc=obj_wcc,
                count=written,
                committed=StableHow.FILE_SYNC,
                verf=b"\x00" * NFS3_WRITEVERFSIZE,
            )
        )

    @fs_error_handler(lambda code, dir_wcc: CREATE3Res(code, resfail=CREATE3ResFail(dir_wcc)))
    async def CREATE(self, arg_0: CREATE3Args, dir_wcc: WccWrapper) -> CREATE3Res:
        target_dir, target = self._get_named_child(arg_0.where.dir_handle, arg_0.where.name, dir_wcc)
        # We have no intention of supporting exclusive mode for the moment
        # due to the additional bookkeeping required
        if arg_0.how.mode == Createmode3.EXCLUSIVE:
            raise FSException(NFSStat3.NFS3ERR_NOTSUPP)
        fs: BaseFS = target_dir.fs()
        # Only allowed to clobber files / symlinks, and only in UNCHECKED mode
        if target:
            if arg_0.how.mode != Createmode3.UNCHECKED:
                raise FSException(NFSStat3.NFS3ERR_EXIST)
            if target.type not in (FileType.REG, FileType.LNK):
                raise FSException(NFSStat3.NFS3ERR_INVAL)
            # NB: Atomicity issues if this is made threaded!
            fs.rm(target)

        entry = fs.create_file(target_dir, arg_0.where.name, sattr_to_dict(arg_0.how.obj_attributes))
        return CREATE3Res(
            NFSStat3.NFS3_OK,
            resok=CREATE3ResOK(
                obj_handle=self.fs_manager.entry_to_fh(entry),
                obj_attributes=entry_to_fattr(entry),
                dir_wcc=dir_wcc,
            )
        )

    @fs_error_handler(lambda code, dir_wcc: MKDIR3Res(code, resfail=MKDIR3ResFail(dir_wcc)))
    async def MKDIR(self, arg_0: MKDIR3Args, dir_wcc: WccWrapper) -> MKDIR3Res:
        target_dir, target = self._get_named_child(arg_0.where.dir_handle, arg_0.where.name, dir_wcc)
        if target:
            raise FSException(NFSStat3.NFS3ERR_EXIST)
        fs: BaseFS = target_dir.fs()
        entry = fs.mkdir(target_dir, arg_0.where.name, sattr_to_dict(arg_0.attributes))
        return MKDIR3Res(
            NFSStat3.NFS3_OK,
            resok=MKDIR3ResOK(
                obj_handle=self.fs_manager.entry_to_fh(entry),
                obj_attributes=entry_to_fattr(entry),
                dir_wcc=dir_wcc,
            )
        )

    @fs_error_handler(lambda code, dir_wcc: SYMLINK3Res(code, resfail=CREATE3ResFail(dir_wcc)))
    async def SYMLINK(self, arg_0: SYMLINK3Args, dir_wcc: WccWrapper) -> SYMLINK3Res:
        target_dir, target = self._get_named_child(arg_0.where.dir_handle, arg_0.where.name, dir_wcc)
        if target:
            raise FSException(NFSStat3.NFS3ERR_EXIST)
        fs: BaseFS = target_dir.fs()
        attrs = arg_0.symlink.symlink_attributes
        data = arg_0.symlink.symlink_data
        entry = fs.symlink(target_dir, arg_0.where.name, sattr_to_dict(attrs), data)
        return SYMLINK3Res(
            NFSStat3.NFS3_OK,
            resok=SYMLINK3ResOK(
                obj_handle=self.fs_manager.entry_to_fh(entry),
                obj_attributes=entry_to_fattr(entry),
                dir_wcc=dir_wcc,
            )
        )

    async def MKNOD(self, arg_0: MKNOD3Args) -> MKNOD3Res:
        return MKNOD3Res(NFSStat3.NFS3ERR_NOTSUPP, resfail=MKNOD3ResFail(WccData()))

    @fs_error_handler(lambda code, dir_wcc: REMOVE3Res(code, resfail=REMOVE3ResFail(dir_wcc)))
    async def REMOVE(self, arg_0: REMOVE3Args, dir_wcc: WccWrapper) -> REMOVE3Res:
        dir_entry, to_delete = self._get_named_child(arg_0.object.dir_handle, arg_0.object.name, dir_wcc)
        if not to_delete:
            raise FSException(NFSStat3.NFS3ERR_NOENT)
        if to_delete.type == FileType.DIR:
            raise FSException(NFSStat3.NFS3ERR_ISDIR)
        fs: BaseFS = to_delete.fs()
        fs.rm(to_delete)
        return REMOVE3Res(
            NFSStat3.NFS3_OK,
            resok=REMOVE3ResOK(dir_wcc)
        )

    @fs_error_handler(lambda code, dir_wcc: RMDIR3Res(code, resfail=RMDIR3ResFail(dir_wcc)))
    async def RMDIR(self, arg_0: RMDIR3Args, dir_wcc: WccWrapper) -> RMDIR3Res:
        dir_entry, to_delete = self._get_named_child(arg_0.object.dir_handle, arg_0.object.name, dir_wcc)
        if not to_delete:
            raise FSException(NFSStat3.NFS3ERR_NOENT)
        if to_delete.type != FileType.DIR:
            raise FSException(NFSStat3.NFS3ERR_NOTDIR)
        fs: BaseFS = to_delete.fs()
        fs.rmdir(to_delete)
        return RMDIR3Res(
            NFSStat3.NFS3_OK,
            resok=RMDIR3ResOK(dir_wcc)
        )

    @fs_error_handler(lambda code, from_wcc, to_wcc: RENAME3Res(code, resfail=RENAME3ResFail(from_wcc, to_wcc)), 2)
    async def RENAME(self, arg_0: RENAME3Args, from_wcc: WccWrapper, to_wcc: WccWrapper) -> RENAME3Res:
        source_dir, source = self._get_named_child(arg_0.from_.dir_handle, arg_0.from_.name, from_wcc)
        if not source:
            raise FSException(NFSStat3.NFS3ERR_NOENT)
        dest_dir, dest_entry = self._get_named_child(arg_0.to.dir_handle, arg_0.to.name, to_wcc)
        # FS gets to decide whether or not clobbering is allowed
        fs: BaseFS = dest_dir.fs()
        fs.rename(source, dest_dir, arg_0.to.name)
        return RENAME3Res(
            NFSStat3.NFS3_OK,
            resok=RENAME3ResOK(from_wcc, to_wcc),
        )

    async def LINK(self, arg_0: LINK3Args) -> LINK3Res:
        return LINK3Res(NFSStat3.NFS3ERR_NOTSUPP, resfail=LINK3ResFail(None, WccData()))

    def _readdir_common(self, dir_handle: bytes, cookie: int, cookie_verf: bytes,
                        dir_wcc: WccWrapper) -> typing.Tuple[bool, typing.Sequence[FSENTRY], bytes]:
        directory = self.fs_manager.get_entry_by_fh(dir_handle)
        dir_wcc.set_entry(directory)
        # We ignore the limits specified in the request for now since
        # size calculations are annoying. This should be under the limits for most
        # reasonable clients
        count = 4
        if not directory:
            raise FSException(NFSStat3.NFS3ERR_STALE)

        fs: BaseFS = directory.fs()
        children = fs.readdir(directory)

        # Dir mtime will invalidate whenever a child is added or removed, or
        # when a child name changes, so RFC recommends this for cookie verf.
        expected_verf = struct.pack("!Q", int(directory.mtime.timestamp()))
        if expected_verf != cookie_verf and cookie:
            raise FSException(NFSStat3.NFS3ERR_BAD_COOKIE)

        child_ids = [e.fileid for e in children]
        cookie_idx = 0
        if cookie:
            cookie_idx = child_ids.index(cookie)
            if cookie_idx == -1:
                raise FSException(NFSStat3.NFS3ERR_BAD_COOKIE)
            cookie_idx += 1

        children_slice = children[cookie_idx:cookie_idx + count]
        eof = len(children_slice) != count or (children_slice and children_slice[-1].fileid == child_ids[-1])
        return eof, children_slice, expected_verf

    @fs_error_handler(lambda code, dir_wcc: READDIR3Res(code, resfail=READDIR3ResFail(dir_wcc.after)))
    async def READDIR(self, arg_0: READDIR3Args, dir_wcc: WccWrapper) -> READDIR3Res:
        eof, children, verf = self._readdir_common(arg_0.dir_handle, arg_0.cookie, arg_0.cookieverf, dir_wcc)
        return READDIR3Res(
            NFSStat3.NFS3_OK,
            resok=READDIR3ResOK(
                dir_attributes=dir_wcc.after,
                cookieverf=verf,
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
    async def READDIRPLUS(self, arg_0: READDIRPLUS3Args, dir_wcc: WccWrapper) -> READDIRPLUS3Res:
        eof, children, verf = self._readdir_common(arg_0.dir_handle, arg_0.cookie, arg_0.cookieverf, dir_wcc)
        return READDIRPLUS3Res(
            NFSStat3.NFS3_OK,
            resok=READDIRPLUS3ResOK(
                dir_attributes=dir_wcc.after,
                cookieverf=verf,
                reply=Dirlistplus3(
                    entries=[Entryplus3(
                        fileid=child.fileid,
                        name=child.name,
                        cookie=child.fileid,
                        name_attributes=entry_to_fattr(child),
                        name_handle=self.fs_manager.entry_to_fh(child)
                    ) for child in children],
                    eof=eof,
                )
            )
        )

    @fs_error_handler(lambda code, obj_wcc: FSSTAT3Res(code, resfail=FSSTAT3ResFail(obj_wcc.after)))
    async def FSSTAT(self, arg_0: FSSTAT3Args, obj_wcc: WccWrapper) -> FSSTAT3Res:
        entry = self.fs_manager.get_entry_by_fh(arg_0.fsroot_handle)
        if not entry:
            raise FSException(NFSStat3.NFS3ERR_STALE)
        obj_wcc.set_entry(entry)
        return FSSTAT3Res(
            NFSStat3.NFS3_OK,
            resok=FSSTAT3ResOK(
                obj_attributes=obj_wcc.after,
                tbytes=10000,
                fbytes=4000,
                abytes=4000,
                tfiles=200,
                ffiles=100,
                afiles=100,
                invarsec=0,
            )
        )

    @fs_error_handler(lambda code, obj_wcc: FSINFO3Res(code, resfail=FSINFO3ResFail(obj_wcc.after)))
    async def FSINFO(self, arg_0: FSINFO3Args, obj_wcc: WccWrapper) -> FSINFO3Res:
        entry = self.fs_manager.get_entry_by_fh(arg_0.fsroot_handle)
        if not entry:
            raise FSException(NFSStat3.NFS3ERR_STALE)
        obj_wcc.set_entry(entry)
        if entry.parent_id is not None:
            raise FSException(NFSStat3.NFS3ERR_BADHANDLE)
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
                maxfilesize=0xFFffFFff,
                time_delta=NFSTime3(0, 1),
                properties=FSF3_CANSETTIME | FSF3_LINK | FSF3_SYMLINK | FSF3_HOMOGENEOUS
            )
        )

    @fs_error_handler(lambda code, obj_wcc: PATHCONF3Res(code, resfail=PATHCONF3ResFail(obj_wcc.after)))
    async def PATHCONF(self, arg_0: PATHCONF3Args, obj_wcc: WccWrapper) -> PATHCONF3Res:
        entry = self.fs_manager.get_entry_by_fh(arg_0.obj_handle)
        if not entry:
            raise FSException(NFSStat3.NFS3ERR_STALE)
        obj_wcc.set_entry(entry)
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
    async def COMMIT(self, arg_0: COMMIT3Args, obj_wcc: WccWrapper) -> COMMIT3Res:
        entry = self.fs_manager.get_entry_by_fh(arg_0.file_handle)
        if not entry:
            raise FSException(NFSStat3.NFS3ERR_STALE)
        obj_wcc.set_entry(entry)
        return COMMIT3Res(
            NFSStat3.NFS3_OK,
            resok=COMMIT3ResOK(
                file_wcc=obj_wcc,
                verf=b"\x00" * NFS3_WRITEVERFSIZE,
            )
        )
