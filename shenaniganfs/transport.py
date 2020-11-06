import abc
import asyncio
import struct
import xdrlib
from io import BytesIO
from typing import *

from shenaniganfs.generated.rfc1831 import *
from shenaniganfs.rpchelp import Proc

SPLIT_MSG = Tuple[RPCMsg, bytes]

_T = TypeVar("T")
ProcRet = Union[ReplyBody, _T]


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

    @property
    def client_addr(self) -> Tuple:
        return ()

    @abc.abstractmethod
    def close(self):
        pass

    async def write_msg(self, header: RPCMsg, body: bytes) -> None:
        p = xdrlib.Packer()
        RPCMsg.pack(p, header)
        p.pack_fstring(len(body), body)
        await self.write_msg_bytes(p.get_buffer())

    async def read_msg(self) -> SPLIT_MSG:
        msg_bytes = await self.read_msg_bytes()
        unpacker = xdrlib.Unpacker(msg_bytes)
        msg = RPCMsg.unpack(unpacker)
        return msg, unpacker.get_buffer()[unpacker.get_position():]


class TCPTransport(BaseTransport):
    # 100KB, larger than UDP would allow anyway?
    MAX_MSG_BYTES = 100_000

    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.reader = reader
        self.writer = writer

    @property
    def closed(self):
        return self.reader.at_eof() or self.writer.is_closing()

    @property
    def client_addr(self) -> Tuple:
        return self.writer.get_extra_info('peername')

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


class CallContext:
    def __init__(self, transport: BaseTransport, msg: RPCMsg):
        self.msg = msg
        self.transport = transport


class Prog:
    """Base class for rpcgen-created server classes."""
    prog: int
    vers: int
    min_vers: Optional[int] = None
    procs: Dict[int, Proc]

    def supports_version(self, vers: int) -> bool:
        if self.min_vers is not None:
            return self.min_vers <= vers <= self.vers
        else:
            return self.vers == vers

    def get_handler(self, proc_id) -> Callable:
        return getattr(self, self.procs[proc_id].name)

    @staticmethod
    def _make_reply_body(
            accept_stat: Optional[AcceptStat] = None,
            reject_stat: Optional[RejectStat] = None,
            auth_stat: Optional[AuthStat] = None,
    ):
        if sum(x is None for x in (accept_stat, reject_stat)) != 1:
            raise Exception("Must specify either accept_stat OR reject_stat!")

        return ReplyBody(
            stat=ReplyStat.MSG_ACCEPTED if accept_stat is not None else ReplyStat.MSG_DENIED,
            areply=AcceptedReply(
                # TODO: this should be replaced on the way out,
                #  prog probably doesn't know which to use
                verf=OpaqueAuth(
                    flavor=AuthFlavor.AUTH_NONE,
                    body=b"",
                ),
                data=ReplyData(
                    stat=accept_stat,
                )
            ) if accept_stat is not None else None,
            rreply=RejectedReply(
                r_stat=reject_stat,
                auth_error=auth_stat,
            ) if reject_stat is not None else None,
        )

    async def handle_proc_call(self, call_ctx: CallContext, proc_id: int, call_body: bytes) \
            -> Union[ReplyBody, bytes]:
        proc = self.procs.get(proc_id)
        if proc is None:
            raise NotImplementedError()

        unpacker = xdrlib.Unpacker(call_body)
        argl = [arg_type.unpack(unpacker)
                for arg_type in proc.arg_types]
        handler: Callable = self.get_handler(proc_id)
        rv = await handler(call_ctx, *argl)
        if isinstance(rv, ReplyBody):
            return rv

        packer = xdrlib.Packer()
        proc.ret_type.pack(packer, rv)
        return packer.get_buffer()
