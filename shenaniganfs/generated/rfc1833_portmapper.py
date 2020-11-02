# Auto-generated from IDL file
import abc
import dataclasses
import typing
from dataclasses import dataclass

from shenaniganfs import rpchelp

TRUE = True
FALSE = False

PMAP_PORT = 111


@dataclass
class Mapping(rpchelp.Struct):  # mapping
    prog: int = rpchelp.rpc_field(rpchelp.r_uint)
    vers: int = rpchelp.rpc_field(rpchelp.r_uint)
    prot: int = rpchelp.rpc_field(rpchelp.r_uint)
    port: int = rpchelp.rpc_field(rpchelp.r_uint)


IPPROTO_TCP = 6
IPPROTO_UDP = 17


@dataclass
class PmapList(rpchelp.LinkedList):  # pmaplist
    map: Mapping = rpchelp.rpc_field(Mapping)


@dataclass
class CallArgs(rpchelp.Struct):  # call_args
    prog: int = rpchelp.rpc_field(rpchelp.r_uint)
    vers: int = rpchelp.rpc_field(rpchelp.r_uint)
    proc: int = rpchelp.rpc_field(rpchelp.r_uint)
    args: bytes = rpchelp.rpc_field(rpchelp.Opaque(rpchelp.LengthType.VAR, None))


@dataclass
class CallResult(rpchelp.Struct):  # call_result
    port: int = rpchelp.rpc_field(rpchelp.r_uint)
    res: bytes = rpchelp.rpc_field(rpchelp.Opaque(rpchelp.LengthType.VAR, None))


from shenaniganfs import client


class PMAP_PROG_2_SERVER(rpchelp.Prog):
    prog = 100000
    vers = 2
    procs = {
        0: rpchelp.Proc('NULL', rpchelp.r_void, []),
        1: rpchelp.Proc('SET', rpchelp.r_bool, [Mapping]),
        2: rpchelp.Proc('UNSET', rpchelp.r_bool, [Mapping]),
        3: rpchelp.Proc('GETPORT', rpchelp.r_uint, [Mapping]),
        4: rpchelp.Proc('DUMP', PmapList, []),
        5: rpchelp.Proc('CALLIT', CallResult, [CallArgs]),
    }

    @abc.abstractmethod
    async def NULL(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def SET(self, arg_0: Mapping) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    async def UNSET(self, arg_0: Mapping) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    async def GETPORT(self, arg_0: Mapping) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def DUMP(self) -> typing.List[Mapping]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def CALLIT(self, arg_0: CallArgs) -> CallResult:
        raise NotImplementedError()


class PMAP_PROG_2_CLIENT(client.BaseClient):
    prog = 100000
    vers = 2
    procs = {
        0: rpchelp.Proc('NULL', rpchelp.r_void, []),
        1: rpchelp.Proc('SET', rpchelp.r_bool, [Mapping]),
        2: rpchelp.Proc('UNSET', rpchelp.r_bool, [Mapping]),
        3: rpchelp.Proc('GETPORT', rpchelp.r_uint, [Mapping]),
        4: rpchelp.Proc('DUMP', PmapList, []),
        5: rpchelp.Proc('CALLIT', CallResult, [CallArgs]),
    }

    async def NULL(self) -> client.UnpackedRPCMsg[None]:
        return await self.send_call(0, )

    async def SET(self, arg_0: Mapping) -> client.UnpackedRPCMsg[bool]:
        return await self.send_call(1, arg_0)

    async def UNSET(self, arg_0: Mapping) -> client.UnpackedRPCMsg[bool]:
        return await self.send_call(2, arg_0)

    async def GETPORT(self, arg_0: Mapping) -> client.UnpackedRPCMsg[int]:
        return await self.send_call(3, arg_0)

    async def DUMP(self) -> client.UnpackedRPCMsg[typing.List[Mapping]]:
        return await self.send_call(4, )

    async def CALLIT(self, arg_0: CallArgs) -> client.UnpackedRPCMsg[CallResult]:
        return await self.send_call(5, arg_0)


__all__ = ['PMAP_PROG_2_SERVER', 'PMAP_PROG_2_CLIENT', 'TRUE', 'FALSE', 'PMAP_PORT', 'IPPROTO_TCP', 'IPPROTO_UDP', 'Mapping', 'PmapList', 'CallArgs', 'CallResult']
