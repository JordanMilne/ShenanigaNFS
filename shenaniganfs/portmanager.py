import datetime as dt
from typing import *

import shenaniganfs.generated.rfc1831 as rpc
import shenaniganfs.generated.rfc1833_portmapper as pm
import shenaniganfs.generated.rfc1833_rpcbind as rb
from shenaniganfs.rpchelp import addr_to_rpcbind
from shenaniganfs.transport import CallContext, ProcRet


class PortBinding(NamedTuple):
    prog_num: int
    vers: int
    protocol: str
    host: str
    port: int
    owner: str

    @property
    def portmapper_compatible(self) -> bool:
        if self.protocol not in ("udp", "tcp"):
            return False
        if self.host != "0.0.0.0":
            return False
        return True

    def to_rpcbind(self) -> rb.RPCB:
        return rb.RPCB(
            r_prog=self.prog_num,
            r_vers=self.vers,
            r_netid=self.protocol.encode("utf8"),
            r_addr=addr_to_rpcbind(self.host, self.port),
            r_owner=self.owner.encode("utf8"),
        )

    def to_portmapper(self) -> pm.Mapping:
        return pm.Mapping(
            prog=self.prog_num,
            vers=self.vers,
            prot=pm.IPPROTO_TCP if self.protocol == "tcp" else pm.IPPROTO_UDP,
            port=self.port,
        )

    def match_tuple(self):
        return self.prog_num, self.protocol

    def vers_match_tuple(self):
        return self.prog_num, self.vers, self.protocol


class PortManager:
    def __init__(self):
        self.bindings: List[PortBinding] = []

    def set_port(self, binding: PortBinding):
        if binding in self.bindings:
            return
        self.bindings.append(binding)

    def get_mapping(self, prog: int, protocol: str) -> Optional[PortBinding]:
        matching = [b for b in self.bindings if b.match_tuple() == (prog, protocol)]
        if not matching:
            return None
        return matching[0]

    def get_vers_mapping(self, prog: int, vers: int, protocol: str) -> Optional[PortBinding]:
        matching = [b for b in self.bindings if b.vers_match_tuple() == (prog, vers, protocol)]
        if not matching:
            return None
        return matching[0]


class SimplePortMapper(pm.PMAP_PROG_2_SERVER):
    def __init__(self, port_manager: PortManager):
        super().__init__()
        self.port_manager = port_manager

    async def NULL(self, call_ctx: CallContext) -> ProcRet[None]:
        pass

    async def SET(self, call_ctx: CallContext, arg_0: pm.Mapping) -> ProcRet[bool]:
        return self._make_reply_body(
            reject_stat=rpc.RejectStat.AUTH_ERROR,
            # Somewhat of a misnomer, just catch-all for server doesn't
            # want to handle this call for security reasons.
            auth_stat=rpc.AuthStat.AUTH_TOOWEAK,
        )

    async def UNSET(self, call_ctx: CallContext, arg_0: pm.Mapping) -> ProcRet[bool]:
        return self._make_reply_body(
            reject_stat=rpc.RejectStat.AUTH_ERROR,
            auth_stat=rpc.AuthStat.AUTH_TOOWEAK,
        )

    async def GETPORT(self, call_ctx: CallContext, arg_0: pm.Mapping) -> ProcRet[int]:
        prot_str = "tcp" if arg_0.prot == pm.IPPROTO_TCP else "udp"
        match = self.port_manager.get_mapping(arg_0.prog, prot_str)
        if not match:
            return 0
        return match.port

    async def DUMP(self, call_ctx: CallContext) -> ProcRet[List[pm.Mapping]]:
        return [
            x.to_portmapper() for x in self.port_manager.bindings if x.portmapper_compatible
        ]

    async def CALLIT(self, call_ctx: CallContext, arg_0: pm.CallArgs) -> ProcRet[pm.CallResult]:
        # We're not implementing this, it's a nightmare.
        # https://github.com/okirch/rpcbind/blob/b3b031b07cc5909aaf964f9d4cf46f6097769320/src/security.c#L284-L296
        return self._make_reply_body(
            reject_stat=rpc.RejectStat.AUTH_ERROR,
            auth_stat=rpc.AuthStat.AUTH_TOOWEAK,
        )


class SimpleRPCBind(rb.RPCBPROG_4_SERVER):
    min_vers = 3

    def __init__(self, port_manager: PortManager):
        super().__init__()
        self.port_manager = port_manager

    async def NULL(self, call_ctx: CallContext) -> ProcRet[None]:
        pass

    async def SET(self, call_ctx: CallContext, arg_0: rb.RPCB) -> ProcRet[bool]:
        return self._make_reply_body(
            reject_stat=rpc.RejectStat.AUTH_ERROR,
            auth_stat=rpc.AuthStat.AUTH_TOOWEAK,
        )

    async def UNSET(self, call_ctx: CallContext, arg_0: rb.RPCB) -> ProcRet[bool]:
        return self._make_reply_body(
            reject_stat=rpc.RejectStat.AUTH_ERROR,
            auth_stat=rpc.AuthStat.AUTH_TOOWEAK,
        )

    async def GETADDR(self, call_ctx: CallContext, arg_0: rb.RPCB) -> ProcRet[bytes]:
        match = self.port_manager.get_mapping(arg_0.r_prog, arg_0.r_netid.decode("utf8"))
        if not match:
            return b""
        return match.to_rpcbind().r_addr

    async def DUMP(self, call_ctx: CallContext) -> ProcRet[List[rb.RPCB]]:
        return [x.to_rpcbind() for x in self.port_manager.bindings]

    async def BCAST(self, call_ctx: CallContext, arg_0: rb.RPCBRmtcallArgs) -> ProcRet[rb.RPCBRmtcallRes]:
        return self._make_reply_body(
            reject_stat=rpc.RejectStat.AUTH_ERROR,
            auth_stat=rpc.AuthStat.AUTH_TOOWEAK,
        )

    async def GETTIME(self, call_ctx: CallContext) -> ProcRet[int]:
        return int(dt.datetime.now(tz=dt.timezone.utc).timestamp())

    async def UADDR2TADDR(self, call_ctx: CallContext, arg_0: bytes) -> ProcRet[rb.Netbuf]:
        raise NotImplementedError()

    async def TADDR2UADDR(self, call_ctx: CallContext, arg_0: rb.Netbuf) -> ProcRet[bytes]:
        raise NotImplementedError()

    async def GETVERSADDR(self, call_ctx: CallContext, arg_0: rb.RPCB) -> ProcRet[bytes]:
        match = self.port_manager.get_vers_mapping(arg_0.r_prog, arg_0.r_vers, arg_0.r_netid.decode("utf8"))
        if not match:
            return b""
        return match.to_rpcbind().r_addr

    async def INDIRECT(self, call_ctx: CallContext, arg_0: rb.RPCBRmtcallArgs) -> ProcRet[rb.RPCBRmtcallRes]:
        return self._make_reply_body(
            reject_stat=rpc.RejectStat.AUTH_ERROR,
            auth_stat=rpc.AuthStat.AUTH_TOOWEAK,
        )

    async def GETADDRLIST(self, call_ctx: CallContext, arg_0: rb.RPCB) -> ProcRet[List[rb.RPCBEntry]]:
        # semantics for this are hard to grok. Meh, doesn't seem to be used much.
        raise NotImplementedError()

    async def GETSTAT(self, call_ctx: CallContext) -> ProcRet[List[rb.RPCBStat]]:
        raise NotImplementedError()
