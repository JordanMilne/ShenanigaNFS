import abc
import asyncio
import itertools
from typing import *

from shenaniganfs import rpchelp
from shenaniganfs.client import TCPClient
from shenaniganfs.generated.rfc1831 import *
import shenaniganfs.generated.rfc1833_rpcbind as rpcbind
from shenaniganfs.portmanager import PortBinding, PortManager
from shenaniganfs.transport import SPLIT_MSG, BaseTransport, TCPTransport


class CallContext:
    def __init__(self, transport: BaseTransport, msg: RPCMsg):
        self.msg = msg
        self.transport = transport


class TransportServer:
    def __init__(self):
        self.owner: str = ""
        self.progs: Set[rpchelp.Prog] = set()

    def register_prog(self, prog: rpchelp.Prog):
        self.progs.add(prog)

    async def notify_rpcbind(self, host="127.0.0.1", port=111):
        for prog in self.progs:
            async with SimpleRPCBindClient(host, port) as rpcb_client:
                await rpcb_client.SET(self.get_prog_port_binding(prog).to_rpcbind())

    def notify_port_manager(self, port_manager: PortManager):
        for prog in self.progs:
            port_manager.set_port(self.get_prog_port_binding(prog))

    @abc.abstractmethod
    def get_prog_port_binding(self, prog: rpchelp.Prog) -> PortBinding:
        pass

    async def handle_message(self, transport: BaseTransport, msg: SPLIT_MSG):
        call, body_bytes = msg
        if call.header.mtype == MsgType.CALL:
            await self.handle_call(transport, call, body_bytes)
        else:
            # TODO: what's the proper error code for this?
            err_msg = self.make_reply(call.xid, ReplyStat.MSG_ACCEPTED, AcceptStat.GARBAGE_ARGS)
            await transport.write_msg(err_msg, b"")

    async def handle_call(self, transport: BaseTransport, call: RPCMsg, call_body_bytes: bytes):
        stat = AcceptStat.SUCCESS
        mismatch: Optional[MismatchInfo] = None
        reply_body_bytes = b""
        cbody = call.header.cbody

        try:
            progs = [p for p in self.progs if p.prog == cbody.prog]
            if progs:
                vers_progs = [p for p in progs if p.supports_version(cbody.vers)]
                if vers_progs:
                    call_ctx = CallContext(transport, call)
                    reply_body_bytes = await vers_progs[0].handle_proc_call(call_ctx, cbody.proc, call_body_bytes)
                else:
                    prog_versions = itertools.chain(*[(p.vers, p.min_vers) for p in progs])
                    prog_versions = list(x for x in prog_versions if x is not None)
                    mismatch = MismatchInfo(min(prog_versions), max(prog_versions))
                    stat = AcceptStat.PROG_MISMATCH
            else:
                stat = AcceptStat.PROG_UNAVAIL

        except NotImplementedError:
            stat = AcceptStat.PROC_UNAVAIL
        except Exception:
            print(f"Failed in {cbody.prog}.{cbody.vers}.{cbody.proc}")
            reply_header = self.make_reply(call.xid, ReplyStat.MSG_ACCEPTED, AcceptStat.SYSTEM_ERR)
            await transport.write_msg(reply_header, b"")
            # Might not be able to gracefully handle this. try to kill the transport.
            transport.close()
            raise

        reply_header = self.make_reply(call.xid, ReplyStat.MSG_ACCEPTED, stat, mismatch)
        await transport.write_msg(reply_header, reply_body_bytes)

    @staticmethod
    def make_reply(xid, stat: ReplyStat = 0, msg_stat: Union[AcceptStat, RejectStat] = 0,
                   mismatch: Optional[MismatchInfo] = None) -> RPCMsg:
        return RPCMsg(
            xid=xid,
            header=RPCBody(
                mtype=MsgType.REPLY,
                rbody=ReplyBody(
                    stat=stat,
                    areply=AcceptedReply(
                        verf=OpaqueAuth(
                            AuthFlavor.AUTH_NONE,
                            body=b""
                        ),
                        data=ReplyData(
                            stat=msg_stat,
                            mismatch=mismatch,
                        )
                    )
                )
            )
        )


class TCPTransportServer(TransportServer):
    def __init__(self, bind_host, bind_port):
        super().__init__()
        self.bind_host, self.bind_port = bind_host, bind_port

    async def start(self) -> asyncio.AbstractServer:
        return await asyncio.start_server(self.handle_connection, self.bind_host, self.bind_port)

    async def handle_connection(self, reader, writer):
        transport = TCPTransport(reader, writer)
        while not transport.closed:
            try:
                read_ret = await asyncio.wait_for(transport.read_msg(), 1)
            except asyncio.TimeoutError:
                continue
            except asyncio.IncompleteReadError:
                transport.close()
                break

            await self.handle_message(transport, read_ret)
        transport.close()

    def get_prog_port_binding(self, prog: rpchelp.Prog) -> PortBinding:
        return PortBinding(
            prog_num=prog.prog,
            vers=prog.vers,
            protocol="tcp",
            # Same host as rpcbind
            host="0.0.0.0",
            port=self.bind_port,
            owner=self.owner,
        )


class SimpleRPCBindClient(TCPClient, rpcbind.RPCBPROG_4_CLIENT):
    pass
