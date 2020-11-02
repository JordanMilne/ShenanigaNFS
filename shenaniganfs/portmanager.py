import datetime as dt
from typing import *

import shenaniganfs.generated.rfc1833_portmapper as pm
import shenaniganfs.generated.rfc1833_rpcbind as rb
from shenaniganfs.rpchelp import addr_to_rpcbind


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

    async def NULL(self) -> None:
        pass

    async def SET(self, arg_0: pm.Mapping) -> bool:
        return False

    async def UNSET(self, arg_0: pm.Mapping) -> bool:
        return False

    async def GETPORT(self, arg_0: pm.Mapping) -> int:
        prot_str = "tcp" if arg_0.prot == pm.IPPROTO_TCP else "udp"
        match = self.port_manager.get_mapping(arg_0.prog, prot_str)
        if not match:
            return 0
        return match.port

    async def DUMP(self) -> List[pm.Mapping]:
        return [
            x.to_portmapper() for x in self.port_manager.bindings if x.portmapper_compatible
        ]

    async def CALLIT(self, arg_0: pm.CallArgs) -> pm.CallResult:
        # We're not implementing this, it's a nightmare.
        # https://github.com/okirch/rpcbind/blob/b3b031b07cc5909aaf964f9d4cf46f6097769320/src/security.c#L284-L296
        return pm.CallResult(port=0, res=b"")


class SimpleRPCBind(rb.RPCBPROG_4_SERVER):
    min_vers = 3

    def __init__(self, port_manager: PortManager):
        super().__init__()
        self.port_manager = port_manager

    async def NULL(self) -> None:
        pass

    async def SET(self, arg_0: rb.RPCB) -> bool:
        return False

    async def UNSET(self, arg_0: rb.RPCB) -> bool:
        return False

    async def GETADDR(self, arg_0: rb.RPCB) -> bytes:
        match = self.port_manager.get_mapping(arg_0.r_prog, arg_0.r_netid.decode("utf8"))
        if not match:
            return b""
        return match.to_rpcbind().r_addr

    async def DUMP(self) -> List[rb.RPCB]:
        return [x.to_rpcbind() for x in self.port_manager.bindings]

    async def BCAST(self, arg_0: rb.RPCBRmtcallArgs) -> rb.RPCBRmtcallRes:
        return rb.RPCBRmtcallRes(b"", b"")

    async def GETTIME(self) -> int:
        return int(dt.datetime.now(tz=dt.timezone.utc).timestamp())

    async def UADDR2TADDR(self, arg_0: bytes) -> rb.Netbuf:
        return rb.Netbuf(0, b"")

    async def TADDR2UADDR(self, arg_0: rb.Netbuf) -> bytes:
        return b""

    async def GETVERSADDR(self, arg_0: rb.RPCB) -> bytes:
        match = self.port_manager.get_vers_mapping(arg_0.r_prog, arg_0.r_vers, arg_0.r_netid.decode("utf8"))
        if not match:
            return b""
        return match.to_rpcbind().r_addr

    async def INDIRECT(self, arg_0: rb.RPCBRmtcallArgs) -> rb.RPCBRmtcallRes:
        return rb.RPCBRmtcallRes(b"", b"")

    async def GETADDRLIST(self, arg_0: rb.RPCB) -> List[rb.RPCBEntry]:
        # semantics for this are hard to grok. Meh, doesn't seem to be used much.
        return []

    async def GETSTAT(self) -> List[rb.RPCBStat]:
        return []
