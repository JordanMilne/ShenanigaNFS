# Auto-generated from IDL file
import abc
import dataclasses
import typing
from dataclasses import dataclass

from shenaniganfs import rpchelp

TRUE = True
FALSE = False

RPCB_PORT = 111


@dataclass
class RPCB(rpchelp.Struct):  # rpcb
    r_prog: int = rpchelp.rpc_field(rpchelp.r_uint)
    r_vers: int = rpchelp.rpc_field(rpchelp.r_uint)
    r_netid: bytes = rpchelp.rpc_field(rpchelp.Opaque(rpchelp.LengthType.VAR, None))
    r_addr: bytes = rpchelp.rpc_field(rpchelp.Opaque(rpchelp.LengthType.VAR, None))
    r_owner: bytes = rpchelp.rpc_field(rpchelp.Opaque(rpchelp.LengthType.VAR, None))


@dataclass
class RpList(rpchelp.LinkedList):  # rp__list
    rpcb_map: RPCB = rpchelp.rpc_field(RPCB)


RPCBList = RpList


@dataclass
class RPCBRmtcallArgs(rpchelp.Struct):  # rpcb_rmtcallargs
    prog: int = rpchelp.rpc_field(rpchelp.r_uint)
    vers: int = rpchelp.rpc_field(rpchelp.r_uint)
    proc: int = rpchelp.rpc_field(rpchelp.r_uint)
    args: bytes = rpchelp.rpc_field(rpchelp.Opaque(rpchelp.LengthType.VAR, None))


@dataclass
class RPCBRmtcallRes(rpchelp.Struct):  # rpcb_rmtcallres
    addr: bytes = rpchelp.rpc_field(rpchelp.Opaque(rpchelp.LengthType.VAR, None))
    results: bytes = rpchelp.rpc_field(rpchelp.Opaque(rpchelp.LengthType.VAR, None))


@dataclass
class RPCBEntry(rpchelp.Struct):  # rpcb_entry
    r_maddr: bytes = rpchelp.rpc_field(rpchelp.Opaque(rpchelp.LengthType.VAR, None))
    r_nc_netid: bytes = rpchelp.rpc_field(rpchelp.Opaque(rpchelp.LengthType.VAR, None))
    r_nc_semantics: int = rpchelp.rpc_field(rpchelp.r_uint)
    r_nc_protofmly: bytes = rpchelp.rpc_field(rpchelp.Opaque(rpchelp.LengthType.VAR, None))
    r_nc_proto: bytes = rpchelp.rpc_field(rpchelp.Opaque(rpchelp.LengthType.VAR, None))


@dataclass
class RPCBEntryList(rpchelp.LinkedList):  # rpcb_entry_list
    rpcb_entry_map: RPCBEntry = rpchelp.rpc_field(RPCBEntry)


RPCBHighproc2 = 5
RPCBHighproc3 = 8
RPCBHighproc4 = 12
RPCBSTAT_HIGHPROC = 13
RPCBVERS_STAT = 3
RPCBVERS_4_STAT = 2
RPCBVERS_3_STAT = 1
RPCBVERS_2_STAT = 0


@dataclass
class RPCBsAddrList(rpchelp.LinkedList):  # rpcbs_addrlist
    prog: int = rpchelp.rpc_field(rpchelp.r_uint)
    vers: int = rpchelp.rpc_field(rpchelp.r_uint)
    success: int = rpchelp.rpc_field(rpchelp.r_int)
    failure: int = rpchelp.rpc_field(rpchelp.r_int)
    netid: bytes = rpchelp.rpc_field(rpchelp.Opaque(rpchelp.LengthType.VAR, None))


@dataclass
class RPCBsRmtcallList(rpchelp.LinkedList):  # rpcbs_rmtcalllist
    prog: int = rpchelp.rpc_field(rpchelp.r_uint)
    vers: int = rpchelp.rpc_field(rpchelp.r_uint)
    proc: int = rpchelp.rpc_field(rpchelp.r_uint)
    success: int = rpchelp.rpc_field(rpchelp.r_int)
    failure: int = rpchelp.rpc_field(rpchelp.r_int)
    indirect: int = rpchelp.rpc_field(rpchelp.r_int)
    netid: bytes = rpchelp.rpc_field(rpchelp.Opaque(rpchelp.LengthType.VAR, None))


RPCBsProc = rpchelp.Array(rpchelp.r_int, rpchelp.LengthType.FIXED, RPCBSTAT_HIGHPROC)


@dataclass
class RPCBStat(rpchelp.Struct):  # rpcb_stat
    info: typing.List[int] = rpchelp.rpc_field(RPCBsProc)
    setinfo: int = rpchelp.rpc_field(rpchelp.r_int)
    unsetinfo: int = rpchelp.rpc_field(rpchelp.r_int)
    addrinfo: typing.List[RPCBsAddrList] = rpchelp.rpc_field(rpchelp.OptData(RPCBsAddrList))
    rmtinfo: typing.List[RPCBsRmtcallList] = rpchelp.rpc_field(rpchelp.OptData(RPCBsRmtcallList))


RPCBStatByvers = rpchelp.Array(RPCBStat, rpchelp.LengthType.FIXED, RPCBVERS_STAT)


@dataclass
class Netbuf(rpchelp.Struct):  # netbuf
    maxlen: int = rpchelp.rpc_field(rpchelp.r_uint)
    buf: bytes = rpchelp.rpc_field(rpchelp.Opaque(rpchelp.LengthType.VAR, None))


from shenaniganfs import client


class RPCBPROG_3_SERVER(rpchelp.Prog):
    prog = 100000
    vers = 3
    procs = {
        0: rpchelp.Proc('NULL', rpchelp.r_void, []),
        1: rpchelp.Proc('SET', rpchelp.r_bool, [RPCB]),
        2: rpchelp.Proc('UNSET', rpchelp.r_bool, [RPCB]),
        3: rpchelp.Proc('GETADDR', rpchelp.r_string, [RPCB]),
        4: rpchelp.Proc('DUMP', RPCBList, []),
        5: rpchelp.Proc('CALLIT', RPCBRmtcallRes, [RPCBRmtcallArgs]),
        6: rpchelp.Proc('GETTIME', rpchelp.r_uint, []),
        7: rpchelp.Proc('UADDR2TADDR', Netbuf, [rpchelp.r_string]),
        8: rpchelp.Proc('TADDR2UADDR', rpchelp.r_string, [Netbuf]),
    }

    @abc.abstractmethod
    async def NULL(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def SET(self, arg_0: RPCB) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    async def UNSET(self, arg_0: RPCB) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    async def GETADDR(self, arg_0: RPCB) -> bytes:
        raise NotImplementedError()

    @abc.abstractmethod
    async def DUMP(self) -> typing.List[RPCB]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def CALLIT(self, arg_0: RPCBRmtcallArgs) -> RPCBRmtcallRes:
        raise NotImplementedError()

    @abc.abstractmethod
    async def GETTIME(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def UADDR2TADDR(self, arg_0: bytes) -> Netbuf:
        raise NotImplementedError()

    @abc.abstractmethod
    async def TADDR2UADDR(self, arg_0: Netbuf) -> bytes:
        raise NotImplementedError()


class RPCBPROG_4_SERVER(rpchelp.Prog):
    prog = 100000
    vers = 4
    procs = {
        0: rpchelp.Proc('NULL', rpchelp.r_void, []),
        1: rpchelp.Proc('SET', rpchelp.r_bool, [RPCB]),
        2: rpchelp.Proc('UNSET', rpchelp.r_bool, [RPCB]),
        3: rpchelp.Proc('GETADDR', rpchelp.r_string, [RPCB]),
        4: rpchelp.Proc('DUMP', RPCBList, []),
        5: rpchelp.Proc('BCAST', RPCBRmtcallRes, [RPCBRmtcallArgs]),
        6: rpchelp.Proc('GETTIME', rpchelp.r_uint, []),
        7: rpchelp.Proc('UADDR2TADDR', Netbuf, [rpchelp.r_string]),
        8: rpchelp.Proc('TADDR2UADDR', rpchelp.r_string, [Netbuf]),
        9: rpchelp.Proc('GETVERSADDR', rpchelp.r_string, [RPCB]),
        10: rpchelp.Proc('INDIRECT', RPCBRmtcallRes, [RPCBRmtcallArgs]),
        11: rpchelp.Proc('GETADDRLIST', RPCBEntryList, [RPCB]),
        12: rpchelp.Proc('GETSTAT', RPCBStatByvers, []),
    }

    @abc.abstractmethod
    async def NULL(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def SET(self, arg_0: RPCB) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    async def UNSET(self, arg_0: RPCB) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    async def GETADDR(self, arg_0: RPCB) -> bytes:
        raise NotImplementedError()

    @abc.abstractmethod
    async def DUMP(self) -> typing.List[RPCB]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def BCAST(self, arg_0: RPCBRmtcallArgs) -> RPCBRmtcallRes:
        raise NotImplementedError()

    @abc.abstractmethod
    async def GETTIME(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def UADDR2TADDR(self, arg_0: bytes) -> Netbuf:
        raise NotImplementedError()

    @abc.abstractmethod
    async def TADDR2UADDR(self, arg_0: Netbuf) -> bytes:
        raise NotImplementedError()

    @abc.abstractmethod
    async def GETVERSADDR(self, arg_0: RPCB) -> bytes:
        raise NotImplementedError()

    @abc.abstractmethod
    async def INDIRECT(self, arg_0: RPCBRmtcallArgs) -> RPCBRmtcallRes:
        raise NotImplementedError()

    @abc.abstractmethod
    async def GETADDRLIST(self, arg_0: RPCB) -> typing.List[RPCBEntry]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def GETSTAT(self) -> typing.List[RPCBStat]:
        raise NotImplementedError()


class RPCBPROG_3_CLIENT(client.BaseClient):
    prog = 100000
    vers = 3
    procs = {
        0: rpchelp.Proc('NULL', rpchelp.r_void, []),
        1: rpchelp.Proc('SET', rpchelp.r_bool, [RPCB]),
        2: rpchelp.Proc('UNSET', rpchelp.r_bool, [RPCB]),
        3: rpchelp.Proc('GETADDR', rpchelp.r_string, [RPCB]),
        4: rpchelp.Proc('DUMP', RPCBList, []),
        5: rpchelp.Proc('CALLIT', RPCBRmtcallRes, [RPCBRmtcallArgs]),
        6: rpchelp.Proc('GETTIME', rpchelp.r_uint, []),
        7: rpchelp.Proc('UADDR2TADDR', Netbuf, [rpchelp.r_string]),
        8: rpchelp.Proc('TADDR2UADDR', rpchelp.r_string, [Netbuf]),
    }

    async def NULL(self) -> client.UnpackedRPCMsg[None]:
        return await self.send_call(0, )

    async def SET(self, arg_0: RPCB) -> client.UnpackedRPCMsg[bool]:
        return await self.send_call(1, arg_0)

    async def UNSET(self, arg_0: RPCB) -> client.UnpackedRPCMsg[bool]:
        return await self.send_call(2, arg_0)

    async def GETADDR(self, arg_0: RPCB) -> client.UnpackedRPCMsg[bytes]:
        return await self.send_call(3, arg_0)

    async def DUMP(self) -> client.UnpackedRPCMsg[typing.List[RPCB]]:
        return await self.send_call(4, )

    async def CALLIT(self, arg_0: RPCBRmtcallArgs) -> client.UnpackedRPCMsg[RPCBRmtcallRes]:
        return await self.send_call(5, arg_0)

    async def GETTIME(self) -> client.UnpackedRPCMsg[int]:
        return await self.send_call(6, )

    async def UADDR2TADDR(self, arg_0: bytes) -> client.UnpackedRPCMsg[Netbuf]:
        return await self.send_call(7, arg_0)

    async def TADDR2UADDR(self, arg_0: Netbuf) -> client.UnpackedRPCMsg[bytes]:
        return await self.send_call(8, arg_0)


class RPCBPROG_4_CLIENT(client.BaseClient):
    prog = 100000
    vers = 4
    procs = {
        0: rpchelp.Proc('NULL', rpchelp.r_void, []),
        1: rpchelp.Proc('SET', rpchelp.r_bool, [RPCB]),
        2: rpchelp.Proc('UNSET', rpchelp.r_bool, [RPCB]),
        3: rpchelp.Proc('GETADDR', rpchelp.r_string, [RPCB]),
        4: rpchelp.Proc('DUMP', RPCBList, []),
        5: rpchelp.Proc('BCAST', RPCBRmtcallRes, [RPCBRmtcallArgs]),
        6: rpchelp.Proc('GETTIME', rpchelp.r_uint, []),
        7: rpchelp.Proc('UADDR2TADDR', Netbuf, [rpchelp.r_string]),
        8: rpchelp.Proc('TADDR2UADDR', rpchelp.r_string, [Netbuf]),
        9: rpchelp.Proc('GETVERSADDR', rpchelp.r_string, [RPCB]),
        10: rpchelp.Proc('INDIRECT', RPCBRmtcallRes, [RPCBRmtcallArgs]),
        11: rpchelp.Proc('GETADDRLIST', RPCBEntryList, [RPCB]),
        12: rpchelp.Proc('GETSTAT', RPCBStatByvers, []),
    }

    async def NULL(self) -> client.UnpackedRPCMsg[None]:
        return await self.send_call(0, )

    async def SET(self, arg_0: RPCB) -> client.UnpackedRPCMsg[bool]:
        return await self.send_call(1, arg_0)

    async def UNSET(self, arg_0: RPCB) -> client.UnpackedRPCMsg[bool]:
        return await self.send_call(2, arg_0)

    async def GETADDR(self, arg_0: RPCB) -> client.UnpackedRPCMsg[bytes]:
        return await self.send_call(3, arg_0)

    async def DUMP(self) -> client.UnpackedRPCMsg[typing.List[RPCB]]:
        return await self.send_call(4, )

    async def BCAST(self, arg_0: RPCBRmtcallArgs) -> client.UnpackedRPCMsg[RPCBRmtcallRes]:
        return await self.send_call(5, arg_0)

    async def GETTIME(self) -> client.UnpackedRPCMsg[int]:
        return await self.send_call(6, )

    async def UADDR2TADDR(self, arg_0: bytes) -> client.UnpackedRPCMsg[Netbuf]:
        return await self.send_call(7, arg_0)

    async def TADDR2UADDR(self, arg_0: Netbuf) -> client.UnpackedRPCMsg[bytes]:
        return await self.send_call(8, arg_0)

    async def GETVERSADDR(self, arg_0: RPCB) -> client.UnpackedRPCMsg[bytes]:
        return await self.send_call(9, arg_0)

    async def INDIRECT(self, arg_0: RPCBRmtcallArgs) -> client.UnpackedRPCMsg[RPCBRmtcallRes]:
        return await self.send_call(10, arg_0)

    async def GETADDRLIST(self, arg_0: RPCB) -> client.UnpackedRPCMsg[typing.List[RPCBEntry]]:
        return await self.send_call(11, arg_0)

    async def GETSTAT(self) -> client.UnpackedRPCMsg[typing.List[RPCBStat]]:
        return await self.send_call(12, )


__all__ = ['RPCBPROG_3_SERVER', 'RPCBPROG_3_CLIENT', 'RPCBPROG_4_SERVER', 'RPCBPROG_4_CLIENT', 'TRUE', 'FALSE', 'RPCB_PORT', 'RPCBHighproc2', 'RPCBHighproc3', 'RPCBHighproc4', 'RPCBSTAT_HIGHPROC', 'RPCBVERS_STAT', 'RPCBVERS_4_STAT', 'RPCBVERS_3_STAT', 'RPCBVERS_2_STAT', 'RPCB', 'RpList', 'RPCBList', 'RPCBRmtcallArgs', 'RPCBRmtcallRes', 'RPCBEntry', 'RPCBEntryList', 'RPCBsAddrList', 'RPCBsRmtcallList', 'RPCBsProc', 'RPCBStat', 'RPCBStatByvers', 'Netbuf']
