import asyncio
import errno
import typing

from pynefs.generated.rfc1094 import *
from pynefs.server import TCPTransportServer
from pynefs.fs import FileSystemManager, FileType
from pynefs.nullfs import NullFS


class MountV1Service(MOUNTPROG_1_SERVER):
    def __init__(self, fs_manager):
        self.fs_manager: FileSystemManager = fs_manager

    def NULL(self) -> None:
        pass

    def MNT(self, mount_path: bytes) -> FHStatus:
        fs = self.fs_manager.get_fs_by_root(mount_path)
        if fs is None:
            return FHStatus(
                errno=errno.ENOENT
            )
        return FHStatus(
            errno=0,
            directory=fs.fh,
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
            for fs in self.fs_manager.filesystems
        ]


class NFSV2Service(NFS_PROGRAM_2_SERVER):
    def __init__(self, fs_manager):
        super().__init__()
        self.fs_manager: FileSystemManager = fs_manager

    def NULL(self) -> None:
        pass

    def GETATTR(self, fh: bytes) -> AttrStat:
        fs_entry = self.fs_manager.get_entry_by_fh(fh)
        if not fs_entry:
            return AttrStat(Stat.NFSERR_STALE)
        return AttrStat(Stat.NFS_OK, fs_entry.to_nfs2_fattr())

    def SETATTR(self, arg_0: SattrArgs) -> AttrStat:
        return AttrStat(Stat.NFSERR_ROFS)

    def ROOT(self) -> None:
        pass

    def LOOKUP(self, arg_0: DiropArgs) -> DiropRes:
        directory = self.fs_manager.get_entry_by_fh(arg_0.dir)
        if not directory:
            return DiropRes(Stat.NFSERR_STALE)
        child = directory.get_child_by_name(arg_0.name)
        if not child:
            return DiropRes(Stat.NFSERR_NOENT)
        return DiropRes(
            Stat.NFS_OK,
            DiropOK(child.fh, child.to_nfs2_fattr())
        )

    def READLINK(self, fh: bytes) -> ReadlinkRes:
        fs_entry = self.fs_manager.get_entry_by_fh(fh)
        if not fs_entry:
            return ReadlinkRes(Stat.NFSERR_STALE)
        if fs_entry.type != FileType.LINK:
            # TODO: Better error for this?
            return ReadlinkRes(Stat.NFSERR_NOENT)
        return ReadlinkRes(Stat.NFS_OK, fs_entry.contents)

    def READ(self, read_args: ReadArgs) -> ReadRes:
        fs_entry = self.fs_manager.get_entry_by_fh(read_args.file)
        if not fs_entry:
            return ReadRes(Stat.NFSERR_STALE)
        # No special devices for now!
        if fs_entry.type not in (FileType.LINK, FileType.REG):
            return ReadRes(Stat.NFSERR_IO)
        return ReadRes(Stat.NFS_OK, AttrDat(
            attributes=fs_entry.to_nfs2_fattr(),
            data=fs_entry.contents[read_args.offset:read_args.offset + read_args.count]
        ))

    def WRITECACHE(self) -> None:
        pass

    def WRITE(self, arg_0: CreateArgs) -> AttrStat:
        return AttrStat(Stat.NFSERR_ROFS)

    def CREATE(self, arg_0: CreateArgs) -> DiropRes:
        return DiropRes(Stat.NFSERR_ROFS)

    def REMOVE(self, arg_0: DiropArgs) -> Stat:
        return Stat.NFSERR_ROFS

    def RENAME(self, arg_0: RenameArgs) -> Stat:
        return Stat.NFSERR_ROFS

    def LINK(self, arg_0: LinkArgs) -> Stat:
        return Stat.NFSERR_ROFS

    def SYMLINK(self, arg_0: LinkArgs) -> Stat:
        return Stat.NFSERR_ROFS

    def MKDIR(self, arg_0: CreateArgs) -> DiropRes:
        return DiropRes(Stat.NFSERR_ROFS)

    def RMDIR(self, arg_0: DiropArgs) -> Stat:
        return Stat.NFSERR_ROFS

    def READDIR(self, arg_0: ReaddirArgs) -> ReaddirRes:
        directory = self.fs_manager.get_entry_by_fh(arg_0.dir)
        count = min(arg_0.count, 50)
        if not directory:
            return ReaddirRes(Stat.NFSERR_STALE)

        cookie_idx = 0
        null_cookie = not sum(arg_0.cookie)
        if not null_cookie:
            cookie_idx = [e.nfs2_cookie for e in directory.children].index(arg_0.cookie)
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
                    cookie=file.nfs2_cookie,
                ) for file in children],
                eof=eof,
            )
        )

    def STATFS(self, fh: bytes) -> StatfsRes:
        fs = self.fs_manager.get_fs_by_fh(fh)
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
    fs_manager = FileSystemManager([
        NullFS(b"/tmp/nfs2"),
    ])

    transport_server = TCPTransportServer("127.0.0.1", 2222)
    transport_server.register_prog(MountV1Service(fs_manager))
    transport_server.register_prog(NFSV2Service(fs_manager))
    await transport_server.notify_portmapper()

    server = await transport_server.start()

    async with server:
        await server.serve_forever()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
