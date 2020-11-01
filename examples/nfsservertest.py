import asyncio

from pynefs.server import TCPTransportServer
from pynefs.fs import FileSystemManager, VerifyingFileHandleEncoder
from pynefs.nfs2 import MountV1Service, NFSV2Service
from pynefs.nfs3 import NFSV3Service, MountV3Service
from pynefs.nullfs import NullFS


async def main():
    fs_manager = FileSystemManager(
        VerifyingFileHandleEncoder(b"foobar"),
        factories={
            b"/tmp/nfs2": lambda x: NullFS(read_only=False),
        },
    )

    transport_server = TCPTransportServer("127.0.0.1", 2222)
    transport_server.register_prog(MountV1Service(fs_manager))
    transport_server.register_prog(NFSV2Service(fs_manager))
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
