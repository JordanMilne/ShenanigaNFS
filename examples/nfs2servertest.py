import asyncio
import errno
import typing

from pynefs.server import TCPTransportServer
from pynefs.generated.rfc1094 import *
from pynefs.fs import FileSystemManager, FileType
from pynefs.nullfs import NullFS


class MountService(MOUNTPROG_1_SERVER):
    def __init__(self, fs_manager):
        self.fs_manager: FileSystemManager = fs_manager

    def NULL(self) -> None:
        pass

    def MNT(self, mount_path: bytes) -> v_fhstatus:
        fs = self.fs_manager.get_fs_by_root(mount_path)
        if fs is None:
            return v_fhstatus(
                errno=errno.ENOENT
            )
        return v_fhstatus(
            errno=0,
            directory=fs.fh,
        )

    def DUMP(self) -> typing.List[v_mountlist]:
        # State maintenance is only for informational purposes?
        # Let's just not bother then.
        return []

    def UMNT(self, arg_0: bytes) -> None:
        return

    def UMNTALL(self) -> None:
        return

    def EXPORT(self) -> typing.List[v_exportlist]:
        return [v_exportlist(fs.root_path, [b"*"]) for fs in self.fs_manager.filesystems]


class NFSv2Service(NFS_PROGRAM_2_SERVER):
    def __init__(self, fs_manager):
        super().__init__()
        self.fs_manager: FileSystemManager = fs_manager

    def NULL(self) -> None:
        pass

    def GETATTR(self, fh: bytes) -> v_attrstat:
        entry = self.fs_manager.get_entry_by_fh(fh)
        if not entry:
            return v_attrstat(stat.NFSERR_STALE)
        return v_attrstat(stat.NFS_OK, entry.to_fattr())

    def SETATTR(self, arg_0: v_sattrargs) -> v_attrstat:
        return v_attrstat(stat.NFSERR_ROFS)

    def ROOT(self) -> None:
        pass

    def LOOKUP(self, arg_0: v_diropargs) -> v_diropres:
        directory = self.fs_manager.get_entry_by_fh(arg_0.dir)
        if not directory:
            return v_diropres(stat.NFSERR_STALE)
        child = directory.get_child_by_name(arg_0.name)
        if not child:
            return v_diropres(stat.NFSERR_NOENT)
        return v_diropres(
            stat.NFS_OK, v_diropres_diropok(child.fh, child.to_fattr())
        )

    def READLINK(self, fh: bytes) -> v_readlinkres:
        entry = self.fs_manager.get_entry_by_fh(fh)
        if not entry:
            return v_readlinkres(stat.NFSERR_STALE)
        if entry.type != FileType.LINK:
            # TODO: Better error for this?
            return v_readlinkres(stat.NFSERR_NOENT)
        return v_readlinkres(stat.NFS_OK, entry.contents)

    def READ(self, read_args: v_readargs) -> v_readres:
        entry = self.fs_manager.get_entry_by_fh(read_args.file)
        if not entry:
            return v_readres(stat.NFSERR_STALE)
        # No special devices for now!
        if entry.type not in (FileType.LINK, FileType.REG):
            return v_readres(stat.NFSERR_IO)
        return v_readres(stat.NFS_OK, v_attrdat(
            attributes=entry.to_fattr(),
            data=entry.contents[read_args.offset:read_args.offset + read_args.count]
        ))

    def WRITECACHE(self) -> None:
        pass

    def WRITE(self, arg_0: v_writeargs) -> v_attrstat:
        return v_attrstat(stat.NFSERR_ROFS)

    def CREATE(self, arg_0: v_createargs) -> v_diropres:
        return v_diropres(stat.NFSERR_ROFS)

    def REMOVE(self, arg_0: v_diropargs) -> stat:
        return stat.NFSERR_ROFS

    def RENAME(self, arg_0: v_renameargs) -> stat:
        return stat.NFSERR_ROFS

    def LINK(self, arg_0: v_linkargs) -> stat:
        return stat.NFSERR_ROFS

    def SYMLINK(self, arg_0: v_symlinkargs) -> stat:
        return stat.NFSERR_ROFS

    def MKDIR(self, arg_0: v_createargs) -> v_diropres:
        return v_diropres(stat.NFSERR_ROFS)

    def RMDIR(self, arg_0: v_diropargs) -> stat:
        return stat.NFSERR_ROFS

    def READDIR(self, arg_0: v_readdirargs) -> v_readdirres:
        directory = self.fs_manager.get_entry_by_fh(arg_0.dir)
        if not directory:
            return v_readdirres(stat.NFSERR_STALE)
        null_cookie = not sum(arg_0.cookie)
        if null_cookie:
            cookie_idx = 0
        else:
            # TODO: should these change when the file is mutated?
            cookie_idx = directory.child_fhs.index(arg_0.cookie)
            if cookie_idx == -1:
                return v_readdirres(stat.NFSERR_NOENT)
            cookie_idx += 1

        children = directory.dir_listing[cookie_idx:cookie_idx + arg_0.count]
        eof = len(children) != arg_0.count
        return v_readdirres(
            stat.NFS_OK,
            v_readdirres_readdirok(
                entries=[v_entry(
                    fileid=file.fileid,
                    name=file.name,
                    cookie=file.fh[:4],
                ) for file in children],
                eof=eof,
            )
        )

    def STATFS(self, fh: bytes) -> v_statfsres:
        fs = self.fs_manager.get_fs_by_fh(fh)
        if not fs:
            return v_statfsres(stat.NFSERR_STALE)
        return v_statfsres(
            stat.NFS_OK,
            v_statfsres_info(
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
    transport_server.register_prog(MountService(fs_manager))
    transport_server.register_prog(NFSv2Service(fs_manager))
    await transport_server.notify_portmapper()

    server = await transport_server.start()

    async with server:
        await server.serve_forever()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
