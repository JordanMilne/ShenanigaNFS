import abc
import asyncio
import random

import struct
import typing
import xdrlib
from asyncio import StreamWriter, StreamReader
from io import BytesIO

from pynefs import rpchelp
from pynefs.generated.rfc1831 import *
from pynefs.generated.rfc1831 import rpc_msg


class Server:
    """Base class for rpcgen-created server classes.  Unpack arguments,
    dispatch to appropriate procedure, and pack return value.  Check,
    at instantiation time, whether there are any procedures defined in the
    IDL which are both unimplemented and whose names are missing from the
    deliberately_unimplemented member.
    As a convenience, allows creation of transport server w/
    create_transport_server.  In what every way the server is created,
    you must call register."""
    prog: int
    vers: int
    procs: typing.Dict[int, rpchelp.Proc]

    def __init__(self):
        pass

    def get_handler(self, proc_id) -> typing.Callable:
        return getattr(self, self.procs[proc_id].name)

    def register(self, transport_server):
        transport_server.register(self.prog, self.vers, self)

    def handle_proc_call(self, proc_id, unpacker: xdrlib.Unpacker) -> bytes:
        proc = self.procs[proc_id]
        if proc is None:
            raise NotImplementedError()

        argl = [arg_type.unpack(unpacker)
                for arg_type in proc.arg_types]
        rv = self.get_handler(proc_id)(*argl)

        packer = xdrlib.Packer()
        proc.ret_type.pack(packer, rv)
        return packer.get_buffer()


class BaseClient(abc.ABC):
    prog: int
    vers: int
    procs: typing.Dict[int, rpchelp.Proc]

    def pack_args(self, proc_id: int, args: typing.List[typing.Any]):
        packer = xdrlib.Packer()
        arg_specs = self.procs[proc_id].arg_types
        if len(args) != len(arg_specs):
            raise ValueError("Wrong number of arguments!")

        for spec, arg in zip(arg_specs, args):
            spec.pack(packer, arg)
        return packer.get_buffer()

    def unpack_return(self, proc_id: int, body: bytes):
        unpacker = xdrlib.Unpacker(body)
        return self.procs[proc_id].ret_type.unpack(unpacker)

    def gen_xid(self) -> int:
        return random.getrandbits(32)

    @abc.abstractmethod
    async def connect(self):
        pass

    @abc.abstractmethod
    async def send_call(self, proc_id: int,
                        args: typing.List[typing.Any],
                        xid: typing.Optional[int] = None) -> typing.Tuple[v_rpc_msg, typing.Any]:
        pass


class BaseTransport(abc.ABC):
    @abc.abstractmethod
    async def write_msg_bytes(self, msg: bytes):
        pass

    @abc.abstractmethod
    async def read_msg_bytes(self) -> bytes:
        pass

    async def write_msg(self, header: v_rpc_msg, body: bytes) -> None:
        p = xdrlib.Packer()
        rpc_msg.pack(p, header)
        p.pack_fstring(len(body), body)
        await self.write_msg_bytes(p.get_buffer())

    async def read_msg(self) -> typing.Tuple[v_rpc_msg, bytes]:
        msg_bytes = await self.read_msg_bytes()
        unpacker = xdrlib.Unpacker(msg_bytes)
        msg = rpc_msg.unpack(unpacker)
        return msg, unpacker.get_buffer()[unpacker.get_position():]


class TCPTransport(BaseTransport):
    def __init__(self, reader: StreamReader, writer: StreamWriter):
        self.reader = reader
        self.writer = writer

    async def write_msg_bytes(self, msg: bytes):
        # Tack on the fragment size, mark as last frag
        msg = struct.pack("!L", len(msg) | (1 << 31)) + msg
        self.writer.write(msg)
        await self.writer.drain()

    async def read_msg_bytes(self) -> bytes:
        last_frag = False
        msg_bytes = BytesIO()
        while not last_frag:
            frag_header = struct.unpack("!L", await self.reader.readexactly(4))[0]
            last_frag = frag_header & (1 << 31)
            frag_len = frag_header & (~(1 << 31))
            msg_bytes.write(await self.reader.readexactly(frag_len))
        return msg_bytes.getvalue()


class TCPClient(BaseClient):
    def __init__(self, host, port):
        self.transport: typing.Optional[BaseTransport] = None
        self.host = host
        self.port = port

    async def connect(self):
        self.transport = TCPTransport(*await asyncio.open_connection(self.host, self.port))

    async def send_call(self, proc_id: int,
                        args: typing.List[typing.Any],
                        xid: typing.Optional[int] = None) -> typing.Tuple[v_rpc_msg, typing.Any]:
        if xid is None:
            xid = self.gen_xid()
        if not self.transport:
            await self.connect()

        msg = v_rpc_msg(
            xid,
            v_rpc_body(mtype=CALL, val=v_call_body(
                rpcvers=2,
                prog=self.prog,
                vers=self.vers,
                proc=proc_id,
                # always null auth for now
                cred=v_opaque_auth(
                    flavor=AUTH_NONE,
                    body=b""
                ),
                verf=v_opaque_auth(
                    flavor=AUTH_NONE,
                    body=b""
                ),
            ))
        )
        await self.transport.write_msg(msg, self.pack_args(proc_id, args))

        # TODO: Almost definitely bad, no guarantee reply immediately follows.
        # should return a Future and pump messages instead?
        reply, reply_body = await self.transport.read_msg()

        if reply.body.val.stat != MSG_ACCEPTED:
            return reply, None
        return reply, self.unpack_return(proc_id, reply_body)
