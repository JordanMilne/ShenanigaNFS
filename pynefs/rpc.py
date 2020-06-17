import abc
import asyncio

import struct
import typing
import xdrlib
from asyncio import StreamWriter, StreamReader
from io import BytesIO

from pynefs import rpchelp
from pynefs.generated.rfc1831 import *
from pynefs.generated.rfc1831 import rpc_msg


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


class TCPClient(rpchelp.BaseClient):
    def __init__(self, host, port):
        self.transport: typing.Optional[BaseTransport] = None
        self.host = host
        self.port = port

    async def connect(self):
        self.transport = TCPTransport(*await asyncio.open_connection(self.host, self.port))

    async def send_call(self, proc_id: int, args: typing.List[typing.Any], xid: typing.Optional[int] = None):
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
        packer = xdrlib.Packer()
        self.pack_args(proc_id, args, packer)
        await self.transport.write_msg(msg, packer.get_buffer())
        reply, reply_body = await self.transport.read_msg()

        if reply.body.val.stat != MSG_ACCEPTED:
            raise Exception("Reply indicated error!")
        unpacker = xdrlib.Unpacker(reply_body)
        print(reply)
        print(self.unpack_return(proc_id, unpacker))
