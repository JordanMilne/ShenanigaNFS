import abc
import asyncio
import random
import xdrlib
from typing import *

from shenaniganfs import rpchelp
from shenaniganfs.generated.rfc1831 import *
from shenaniganfs.transport import BaseTransport, SPLIT_MSG, TCPTransport

_T = TypeVar("T")


class UnpackedRPCMsg(Generic[_T]):
    """Wrapper for a parsed message header and parsed return data"""
    def __init__(self, msg: RPCMsg, body: _T):
        self.msg = msg
        self.body: Optional[_T] = body

    def __repr__(self):
        return f"<{self.__class__.__name__}{(self.msg, self.body)!r}>"

    @property
    def xid(self) -> int:
        return self.msg.xid

    @xid.setter
    def xid(self, v):
        self.msg.xid = v

    @property
    def header(self):
        return self.msg.header

    @header.setter
    def header(self, v):
        self.msg.header = v

    @property
    def success(self):
        if self.msg.header.mtype != REPLY:
            raise ValueError("Tried to check success of call message?")
        if self.msg.header.rbody.stat != ReplyStat.MSG_ACCEPTED:
            return False
        if self.msg.header.rbody.areply.data.stat != AcceptStat.SUCCESS:
            return False
        return True


class BaseClient(rpchelp.Prog):
    transport: Optional[BaseTransport]

    def __init__(self):
        super().__init__()
        self.xid_map: Dict[int, asyncio.Future] = {}

    def __del__(self):
        try:
            self.disconnect()
        except RuntimeError:
            # Event loop may have already gone away
            pass

    async def __aenter__(self):
        if not self.transport:
            await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    @abc.abstractmethod
    async def connect(self):
        self.disconnect()

    @abc.abstractmethod
    def disconnect(self):
        self.kill_futures(asyncio.CancelledError("Connection is closing"))
        if self.transport is not None:
            self.transport.close()
            self.transport = None

    def pack_args(self, proc_id: int, args: Sequence):
        packer = xdrlib.Packer()
        arg_specs = self.procs[proc_id].arg_types
        if len(args) != len(arg_specs):
            raise ValueError("Wrong number of arguments!")

        for spec, arg in zip(arg_specs, args):
            spec.pack(packer, arg)
        return packer.get_buffer()

    def kill_futures(self, exc: Exception):
        # Tell anyone awaiting that the transport went away
        for xid, fut in self.xid_map.items():
            fut.set_exception(exc)
        self.xid_map.clear()

    def pump_reply(self, msg: SPLIT_MSG):
        reply, _ = msg
        xid_future = self.xid_map.pop(reply.xid, None)
        if not xid_future:
            # Got a reply for a message we didn't send???
            return
        if reply.header.mtype == MsgType.REPLY:
            xid_future.set_result(msg)
        else:
            xid_future.set_exception(ValueError(f"Expected REPLY, got {reply.header.mtype}"))

    def unpack_return(self, proc_id: int, body: bytes):
        unpacker = xdrlib.Unpacker(body)
        return self.procs[proc_id].ret_type.unpack(unpacker)

    @staticmethod
    def gen_xid() -> int:
        return random.getrandbits(32)

    async def send_call(self, proc_id: int, *args, xid: Optional[int] = None) -> UnpackedRPCMsg[_T]:
        if xid is None:
            xid = self.gen_xid()
        if not self.transport:
            await self.connect()

        msg = RPCMsg(
            xid=xid,
            header=RPCBody(
                mtype=MsgType.CALL,
                cbody=CallBody(
                    rpcvers=2,
                    prog=self.prog,
                    vers=self.vers,
                    proc=proc_id,
                    # always null auth for now
                    cred=OpaqueAuth(
                        flavor=AuthFlavor.AUTH_NONE,
                        body=b""
                    ),
                    verf=OpaqueAuth(
                        flavor=AuthFlavor.AUTH_NONE,
                        body=b""
                    ),
                )
            )
        )
        fut = asyncio.Future()
        self.xid_map[xid] = fut
        await self.transport.write_msg(msg, self.pack_args(proc_id, args))

        # TODO: timeout?
        reply_msg = await fut
        reply: RPCMsg = reply_msg[0]
        reply_body_bytes: bytes = reply_msg[1]

        assert(reply.header.mtype == REPLY)
        rbody = reply.header.rbody
        if rbody.stat != ReplyStat.MSG_ACCEPTED or rbody.areply.data.stat != AcceptStat.SUCCESS:
            return UnpackedRPCMsg(reply, None)
        return UnpackedRPCMsg(reply, self.unpack_return(proc_id, reply_body_bytes))


class TCPClient(BaseClient):
    def __init__(self, host, port):
        super().__init__()
        self.transport = None
        self.pump_replies_task: Optional[asyncio.Task] = None
        self.host = host
        self.port = port

    async def pump_replies(self):
        while self.transport and not self.transport.closed:
            try:
                self.pump_reply(await self.transport.read_msg())
            except asyncio.IncompleteReadError:
                self.disconnect()
        self.disconnect()

    async def connect(self):
        await super().connect()
        self.transport = TCPTransport(*await asyncio.open_connection(self.host, self.port))
        self.pump_replies_task = asyncio.create_task(self.pump_replies())

    def disconnect(self):
        super().disconnect()
        if self.pump_replies_task is not None:
            self.pump_replies_task.cancel()
            self.pump_replies_task = None
