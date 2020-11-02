import datetime as dt
import errno
import functools
import math
import stat
import struct
import typing

from shenaniganfs.generated.rfc1094 import *

from shenaniganfs.fs import FileType, BaseFS, FSException, FSENTRY
from shenaniganfs.fs_manager import FileSystemManager
from shenaniganfs.rpchelp import want_ctx


def sattr_to_dict(attrs: SAttr):
    attrs_dict = {}
    for attr_name in ("mode", "uid", "gid", "size"):
        val = getattr(attrs, attr_name)
        if val != 0xFFffFFff:
            if attr_name == "mode":
                # Technically throws away the type which is problematic
                # if you want to support NFS2's overloaded mknod semantics
                # for CREATE().
                val = stat.S_IMODE(val)
            attrs_dict[attr_name] = val
    for attr_name in ("atime", "mtime"):
        val: Timeval = getattr(attrs, attr_name)
        attrs_dict[attr_name] = nfs2_to_date(val) if val.seconds != 0xFFffFFff else None
    return attrs_dict


def date_to_nfs2(date: dt.datetime) -> Timeval:
    ts = date.timestamp()
    frac, whole = math.modf(ts)
    return Timeval(math.floor(whole), math.floor(frac * 1e6))


def nfs2_to_date(date: Timeval) -> dt.datetime:
    return dt.datetime.fromtimestamp(date.seconds + (date.useconds / 1e6), tz=dt.timezone.utc)


def get_nfs2_cookie(entry: FSENTRY):
    return struct.pack("!L", entry.fileid)


# https://tools.ietf.org/html/rfc1094#section-2.3.5
# NFSv2 specific protocol weirdness
_NFS2_MODE_MAPPING = {
    FileType.CHR: stat.S_IFCHR,
    FileType.DIR: stat.S_IFDIR,
    FileType.BLK: stat.S_IFBLK,
    FileType.REG: stat.S_IFREG,
    FileType.LNK: stat.S_IFLNK,
    FileType.SOCK: stat.S_IFSOCK,
    FileType.FIFO: stat.S_IFIFO,
}


def entry_to_fattr(entry: FSENTRY) -> FAttr:
    if entry.type in (FileType.SOCK, FileType.FIFO):
        f_type = Ftype.NFNON
    else:
        f_type = Ftype(entry.type)
    mode = entry.mode | _NFS2_MODE_MAPPING[entry.type]

    return FAttr(
        type=f_type,
        mode=mode,
        nlink=entry.nlink,
        uid=entry.uid,
        gid=entry.gid,
        size=entry.size,
        blocksize=entry.fs().block_size,
        rdev=entry.rdev[0],
        blocks=entry.blocks,
        fsid=entry.fs().fsid & 0xFFffFFff,
        fileid=entry.fileid,
        atime=date_to_nfs2(entry.atime),
        mtime=date_to_nfs2(entry.mtime),
        ctime=date_to_nfs2(entry.ctime),
    )


class MountV1Service(MOUNTPROG_1_SERVER):
    def __init__(self, fs_manager):
        self.fs_manager: FileSystemManager = fs_manager

    async def NULL(self) -> None:
        pass

    @want_ctx
    async def MNT(self, call_ctx, mount_path: bytes) -> FHStatus:
        fs_mgr = self.fs_manager
        try:
            fs: BaseFS = fs_mgr.mount_fs_by_root(mount_path, call_ctx)
        except (KeyError, ValueError):
            return FHStatus(errno=errno.ENOENT)
        print(f"Mounted {fs.owner_addr!r}: {fs.fsid!r}, {mount_path}")
        return FHStatus(errno=0, directory=fs_mgr.entry_to_fh(fs.root_dir, nfs_v2=True))

    async def DUMP(self) -> typing.List[MountList]:
        # State maintenance is only for informational purposes?
        # Let's just not bother then.
        return []

    async def UMNT(self, arg_0: bytes) -> None:
        return

    async def UMNTALL(self) -> None:
        return

    async def EXPORT(self) -> typing.List[ExportList]:
        return [
            ExportList(path, [b"*"])
            for path in self.fs_manager.fs_factories.keys()
        ]


def fs_error_handler(resp_creator: typing.Callable):
    def _wrap(f):
        @functools.wraps(f)
        async def _inner(*args, **kwargs):
            try:
                return await f(*args, **kwargs)
            except FSException as e:
                return resp_creator(e.error_code)
        return _inner
    return _wrap


class NFSV2Service(NFS_PROGRAM_2_SERVER):
    def __init__(self, fs_manager):
        super().__init__()
        self.fs_manager: FileSystemManager = fs_manager

    def _get_child_by_name(self, dir_fh: bytes, name: bytes, do_lookup: bool = False) \
            -> typing.Tuple[FSENTRY, typing.Optional[FSENTRY]]:
        dir_entry = self.fs_manager.get_entry_by_fh(dir_fh, nfs_v2=True)
        if not dir_entry:
            raise FSException(Stat.NFSERR_STALE)
        if dir_entry.type != FileType.DIR:
            raise FSException(Stat.NFSERR_NOTDIR)
        fs: BaseFS = dir_entry.fs()

        # Do we want a side-effectful lookup?
        if do_lookup:
            entry = fs.lookup(dir_entry, name)
        else:
            entry = fs.get_child_by_name(dir_entry, name)
        return dir_entry, entry

    async def NULL(self) -> None:
        pass

    @fs_error_handler(AttrStat)
    async def GETATTR(self, fh: bytes) -> AttrStat:
        fs_entry = self.fs_manager.get_entry_by_fh(fh, nfs_v2=True)
        if not fs_entry:
            return AttrStat(Stat.NFSERR_STALE)
        return AttrStat(Stat.NFS_OK, entry_to_fattr(fs_entry))

    @fs_error_handler(AttrStat)
    async def SETATTR(self, arg_0: SattrArgs) -> AttrStat:
        entry = self.fs_manager.get_entry_by_fh(arg_0.file, nfs_v2=True)
        if not entry:
            return AttrStat(Stat.NFSERR_STALE)
        fs: BaseFS = entry.fs()
        fs.setattrs(entry, sattr_to_dict(arg_0.attributes))
        return AttrStat(Stat.NFS_OK, entry_to_fattr(entry))

    async def ROOT(self) -> None:
        pass

    @fs_error_handler(DiropRes)
    async def LOOKUP(self, arg_0: DiropArgs) -> DiropRes:
        directory, child = self._get_child_by_name(arg_0.dir, arg_0.name, do_lookup=True)
        if not child:
            return DiropRes(Stat.NFSERR_NOENT)

        fs_mgr = self.fs_manager
        return DiropRes(
            Stat.NFS_OK,
            DiropOK(fs_mgr.entry_to_fh(child, nfs_v2=True), entry_to_fattr(child))
        )

    @fs_error_handler(ReadlinkRes)
    async def READLINK(self, fh: bytes) -> ReadlinkRes:
        fs_entry = self.fs_manager.get_entry_by_fh(fh, nfs_v2=True)
        if not fs_entry:
            return ReadlinkRes(Stat.NFSERR_STALE)
        if fs_entry.type != FileType.LNK:
            # TODO: Better error for this?
            return ReadlinkRes(Stat.NFSERR_NOENT)
        fs: BaseFS = fs_entry.fs()
        return ReadlinkRes(Stat.NFS_OK, fs.readlink(fs_entry))

    @fs_error_handler(ReadRes)
    async def READ(self, read_args: ReadArgs) -> ReadRes:
        fs_entry = self.fs_manager.get_entry_by_fh(read_args.file, nfs_v2=True)
        if not fs_entry:
            return ReadRes(Stat.NFSERR_STALE)
        fs: BaseFS = fs_entry.fs()
        return ReadRes(Stat.NFS_OK, AttrDat(
            attributes=entry_to_fattr(fs_entry),
            data=fs.read(fs_entry, read_args.offset, min(read_args.count, 4096))
        ))

    async def WRITECACHE(self) -> None:
        pass

    @fs_error_handler(AttrStat)
    async def WRITE(self, write_args: WriteArgs) -> AttrStat:
        entry = self.fs_manager.get_entry_by_fh(write_args.file, nfs_v2=True)
        if not entry or entry.type != FileType.REG:
            return AttrStat(Stat.NFSERR_IO)
        fs: BaseFS = entry.fs()
        fs.write(entry, write_args.offset, write_args.data)
        return AttrStat(Stat.NFS_OK, entry_to_fattr(entry))

    def _create_common(self, arg_0: CreateArgs, create_func: typing.Callable) -> DiropRes:
        target_dir, target = self._get_child_by_name(arg_0.where.dir, arg_0.where.name)
        if target:
            return DiropRes(Stat.NFSERR_EXIST)
        fs: BaseFS = target_dir.fs()
        new = create_func(fs)(target_dir, arg_0.where.name, sattr_to_dict(arg_0.attributes))
        return DiropRes(Stat.NFS_OK, DiropOK(
            file=self.fs_manager.entry_to_fh(new, nfs_v2=True),
            attributes=entry_to_fattr(new),
        ))

    @fs_error_handler(DiropRes)
    async def CREATE(self, arg_0: CreateArgs) -> DiropRes:
        return self._create_common(arg_0, lambda fs: fs.create_file)

    @fs_error_handler(DiropRes)
    async def MKDIR(self, arg_0: CreateArgs) -> DiropRes:
        return self._create_common(arg_0, lambda fs: fs.mkdir)

    @fs_error_handler(Stat)
    async def REMOVE(self, arg_0: DiropArgs) -> Stat:
        dir_entry, to_delete = self._get_child_by_name(arg_0.dir, arg_0.name)
        if not to_delete:
            return Stat.NFSERR_NOENT
        if to_delete.type == FileType.DIR:
            return Stat.NFSERR_ISDIR
        fs: BaseFS = to_delete.fs()
        fs.rm(to_delete)
        return Stat.NFS_OK

    @fs_error_handler(Stat)
    async def RENAME(self, arg_0: RenameArgs) -> Stat:
        source_dir, source = self._get_child_by_name(arg_0.from_.dir, arg_0.from_.name)
        if not source:
            return Stat.NFSERR_NOENT
        dest_dir, dest_entry = self._get_child_by_name(arg_0.to.dir, arg_0.to.name)
        # FS gets to decide whether or not clobbering is allowed
        fs: BaseFS = dest_dir.fs()
        fs.rename(source, dest_dir, arg_0.to.name)
        return Stat.NFS_OK

    async def LINK(self, arg_0: LinkArgs) -> Stat:
        return Stat.NFSERR_PERM

    async def SYMLINK(self, arg_0: SymlinkArgs) -> Stat:
        return Stat.NFSERR_PERM

    @fs_error_handler(Stat)
    async def RMDIR(self, arg_0: DiropArgs) -> Stat:
        dir_entry, to_delete = self._get_child_by_name(arg_0.dir, arg_0.name)
        if not to_delete:
            return Stat.NFSERR_NOENT
        if to_delete.type != FileType.DIR:
            return Stat.NFSERR_NOTDIR
        fs: BaseFS = to_delete.fs()
        fs.rmdir(to_delete)
        return Stat.NFS_OK

    @fs_error_handler(ReaddirRes)
    async def READDIR(self, arg_0: ReaddirArgs) -> ReaddirRes:
        directory = self.fs_manager.get_entry_by_fh(arg_0.dir, nfs_v2=True)
        count = min(arg_0.count, 50)
        if not directory:
            return ReaddirRes(Stat.NFSERR_STALE)

        cookie_idx = 0
        null_cookie = not sum(arg_0.cookie)
        fs: BaseFS = directory.fs()
        children = fs.readdir(directory)
        if not null_cookie:
            cookie_idx = [get_nfs2_cookie(e) for e in children].index(arg_0.cookie)
            if cookie_idx == -1:
                return ReaddirRes(Stat.NFSERR_NOENT)
            cookie_idx += 1

        children_slice = children[cookie_idx:cookie_idx + count]
        eof = len(children_slice) != count
        return ReaddirRes(
            Stat.NFS_OK,
            ReaddirOK(
                entries=[DirEntry(
                    fileid=file.fileid,
                    name=file.name,
                    cookie=get_nfs2_cookie(file),
                ) for file in children_slice],
                eof=eof,
            )
        )

    @fs_error_handler(StatfsRes)
    async def STATFS(self, fh: bytes) -> StatfsRes:
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
