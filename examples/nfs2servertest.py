import asyncio
import errno
import functools
import stat
import typing

from pynefs.generated.rfc1094 import *
from pynefs.server import TCPTransportServer
from pynefs.fs import FileSystemManager, FileType, VerifyingFileHandleEncoder, \
    BaseFS, nfs2_to_date, FSError, FSENTRY, get_nfs2_cookie
from pynefs.nullfs import NullFS
from pynefs.zipfs import ZipFS


def fs_error_handler(resp_creator: typing.Callable):
    def _wrap(f):
        @functools.wraps(f)
        def _inner(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except FSError as e:
                print(e)
                return resp_creator(e.error_code)
        return _inner
    return _wrap


class MountV1Service(MOUNTPROG_1_SERVER):
    def __init__(self, fs_manager):
        self.fs_manager: FileSystemManager = fs_manager

    def NULL(self) -> None:
        pass

    def MNT(self, mount_path: bytes) -> FHStatus:
        fs_mgr = self.fs_manager
        fs = fs_mgr.get_fs_by_root(mount_path)
        if fs is None:
            return FHStatus(errno=errno.ENOENT)
        return FHStatus(errno=0, directory=fs_mgr.entry_to_fh(fs.root_dir, nfs_v2=True))

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


def sattr_to_dict(attrs: SAttr):
    attrs_dict = {}
    for attr_name in ("mode", "uid", "gid", "size"):
        val = getattr(attrs, attr_name)
        if val != 0xFFffFFff:
            if attr_name == "mode":
                val = stat.S_IMODE(val)
            attrs_dict[attr_name] = val
    for attr_name in ("atime", "mtime"):
        val: Timeval = getattr(attrs, attr_name)
        if val.seconds != 0xFFffFFff:
            attrs_dict[attr_name] = nfs2_to_date(val)
    return attrs_dict


class NFSV2Service(NFS_PROGRAM_2_SERVER):
    def __init__(self, fs_manager):
        super().__init__()
        self.fs_manager: FileSystemManager = fs_manager

    def _get_named_child(self, dir_fh: bytes, name: bytes) -> typing.Tuple[FSENTRY, typing.Optional[FSENTRY]]:
        dir_entry = self.fs_manager.get_entry_by_fh(dir_fh, nfs_v2=True)
        if not dir_entry:
            raise FSError(Stat.NFSERR_STALE)
        if dir_entry.type != FileType.DIR:
            raise FSError(Stat.NFSERR_NOTDIR)
        return dir_entry, dir_entry.get_child_by_name(name)

    def NULL(self) -> None:
        pass

    def GETATTR(self, fh: bytes) -> AttrStat:
        fs_entry = self.fs_manager.get_entry_by_fh(fh, nfs_v2=True)
        if not fs_entry:
            return AttrStat(Stat.NFSERR_STALE)
        return AttrStat(Stat.NFS_OK, fs_entry.to_nfs2_fattr())

    @fs_error_handler(AttrStat)
    def SETATTR(self, arg_0: SattrArgs) -> AttrStat:
        entry = self.fs_manager.get_entry_by_fh(arg_0.file, nfs_v2=True)
        if not entry:
            return AttrStat(Stat.NFSERR_STALE)
        fs: BaseFS = entry.fs()
        fs.setattrs(entry, sattr_to_dict(arg_0.attributes))
        return AttrStat(Stat.NFS_OK, entry.to_nfs2_fattr())

    def ROOT(self) -> None:
        pass

    def LOOKUP(self, arg_0: DiropArgs) -> DiropRes:
        directory, child = self._get_named_child(arg_0.dir, arg_0.name)
        if not child:
            return DiropRes(Stat.NFSERR_NOENT)

        fs_mgr = self.fs_manager
        return DiropRes(
            Stat.NFS_OK,
            DiropOK(fs_mgr.entry_to_fh(child, nfs_v2=True), child.to_nfs2_fattr())
        )

    def READLINK(self, fh: bytes) -> ReadlinkRes:
        fs_entry = self.fs_manager.get_entry_by_fh(fh, nfs_v2=True)
        if not fs_entry:
            return ReadlinkRes(Stat.NFSERR_STALE)
        if fs_entry.type != FileType.LNK:
            # TODO: Better error for this?
            return ReadlinkRes(Stat.NFSERR_NOENT)
        return ReadlinkRes(Stat.NFS_OK, fs_entry.contents)

    @fs_error_handler(ReadRes)
    def READ(self, read_args: ReadArgs) -> ReadRes:
        fs_entry = self.fs_manager.get_entry_by_fh(read_args.file, nfs_v2=True)
        if not fs_entry:
            return ReadRes(Stat.NFSERR_STALE)
        fs: BaseFS = fs_entry.fs()
        return ReadRes(Stat.NFS_OK, AttrDat(
            attributes=fs_entry.to_nfs2_fattr(),
            data=fs.read(fs_entry, read_args.offset, min(read_args.count, 4096))
        ))

    def WRITECACHE(self) -> None:
        pass

    @fs_error_handler(AttrStat)
    def WRITE(self, write_args: WriteArgs) -> AttrStat:
        entry = self.fs_manager.get_entry_by_fh(write_args.file, nfs_v2=True)
        if not entry or entry.type != FileType.REG:
            return AttrStat(Stat.NFSERR_IO)
        fs: BaseFS = entry.fs()
        fs.write(entry, write_args.offset, write_args.data)
        return AttrStat(Stat.NFS_OK, entry.to_nfs2_fattr())

    def _create_common(self, arg_0: CreateArgs, create_func: typing.Callable) -> DiropRes:
        target_dir, target = self._get_named_child(arg_0.where.dir, arg_0.where.name)
        if target:
            return DiropRes(Stat.NFSERR_EXIST)
        fs: BaseFS = target_dir.fs()
        new = create_func(fs)(target_dir, arg_0.where.name, sattr_to_dict(arg_0.attributes))
        return DiropRes(Stat.NFS_OK, DiropOK(
            file=self.fs_manager.entry_to_fh(new, nfs_v2=True),
            attributes=new.to_nfs2_fattr(),
        ))

    @fs_error_handler(DiropRes)
    def CREATE(self, arg_0: CreateArgs) -> DiropRes:
        return self._create_common(arg_0, lambda fs: fs.create_file)

    @fs_error_handler(DiropRes)
    def MKDIR(self, arg_0: CreateArgs) -> DiropRes:
        return self._create_common(arg_0, lambda fs: fs.mkdir)

    @fs_error_handler(Stat)
    def REMOVE(self, arg_0: DiropArgs) -> Stat:
        dir_entry, to_delete = self._get_named_child(arg_0.dir, arg_0.name)
        if not to_delete:
            return Stat.NFSERR_NOENT
        if to_delete.type == FileType.DIR:
            return Stat.NFSERR_ISDIR
        fs: BaseFS = to_delete.fs()
        fs.rm(to_delete)
        return Stat.NFS_OK

    @fs_error_handler(Stat)
    def RENAME(self, arg_0: RenameArgs) -> Stat:
        source_dir, source = self._get_named_child(arg_0.from_.dir, arg_0.from_.name)
        if not source:
            return Stat.NFSERR_NOENT
        if source.type == FileType.DIR:
            return Stat.NFSERR_ISDIR
        dest_dir, dest_entry = self._get_named_child(arg_0.to.dir, arg_0.to.name)
        if dest_entry:
            return Stat.NFSERR_EXIST
        fs: BaseFS = dest_dir.fs()
        fs.rename(source, dest_dir, arg_0.to.name)
        return Stat.NFS_OK

    def LINK(self, arg_0: LinkArgs) -> Stat:
        return Stat.NFSERR_PERM

    def SYMLINK(self, arg_0: SymlinkArgs) -> Stat:
        return Stat.NFSERR_PERM

    @fs_error_handler(Stat)
    def RMDIR(self, arg_0: DiropArgs) -> Stat:
        dir_entry, to_delete = self._get_named_child(arg_0.dir, arg_0.name)
        if not to_delete:
            return Stat.NFSERR_NOENT
        if to_delete.type != FileType.DIR:
            return Stat.NFSERR_NOTDIR
        fs: BaseFS = to_delete.fs()
        fs.rmdir(to_delete)
        return Stat.NFS_OK

    def READDIR(self, arg_0: ReaddirArgs) -> ReaddirRes:
        directory = self.fs_manager.get_entry_by_fh(arg_0.dir, nfs_v2=True)
        count = min(arg_0.count, 50)
        if not directory:
            return ReaddirRes(Stat.NFSERR_STALE)

        cookie_idx = 0
        null_cookie = not sum(arg_0.cookie)
        if not null_cookie:
            cookie_idx = [get_nfs2_cookie(e) for e in directory.children].index(arg_0.cookie)
            if cookie_idx == -1:
                return ReaddirRes(Stat.NFSERR_NOENT)
            cookie_idx += 1

        children = directory.children[cookie_idx:cookie_idx + count]
        eof = len(children) != count
        return ReaddirRes(
            Stat.NFS_OK,
            ReaddirOK(
                entries=[DirEntry(
                    fileid=file.fileid,
                    name=file.name,
                    cookie=get_nfs2_cookie(file),
                ) for file in children],
                eof=eof,
            )
        )

    def STATFS(self, fh: bytes) -> StatfsRes:
        fs = self.fs_manager.get_fs_by_fh(fh, nfs_v2=True)
        if not fs:
            return StatfsRes(Stat.NFSERR_STALE)
        return StatfsRes(
            Stat.NFS_OK,
            FsInfo(
                tsize=4096,
                bsize=fs.block_size,
                blocks=fs.num_blocks,
                bfree=fs.free_blocks,
                bavail=fs.avail_blocks,
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
    transport_server.register_prog(MountV1Service(fs_manager))
    transport_server.register_prog(NFSV2Service(fs_manager))
    await transport_server.notify_rpcbind()

    server = await transport_server.start()

    async with server:
        await server.serve_forever()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
