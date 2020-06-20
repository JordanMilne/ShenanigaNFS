import abc
import asyncio
from typing import *

from pynefs import rpchelp
from pynefs.client import TCPClient
from pynefs.generated.rfc1831 import *
from pynefs.generated.rfc1833_portmapper import *
from pynefs.generated.rfc1833_portmapper import PMAP_PROG_2_CLIENT
from pynefs.transport import SPLIT_MSG, BaseTransport, TCPTransport


class ConnCtx:
    def __init__(self):
        self.state = {}


class TransportServer:
    def __init__(self):
        self.progs: Set[rpchelp.Prog] = set()

    def register_prog(self, prog: rpchelp.Prog):
        self.progs.add(prog)

    async def notify_portmapper(self, host="127.0.0.1", port=111):
        for prog in self.progs:
            async with SimplePortmapperClient(host, port) as pmap_client:
                await pmap_client.SET(self.get_prog_port_mapping(prog))

    @abc.abstractmethod
    def get_prog_port_mapping(self, prog: rpchelp.Prog) -> mapping:
        pass

    async def handle_message(self, transport: BaseTransport, msg: SPLIT_MSG):
        call, call_body = msg
        if call.header.mtype == msg_type.CALL:
            await self.handle_call(transport, call, call_body)
        else:
            # TODO: what's the proper error code for this?
            err_msg = self.make_reply(call.xid, reply_stat.MSG_ACCEPTED, accept_stat.GARBAGE_ARGS)
            await transport.write_msg(err_msg, b"")

    async def handle_call(self, transport: BaseTransport, call: rpc_msg, call_body: bytes):
        stat: accept_stat = accept_stat.SUCCESS
        mismatch: Optional[mismatch_info] = None
        reply_body = b""
        cbody = call.header.cbody

        try:
            progs = [p for p in self.progs if p.prog == cbody.prog]
            if progs:
                vers_progs = [p for p in progs if p.vers == cbody.vers]
                if vers_progs:
                    reply_body = vers_progs[0].handle_proc_call(cbody.proc, call_body)
                else:
                    prog_versions = [p.vers for p in progs]
                    mismatch = mismatch_info(min(prog_versions), max(prog_versions))
                    stat = accept_stat.PROG_MISMATCH
            else:
                stat = accept_stat.PROG_UNAVAIL

        except NotImplementedError:
            stat = accept_stat.PROC_UNAVAIL
        except Exception:
            print(f"Failed in {cbody.prog}.{cbody.vers}.{cbody.proc}")
            reply_header = self.make_reply(call.xid, reply_stat.MSG_ACCEPTED, accept_stat.SYSTEM_ERR)
            await transport.write_msg(reply_header, b"")
            # Might not be able to gracefully handle this. try to kill the transport.
            transport.close()
            raise

        reply_header = self.make_reply(call.xid, reply_stat.MSG_ACCEPTED, stat, mismatch)
        await transport.write_msg(reply_header, reply_body)

    @staticmethod
    def make_reply(xid, stat: reply_stat = 0, msg_stat: Union[accept_stat, reject_stat] = 0,
                   mismatch: Optional[mismatch_info] = None) -> rpc_msg:
        return rpc_msg(
            xid=xid,
            header=v_rpc_body(
                mtype=msg_type.REPLY,
                rbody=v_reply_body(
                    stat=stat,
                    areply=accepted_reply(
                        verf=opaque_auth(
                            auth_flavor.AUTH_NONE,
                            body=b""
                        ),
                        data=v_reply_data(
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

    def get_prog_port_mapping(self, prog: rpchelp.Prog) -> mapping:
        return mapping(
            prog=prog.prog,
            vers=prog.vers,
            prot=IPPROTO_TCP,
            port=self.bind_port,
        )


class SimplePortmapperClient(TCPClient, PMAP_PROG_2_CLIENT):
    pass
