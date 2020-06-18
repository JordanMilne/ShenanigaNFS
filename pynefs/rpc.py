import abc
import asyncio
import random
import struct
import xdrlib
from asyncio import StreamWriter, StreamReader
from io import BytesIO
from typing import *

from pynefs import rpchelp
from pynefs.generated.rfc1831 import *
from pynefs.generated.rfc1831 import rpc_msg


T = TypeVar("T")


class UnpackedRPCMsg(Generic[T]):
    def __init__(self, msg: v_rpc_msg, body: T):
        self.msg = msg
        self.body: Optional[T] = body

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
        if self.msg.header.rbody.stat != MSG_ACCEPTED:
            return False
        if self.msg.header.rbody.areply.data.stat != accept_stat.SUCCESS:
            return False
        return True


SPLIT_MSG = Tuple[v_rpc_msg, bytes]


class BaseTransport(abc.ABC):
    @abc.abstractmethod
    async def write_msg_bytes(self, msg: bytes):
        pass

    @abc.abstractmethod
    async def read_msg_bytes(self) -> bytes:
        pass

    @property
    def closed(self):
        return False

    @abc.abstractmethod
    def close(self):
        pass

    async def write_msg(self, header: v_rpc_msg, body: bytes) -> None:
        p = xdrlib.Packer()
        rpc_msg.pack(p, header)
        p.pack_fstring(len(body), body)
        await self.write_msg_bytes(p.get_buffer())

    async def read_msg(self) -> SPLIT_MSG:
        msg_bytes = await self.read_msg_bytes()
        unpacker = xdrlib.Unpacker(msg_bytes)
        msg = rpc_msg.unpack(unpacker)
        return msg, unpacker.get_buffer()[unpacker.get_position():]


class TCPTransport(BaseTransport):
    # 100KB, larger than UDP would allow anyway?
    MAX_MSG_BYTES = 100_000

    def __init__(self, reader: StreamReader, writer: StreamWriter):
        self.reader = reader
        self.writer = writer

    @property
    def closed(self):
        return self.reader.at_eof() or self.writer.is_closing()

    def close(self):
        if self.writer.can_write_eof():
            self.writer.write_eof()
        if not self.writer.is_closing():
            self.writer.close()

    async def write_msg_bytes(self, msg: bytes):
        # Tack on the fragment size, mark as last frag
        msg = struct.pack("!L", len(msg) | (1 << 31)) + msg
        self.writer.write(msg)
        await self.writer.drain()

    async def read_msg_bytes(self) -> bytes:
        last_frag = False
        msg_bytes = BytesIO()
        total_len = 0
        while not last_frag:
            frag_header = struct.unpack("!L", await self.reader.readexactly(4))[0]
            last_frag = frag_header & (1 << 31)
            frag_len = frag_header & (~(1 << 31))
            total_len += frag_len
            if total_len > self.MAX_MSG_BYTES:
                raise ValueError(f"Overly large RPC message! {total_len}, {frag_len}")
            msg_bytes.write(await self.reader.readexactly(frag_len))
        return msg_bytes.getvalue()


class BaseClient(abc.ABC):
    prog: int
    vers: int
    procs: Dict[int, rpchelp.Proc]
    transport: Optional[BaseTransport]

    def __init__(self):
        self.xid_map: Dict[int, asyncio.Future] = {}

    def pack_args(self, proc_id: int, args: Sequence):
        packer = xdrlib.Packer()
        arg_specs = self.procs[proc_id].arg_types
        if len(args) != len(arg_specs):
            raise ValueError("Wrong number of arguments!")

        for spec, arg in zip(arg_specs, args):
            spec.pack(packer, arg)
        return packer.get_buffer()

    def kill_futures(self, exc: Exception):
        # Tell anyone awaiting that the sockets went away
        for xid, fut in self.xid_map.items():
            fut.set_exception(exc)
        self.xid_map.clear()

    def pump_reply(self, msg: SPLIT_MSG):
        reply, reply_body = msg
        if not reply.header.mtype == msg_type.REPLY:
            # Weird. log this.
            return
        xid_future = self.xid_map.pop(reply.xid, None)
        if not xid_future:
            # Got a reply for a message we didn't send???
            return
        xid_future.set_result(msg)

    def unpack_return(self, proc_id: int, body: bytes):
        unpacker = xdrlib.Unpacker(body)
        return self.procs[proc_id].ret_type.unpack(unpacker)

    @staticmethod
    def gen_xid() -> int:
        return random.getrandbits(32)

    @abc.abstractmethod
    async def connect(self):
        pass

    async def send_call(self, proc_id: int, *args, xid: Optional[int] = None) -> UnpackedRPCMsg[T]:
        if xid is None:
            xid = self.gen_xid()
        if not self.transport:
            await self.connect()

        msg = v_rpc_msg(
            xid=xid,
            header=v_rpc_body(
                mtype=msg_type.CALL,
                cbody=v_call_body(
                    rpcvers=2,
                    prog=self.prog,
                    vers=self.vers,
                    proc=proc_id,
                    # always null auth for now
                    cred=v_opaque_auth(
                        flavor=auth_flavor.AUTH_NONE,
                        body=b""
                    ),
                    verf=v_opaque_auth(
                        flavor=auth_flavor.AUTH_NONE,
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
        reply: v_rpc_msg = reply_msg[0]
        reply_body: bytes = reply_msg[1]

        assert(reply.header.mtype == REPLY)
        rbody = reply.header.rbody
        if rbody.stat != reply_stat.MSG_ACCEPTED or rbody.areply.data.stat != accept_stat.SUCCESS:
            return UnpackedRPCMsg(reply, None)
        return UnpackedRPCMsg(reply, self.unpack_return(proc_id, reply_body))


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
            except asyncio.IncompleteReadError as e:
                self.transport.close()
                self.kill_futures(e)
        self.kill_futures(asyncio.CancelledError("Connection is closing"))

    async def connect(self):
        self.kill_futures(asyncio.CancelledError("Connection is closing"))
        self.transport = TCPTransport(*await asyncio.open_connection(self.host, self.port))
        self.pump_replies_task = asyncio.create_task(self.pump_replies())


class ConnCtx:
    def __init__(self):
        self.state = {}


class TransportServer:
    def __init__(self):
        self.progs: Set[ProgServer] = set()

    def register_prog(self, prog: "ProgServer"):
        self.progs.add(prog)

    async def handle_message(self, transport: BaseTransport, msg: SPLIT_MSG):
        call, call_body = msg
        if call.header.mtype == msg_type.CALL:
            await self.handle_call(transport, call, call_body)
        else:
            # TODO: what's the proper error code for this?
            err_msg = self.make_reply(call.xid, reply_stat.MSG_ACCEPTED, accept_stat.GARBAGE_ARGS)
            await transport.write_msg(err_msg, b"")

    async def handle_call(self, transport: BaseTransport, call: v_rpc_msg, call_body: bytes):
        stat: accept_stat = accept_stat.SUCCESS
        mismatch: Optional[v_mismatch_info] = None
        reply_body = b""

        try:
            cbody = call.header.cbody
            progs = [p for p in self.progs if p.prog == cbody.prog]
            if progs:
                vers_progs = [p for p in progs if p.vers == cbody.vers]
                if vers_progs:
                    reply_body = vers_progs[0].handle_proc_call(cbody.proc, call_body)
                else:
                    prog_versions = [p.vers for p in progs]
                    mismatch = v_mismatch_info(min(prog_versions), max(prog_versions))
                    stat = accept_stat.PROG_MISMATCH
            else:
                stat = accept_stat.PROG_UNAVAIL

        except NotImplementedError:
            stat = accept_stat.PROC_UNAVAIL
        except Exception:
            reply_header = self.make_reply(call.xid, reply_stat.MSG_ACCEPTED, accept_stat.SYSTEM_ERR)
            await transport.write_msg(reply_header, b"")
            # Might not be able to gracefully handle this. try to kill the transport.
            transport.close()
            raise

        reply_header = self.make_reply(call.xid, reply_stat.MSG_ACCEPTED, stat, mismatch)
        await transport.write_msg(reply_header, reply_body)

    @staticmethod
    def make_reply(xid, stat: reply_stat = 0, msg_stat: Union[accept_stat, reject_stat] = 0,
                   mismatch: Optional[v_mismatch_info] = None) -> v_rpc_msg:
        return v_rpc_msg(
            xid=xid,
            header=v_rpc_body(
                mtype=msg_type.REPLY,
                rbody=v_reply_body(
                    stat=stat,
                    areply=v_accepted_reply(
                        verf=v_opaque_auth(
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


class ProgServer:
    """Base class for rpcgen-created server classes."""
    prog: int
    vers: int
    procs: Dict[int, rpchelp.Proc]

    def get_handler(self, proc_id) -> Callable:
        return getattr(self, self.procs[proc_id].name)

    def handle_proc_call(self, proc_id, call_body: bytes) -> bytes:
        proc = self.procs.get(proc_id)
        if proc is None:
            raise NotImplementedError()

        unpacker = xdrlib.Unpacker(call_body)
        argl = [arg_type.unpack(unpacker)
                for arg_type in proc.arg_types]
        rv = self.get_handler(proc_id)(*argl)

        packer = xdrlib.Packer()
        proc.ret_type.pack(packer, rv)
        return packer.get_buffer()