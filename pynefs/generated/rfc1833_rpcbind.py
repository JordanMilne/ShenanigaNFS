# Auto-generated from IDL file
import abc
import dataclasses
import typing
from dataclasses import dataclass

from pynefs import rpchelp

TRUE = True
FALSE = False

RPCB_PORT = 111
@dataclass
class rpcb(rpchelp.struct):
    r_prog: int = rpchelp.rpc_field(rpchelp.r_uint)
    r_vers: int = rpchelp.rpc_field(rpchelp.r_uint)
    r_netid: bytes = rpchelp.rpc_field(rpchelp.string(rpchelp.LengthType.VAR, None))
    r_addr: bytes = rpchelp.rpc_field(rpchelp.string(rpchelp.LengthType.VAR, None))
    r_owner: bytes = rpchelp.rpc_field(rpchelp.string(rpchelp.LengthType.VAR, None))

@dataclass
class rp__list(rpchelp.linked_list):
    rpcb_map: rpcb = rpchelp.rpc_field(rpcb)

rpcblist = rp__list
@dataclass
class rpcb_rmtcallargs(rpchelp.struct):
    prog: int = rpchelp.rpc_field(rpchelp.r_uint)
    vers: int = rpchelp.rpc_field(rpchelp.r_uint)
    proc: int = rpchelp.rpc_field(rpchelp.r_uint)
    args: bytes = rpchelp.rpc_field(rpchelp.opaque(rpchelp.LengthType.VAR, None))

@dataclass
class rpcb_rmtcallres(rpchelp.struct):
    addr: bytes = rpchelp.rpc_field(rpchelp.string(rpchelp.LengthType.VAR, None))
    results: bytes = rpchelp.rpc_field(rpchelp.opaque(rpchelp.LengthType.VAR, None))

@dataclass
class rpcb_entry(rpchelp.struct):
    r_maddr: bytes = rpchelp.rpc_field(rpchelp.string(rpchelp.LengthType.VAR, None))
    r_nc_netid: bytes = rpchelp.rpc_field(rpchelp.string(rpchelp.LengthType.VAR, None))
    r_nc_semantics: int = rpchelp.rpc_field(rpchelp.r_uint)
    r_nc_protofmly: bytes = rpchelp.rpc_field(rpchelp.string(rpchelp.LengthType.VAR, None))
    r_nc_proto: bytes = rpchelp.rpc_field(rpchelp.string(rpchelp.LengthType.VAR, None))

@dataclass
class rpcb_entry_list(rpchelp.linked_list):
    rpcb_entry_map: rpcb_entry = rpchelp.rpc_field(rpcb_entry)

rpcb_highproc_2 = 5
rpcb_highproc_3 = 8
rpcb_highproc_4 = 12
RPCBSTAT_HIGHPROC = 13
RPCBVERS_STAT = 3
RPCBVERS_4_STAT = 2
RPCBVERS_3_STAT = 1
RPCBVERS_2_STAT = 0
@dataclass
class rpcbs_addrlist(rpchelp.linked_list):
    prog: int = rpchelp.rpc_field(rpchelp.r_uint)
    vers: int = rpchelp.rpc_field(rpchelp.r_uint)
    success: int = rpchelp.rpc_field(rpchelp.r_int)
    failure: int = rpchelp.rpc_field(rpchelp.r_int)
    netid: bytes = rpchelp.rpc_field(rpchelp.string(rpchelp.LengthType.VAR, None))

@dataclass
class rpcbs_rmtcalllist(rpchelp.linked_list):
    prog: int = rpchelp.rpc_field(rpchelp.r_uint)
    vers: int = rpchelp.rpc_field(rpchelp.r_uint)
    proc: int = rpchelp.rpc_field(rpchelp.r_uint)
    success: int = rpchelp.rpc_field(rpchelp.r_int)
    failure: int = rpchelp.rpc_field(rpchelp.r_int)
    indirect: int = rpchelp.rpc_field(rpchelp.r_int)
    netid: bytes = rpchelp.rpc_field(rpchelp.string(rpchelp.LengthType.VAR, None))

rpcbs_proc = rpchelp.arr(rpchelp.r_int, rpchelp.LengthType.FIXED, RPCBSTAT_HIGHPROC)
@dataclass
class rpcb_stat(rpchelp.struct):
    info: typing.List[int] = rpchelp.rpc_field(rpcbs_proc)
    setinfo: int = rpchelp.rpc_field(rpchelp.r_int)
    unsetinfo: int = rpchelp.rpc_field(rpchelp.r_int)
    addrinfo: typing.List[rpcbs_addrlist] = rpchelp.rpc_field(rpchelp.opt_data(rpcbs_addrlist))
    rmtinfo: typing.List[rpcbs_rmtcalllist] = rpchelp.rpc_field(rpchelp.opt_data(rpcbs_rmtcalllist))

rpcb_stat_byvers = rpchelp.arr(rpcb_stat, rpchelp.LengthType.FIXED, RPCBVERS_STAT)
@dataclass
class netbuf(rpchelp.struct):
    maxlen: int = rpchelp.rpc_field(rpchelp.r_uint)
    buf: bytes = rpchelp.rpc_field(rpchelp.opaque(rpchelp.LengthType.VAR, None))


from pynefs import client


class RPCBPROG_3_SERVER(rpchelp.Prog):
    prog = 100000
    vers = 3
    procs = {
        0: rpchelp.Proc('NULL', rpchelp.r_void, []),
        1: rpchelp.Proc('SET', rpchelp.r_bool, [rpcb]),
        2: rpchelp.Proc('UNSET', rpchelp.r_bool, [rpcb]),
        3: rpchelp.Proc('GETADDR', rpchelp.r_string, [rpcb]),
        4: rpchelp.Proc('DUMP', rpcblist, []),
        5: rpchelp.Proc('CALLIT', rpcb_rmtcallres, [rpcb_rmtcallargs]),
        6: rpchelp.Proc('GETTIME', rpchelp.r_uint, []),
        7: rpchelp.Proc('UADDR2TADDR', netbuf, [rpchelp.r_string]),
        8: rpchelp.Proc('TADDR2UADDR', rpchelp.r_string, [netbuf]),
    }

    @abc.abstractmethod
    def NULL(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def SET(self, arg_0: rpcb) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def UNSET(self, arg_0: rpcb) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def GETADDR(self, arg_0: rpcb) -> bytes:
        raise NotImplementedError()

    @abc.abstractmethod
    def DUMP(self) -> typing.List[typing.Union[rpcb, rp__list]]:
        raise NotImplementedError()

    @abc.abstractmethod
    def CALLIT(self, arg_0: rpcb_rmtcallargs) -> rpcb_rmtcallres:
        raise NotImplementedError()

    @abc.abstractmethod
    def GETTIME(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    def UADDR2TADDR(self, arg_0: bytes) -> netbuf:
        raise NotImplementedError()

    @abc.abstractmethod
    def TADDR2UADDR(self, arg_0: netbuf) -> bytes:
        raise NotImplementedError()


class RPCBPROG_4_SERVER(rpchelp.Prog):
    prog = 100000
    vers = 4
    procs = {
        0: rpchelp.Proc('NULL', rpchelp.r_void, []),
        1: rpchelp.Proc('SET', rpchelp.r_bool, [rpcb]),
        2: rpchelp.Proc('UNSET', rpchelp.r_bool, [rpcb]),
        3: rpchelp.Proc('GETADDR', rpchelp.r_string, [rpcb]),
        4: rpchelp.Proc('DUMP', rpcblist, []),
        5: rpchelp.Proc('BCAST', rpcb_rmtcallres, [rpcb_rmtcallargs]),
        6: rpchelp.Proc('GETTIME', rpchelp.r_uint, []),
        7: rpchelp.Proc('UADDR2TADDR', netbuf, [rpchelp.r_string]),
        8: rpchelp.Proc('TADDR2UADDR', rpchelp.r_string, [netbuf]),
        9: rpchelp.Proc('GETVERSADDR', rpchelp.r_string, [rpcb]),
        10: rpchelp.Proc('INDIRECT', rpcb_rmtcallres, [rpcb_rmtcallargs]),
        11: rpchelp.Proc('GETADDRLIST', rpcb_entry_list, [rpcb]),
        12: rpchelp.Proc('GETSTAT', rpcb_stat_byvers, []),
    }

    @abc.abstractmethod
    def NULL(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def SET(self, arg_0: rpcb) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def UNSET(self, arg_0: rpcb) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def GETADDR(self, arg_0: rpcb) -> bytes:
        raise NotImplementedError()

    @abc.abstractmethod
    def DUMP(self) -> typing.List[typing.Union[rpcb, rp__list]]:
        raise NotImplementedError()

    @abc.abstractmethod
    def BCAST(self, arg_0: rpcb_rmtcallargs) -> rpcb_rmtcallres:
        raise NotImplementedError()

    @abc.abstractmethod
    def GETTIME(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    def UADDR2TADDR(self, arg_0: bytes) -> netbuf:
        raise NotImplementedError()

    @abc.abstractmethod
    def TADDR2UADDR(self, arg_0: netbuf) -> bytes:
        raise NotImplementedError()

    @abc.abstractmethod
    def GETVERSADDR(self, arg_0: rpcb) -> bytes:
        raise NotImplementedError()

    @abc.abstractmethod
    def INDIRECT(self, arg_0: rpcb_rmtcallargs) -> rpcb_rmtcallres:
        raise NotImplementedError()

    @abc.abstractmethod
    def GETADDRLIST(self, arg_0: rpcb) -> typing.List[typing.Union[rpcb_entry, rpcb_entry_list]]:
        raise NotImplementedError()

    @abc.abstractmethod
    def GETSTAT(self) -> typing.List[rpcb_stat]:
        raise NotImplementedError()


class RPCBPROG_3_CLIENT(client.BaseClient):
    prog = 100000
    vers = 3
    procs = {
        0: rpchelp.Proc('NULL', rpchelp.r_void, []),
        1: rpchelp.Proc('SET', rpchelp.r_bool, [rpcb]),
        2: rpchelp.Proc('UNSET', rpchelp.r_bool, [rpcb]),
        3: rpchelp.Proc('GETADDR', rpchelp.r_string, [rpcb]),
        4: rpchelp.Proc('DUMP', rpcblist, []),
        5: rpchelp.Proc('CALLIT', rpcb_rmtcallres, [rpcb_rmtcallargs]),
        6: rpchelp.Proc('GETTIME', rpchelp.r_uint, []),
        7: rpchelp.Proc('UADDR2TADDR', netbuf, [rpchelp.r_string]),
        8: rpchelp.Proc('TADDR2UADDR', rpchelp.r_string, [netbuf]),
    }

    async def NULL(self) -> client.UnpackedRPCMsg[None]:
        return await self.send_call(0, )

    async def SET(self, arg_0: rpcb) -> client.UnpackedRPCMsg[bool]:
        return await self.send_call(1, arg_0)

    async def UNSET(self, arg_0: rpcb) -> client.UnpackedRPCMsg[bool]:
        return await self.send_call(2, arg_0)

    async def GETADDR(self, arg_0: rpcb) -> client.UnpackedRPCMsg[bytes]:
        return await self.send_call(3, arg_0)

    async def DUMP(self) -> client.UnpackedRPCMsg[typing.List[typing.Union[rpcb, rp__list]]]:
        return await self.send_call(4, )

    async def CALLIT(self, arg_0: rpcb_rmtcallargs) -> client.UnpackedRPCMsg[rpcb_rmtcallres]:
        return await self.send_call(5, arg_0)

    async def GETTIME(self) -> client.UnpackedRPCMsg[int]:
        return await self.send_call(6, )

    async def UADDR2TADDR(self, arg_0: bytes) -> client.UnpackedRPCMsg[netbuf]:
        return await self.send_call(7, arg_0)

    async def TADDR2UADDR(self, arg_0: netbuf) -> client.UnpackedRPCMsg[bytes]:
        return await self.send_call(8, arg_0)


class RPCBPROG_4_CLIENT(client.BaseClient):
    prog = 100000
    vers = 4
    procs = {
        0: rpchelp.Proc('NULL', rpchelp.r_void, []),
        1: rpchelp.Proc('SET', rpchelp.r_bool, [rpcb]),
        2: rpchelp.Proc('UNSET', rpchelp.r_bool, [rpcb]),
        3: rpchelp.Proc('GETADDR', rpchelp.r_string, [rpcb]),
        4: rpchelp.Proc('DUMP', rpcblist, []),
        5: rpchelp.Proc('BCAST', rpcb_rmtcallres, [rpcb_rmtcallargs]),
        6: rpchelp.Proc('GETTIME', rpchelp.r_uint, []),
        7: rpchelp.Proc('UADDR2TADDR', netbuf, [rpchelp.r_string]),
        8: rpchelp.Proc('TADDR2UADDR', rpchelp.r_string, [netbuf]),
        9: rpchelp.Proc('GETVERSADDR', rpchelp.r_string, [rpcb]),
        10: rpchelp.Proc('INDIRECT', rpcb_rmtcallres, [rpcb_rmtcallargs]),
        11: rpchelp.Proc('GETADDRLIST', rpcb_entry_list, [rpcb]),
        12: rpchelp.Proc('GETSTAT', rpcb_stat_byvers, []),
    }

    async def NULL(self) -> client.UnpackedRPCMsg[None]:
        return await self.send_call(0, )

    async def SET(self, arg_0: rpcb) -> client.UnpackedRPCMsg[bool]:
        return await self.send_call(1, arg_0)

    async def UNSET(self, arg_0: rpcb) -> client.UnpackedRPCMsg[bool]:
        return await self.send_call(2, arg_0)

    async def GETADDR(self, arg_0: rpcb) -> client.UnpackedRPCMsg[bytes]:
        return await self.send_call(3, arg_0)

    async def DUMP(self) -> client.UnpackedRPCMsg[typing.List[typing.Union[rpcb, rp__list]]]:
        return await self.send_call(4, )

    async def BCAST(self, arg_0: rpcb_rmtcallargs) -> client.UnpackedRPCMsg[rpcb_rmtcallres]:
        return await self.send_call(5, arg_0)

    async def GETTIME(self) -> client.UnpackedRPCMsg[int]:
        return await self.send_call(6, )

    async def UADDR2TADDR(self, arg_0: bytes) -> client.UnpackedRPCMsg[netbuf]:
        return await self.send_call(7, arg_0)

    async def TADDR2UADDR(self, arg_0: netbuf) -> client.UnpackedRPCMsg[bytes]:
        return await self.send_call(8, arg_0)

    async def GETVERSADDR(self, arg_0: rpcb) -> client.UnpackedRPCMsg[bytes]:
        return await self.send_call(9, arg_0)

    async def INDIRECT(self, arg_0: rpcb_rmtcallargs) -> client.UnpackedRPCMsg[rpcb_rmtcallres]:
        return await self.send_call(10, arg_0)

    async def GETADDRLIST(self, arg_0: rpcb) -> client.UnpackedRPCMsg[typing.List[typing.Union[rpcb_entry, rpcb_entry_list]]]:
        return await self.send_call(11, arg_0)

    async def GETSTAT(self) -> client.UnpackedRPCMsg[typing.List[rpcb_stat]]:
        return await self.send_call(12, )

__all__ = ['rpcb', 'rp__list', 'rpcblist', 'rpcb_rmtcallargs', 'rpcb_rmtcallres', 'rpcb_entry', 'rpcb_entry_list', 'rpcbs_addrlist', 'rpcbs_rmtcalllist', 'rpcb_stat', 'netbuf', 'RPCBPROG_3_SERVER', 'RPCBPROG_4_SERVER', 'TRUE', 'FALSE', 'RPCB_PORT', 'rpcb_highproc_2', 'rpcb_highproc_3', 'rpcb_highproc_4', 'RPCBSTAT_HIGHPROC', 'RPCBVERS_STAT', 'RPCBVERS_4_STAT', 'RPCBVERS_3_STAT', 'RPCBVERS_2_STAT']
