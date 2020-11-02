from shenaniganfs.fs_manager import FileSystemManager
from shenaniganfs.nfs2 import MountV1Service, NFSV2Service
from shenaniganfs.nfs3 import MountV3Service, NFSV3Service
from shenaniganfs.portmanager import PortManager, SimplePortMapper, SimpleRPCBind
from shenaniganfs.server import TCPTransportServer


async def serve_nfs(fs_manager: FileSystemManager, use_internal_rpcbind=True):
    port_manager = PortManager()

    if use_internal_rpcbind:
        rpcbind_transport_server = TCPTransportServer("0.0.0.0", 111)
        rpcbind_transport_server.register_prog(SimplePortMapper(port_manager))
        rpcbind_transport_server.register_prog(SimpleRPCBind(port_manager))
        rpcbind_transport_server.notify_port_manager(port_manager)
        await rpcbind_transport_server.start()

    transport_server = TCPTransportServer("0.0.0.0", 2049)
    transport_server.register_prog(MountV1Service(fs_manager))
    transport_server.register_prog(NFSV2Service(fs_manager))
    transport_server.register_prog(MountV3Service(fs_manager))
    transport_server.register_prog(NFSV3Service(fs_manager))
    if use_internal_rpcbind:
        transport_server.notify_port_manager(port_manager)
    else:
        await transport_server.notify_rpcbind()

    server = await transport_server.start()

    async with server:
        await server.serve_forever()
