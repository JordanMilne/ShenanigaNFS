import asyncio
import errno
import typing

from pynefs.server import TCPTransportServer
from pynefs.generated.rfc1094 import *
from pynefs.fs import FileSystemManager, FileType
from pynefs.nullfs import NullFS


class MountV1Service(MOUNTPROG_1_SERVER):
    def __init__(self, fs_manager):
        self.fs_manager: FileSystemManager = fs_manager

    def NULL(self) -> None:
        pass

    def MNT(self, mount_path: bytes) -> fhstatus:
        fs = self.fs_manager.get_fs_by_root(mount_path)
        if fs is None:
            return fhstatus(
                errno=errno.ENOENT
            )
        return fhstatus(
            errno=0,
            directory=fs.fh,
        )

    def DUMP(self) -> typing.List[mountlist]:
        # State maintenance is only for informational purposes?
        # Let's just not bother then.
        return []

    def UMNT(self, arg_0: bytes) -> None:
        return

    def UMNTALL(self) -> None:
        return

    def EXPORT(self) -> typing.List[exportlist]:
        return [exportlist(fs.root_path, [b"*"]) for fs in self.fs_manager.filesystems]


class NFSV2Service(NFS_PROGRAM_2_SERVER):
    def __init__(self, fs_manager):
        super().__init__()
        self.fs_manager: FileSystemManager = fs_manager

    def NULL(self) -> None:
        pass

    def GETATTR(self, fh: bytes) -> attrstat:
        fs_entry = self.fs_manager.get_entry_by_fh(fh)
        if not fs_entry:
            return attrstat(stat.NFSERR_STALE)
        return attrstat(stat.NFS_OK, fs_entry.to_nfs2_fattr())

    def SETATTR(self, arg_0: sattrargs) -> attrstat:
        return attrstat(stat.NFSERR_ROFS)

    def ROOT(self) -> None:
        pass

    def LOOKUP(self, arg_0: diropargs) -> diropres:
        directory = self.fs_manager.get_entry_by_fh(arg_0.dir)
        if not directory:
            return diropres(stat.NFSERR_STALE)
        child = directory.get_child_by_name(arg_0.name)
        if not child:
            return diropres(stat.NFSERR_NOENT)
        return diropres(
            stat.NFS_OK, diropres_diropok(child.fh, child.to_nfs2_fattr())
        )

    def READLINK(self, fh: bytes) -> readlinkres:
        fs_entry = self.fs_manager.get_entry_by_fh(fh)
        if not fs_entry:
            return readlinkres(stat.NFSERR_STALE)
        if fs_entry.type != FileType.LINK:
            # TODO: Better error for this?
            return readlinkres(stat.NFSERR_NOENT)
        return readlinkres(stat.NFS_OK, fs_entry.contents)

    def READ(self, read_args: readargs) -> readres:
        fs_entry = self.fs_manager.get_entry_by_fh(read_args.file)
        if not fs_entry:
            return readres(stat.NFSERR_STALE)
        # No special devices for now!
        if fs_entry.type not in (FileType.LINK, FileType.REG):
            return readres(stat.NFSERR_IO)
        return readres(stat.NFS_OK, attrdat(
            attributes=fs_entry.to_nfs2_fattr(),
            data=fs_entry.contents[read_args.offset:read_args.offset + read_args.count]
        ))

    def WRITECACHE(self) -> None:
        pass

    def WRITE(self, arg_0: writeargs) -> attrstat:
        return attrstat(stat.NFSERR_ROFS)

    def CREATE(self, arg_0: createargs) -> diropres:
        return diropres(stat.NFSERR_ROFS)

    def REMOVE(self, arg_0: diropargs) -> stat:
        return stat.NFSERR_ROFS

    def RENAME(self, arg_0: renameargs) -> stat:
        return stat.NFSERR_ROFS

    def LINK(self, arg_0: linkargs) -> stat:
        return stat.NFSERR_ROFS

    def SYMLINK(self, arg_0: symlinkargs) -> stat:
        return stat.NFSERR_ROFS

    def MKDIR(self, arg_0: createargs) -> diropres:
        return diropres(stat.NFSERR_ROFS)

    def RMDIR(self, arg_0: diropargs) -> stat:
        return stat.NFSERR_ROFS

    def READDIR(self, arg_0: readdirargs) -> readdirres:
        directory = self.fs_manager.get_entry_by_fh(arg_0.dir)
        count = min(arg_0.count, 50)
        if not directory:
            return readdirres(stat.NFSERR_STALE)

        cookie_idx = 0
        null_cookie = not sum(arg_0.cookie)
        if not null_cookie:
            cookie_idx = [e.nfs2_cookie for e in directory.children].index(arg_0.cookie)
            if cookie_idx == -1:
                return readdirres(stat.NFSERR_NOENT)
            cookie_idx += 1

        children = directory.children[cookie_idx:cookie_idx + count]
        eof = len(children) != count
        return readdirres(
            stat.NFS_OK,
            readdirres_readdirok(
                entries=[entry(
                    fileid=file.fileid,
                    name=file.name,
                    cookie=file.nfs2_cookie,
                ) for file in children],
                eof=eof,
            )
        )

    def STATFS(self, fh: bytes) -> statfsres:
        fs = self.fs_manager.get_fs_by_fh(fh)
        if not fs:
            return statfsres(stat.NFSERR_STALE)
        return statfsres(
            stat.NFS_OK,
            statfsres_info(
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
