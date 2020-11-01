import asyncio
import os
import weakref

from shenaniganfs.portmanager import PortManager, SimplePortMapper, SimpleRPCBind
from shenaniganfs.server import TCPTransportServer
from shenaniganfs.fs import SimpleFS, SimpleDirectory, SimpleFile, VerifyingFileHandleEncoder
from shenaniganfs.fs_manager import EvictingFileSystemManager, create_fs
from shenaniganfs.nfs2 import MountV1Service, NFSV2Service
from shenaniganfs.nfs3 import NFSV3Service, MountV3Service


class ExampleFS(SimpleFS):
    def __init__(self, read_only=True, size_quota=None, entries_quota=None):
        super().__init__(size_quota=size_quota, entries_quota=entries_quota)
        self.read_only = read_only
        self.num_blocks = 1
        self.free_blocks = 0
        self.avail_blocks = 0

        self.track_entry(SimpleDirectory(
            fs=weakref.ref(self),
            mode=0o0755,
            name=b"",
            root_dir=True,
        ))

        self.root_dir.link_child(SimpleFile(
            fs=weakref.ref(self),
            name=b"testfile.txt",
            mode=0o444 if read_only else 0o777,
            contents=bytearray(b"test\n"),
        ))


async def main():
    fs_manager = EvictingFileSystemManager(
        VerifyingFileHandleEncoder(os.urandom(32)),
        factories={
            b"/tmp/nfs2": lambda call_ctx: create_fs(
                ExampleFS,
                call_ctx,
                read_only=False,
                # Only 100 entries total allowed in the FS
                entries_quota=100,
                # names + contents not allowed to exceed this in bytes
                size_quota=100 * 1024
            ),
        },
    )

    port_manager = PortManager()

    rpcbind_transport_server = TCPTransportServer("0.0.0.0", 111)
    rpcbind_transport_server.register_prog(SimplePortMapper(port_manager))
    rpcbind_transport_server.register_prog(SimpleRPCBind(port_manager))
    rpcbind_transport_server.notify_port_manager(port_manager)

    transport_server = TCPTransportServer("127.0.0.1", 2222)
    transport_server.register_prog(MountV1Service(fs_manager))
    transport_server.register_prog(NFSV2Service(fs_manager))
    transport_server.register_prog(MountV3Service(fs_manager))
    transport_server.register_prog(NFSV3Service(fs_manager))
    transport_server.notify_port_manager(port_manager)

    await rpcbind_transport_server.start()
    server = await transport_server.start()

    async with server:
        await server.serve_forever()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
