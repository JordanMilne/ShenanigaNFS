# Auto-generated from IDL file
import abc
import dataclasses
import typing
from dataclasses import dataclass

from pynefs import rpchelp

TRUE = True
FALSE = False

PMAP_PORT = 111
@dataclass
class mapping(rpchelp.struct):
    prog: int = rpchelp.rpc_field(rpchelp.r_uint)
    vers: int = rpchelp.rpc_field(rpchelp.r_uint)
    prot: int = rpchelp.rpc_field(rpchelp.r_uint)
    port: int = rpchelp.rpc_field(rpchelp.r_uint)

IPPROTO_TCP = 6
IPPROTO_UDP = 17
@dataclass
class pmaplist(rpchelp.linked_list):
    map: mapping = rpchelp.rpc_field(mapping)

@dataclass
class call_args(rpchelp.struct):
    prog: int = rpchelp.rpc_field(rpchelp.r_uint)
    vers: int = rpchelp.rpc_field(rpchelp.r_uint)
    proc: int = rpchelp.rpc_field(rpchelp.r_uint)
    args: bytes = rpchelp.rpc_field(rpchelp.opaque(rpchelp.LengthType.VAR, None))

@dataclass
class call_result(rpchelp.struct):
    port: int = rpchelp.rpc_field(rpchelp.r_uint)
    res: bytes = rpchelp.rpc_field(rpchelp.opaque(rpchelp.LengthType.VAR, None))


from pynefs import client


class PMAP_PROG_2_SERVER(rpchelp.Prog):
    prog = 100000
    vers = 2
    procs = {
        0: rpchelp.Proc('NULL', rpchelp.r_void, []),
        1: rpchelp.Proc('SET', rpchelp.r_bool, [mapping]),
        2: rpchelp.Proc('UNSET', rpchelp.r_bool, [mapping]),
        3: rpchelp.Proc('GETPORT', rpchelp.r_uint, [mapping]),
        4: rpchelp.Proc('DUMP', pmaplist, []),
        5: rpchelp.Proc('CALLIT', call_result, [call_args]),
    }

    @abc.abstractmethod
    def NULL(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def SET(self, arg_0: mapping) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def UNSET(self, arg_0: mapping) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def GETPORT(self, arg_0: mapping) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    def DUMP(self) -> typing.List[typing.Union[mapping, pmaplist]]:
        raise NotImplementedError()

    @abc.abstractmethod
    def CALLIT(self, arg_0: call_args) -> call_result:
        raise NotImplementedError()


class PMAP_PROG_2_CLIENT(client.BaseClient):
    prog = 100000
    vers = 2
    procs = {
        0: rpchelp.Proc('NULL', rpchelp.r_void, []),
        1: rpchelp.Proc('SET', rpchelp.r_bool, [mapping]),
        2: rpchelp.Proc('UNSET', rpchelp.r_bool, [mapping]),
        3: rpchelp.Proc('GETPORT', rpchelp.r_uint, [mapping]),
        4: rpchelp.Proc('DUMP', pmaplist, []),
        5: rpchelp.Proc('CALLIT', call_result, [call_args]),
    }

    async def NULL(self) -> client.UnpackedRPCMsg[None]:
        return await self.send_call(0, )

    async def SET(self, arg_0: mapping) -> client.UnpackedRPCMsg[bool]:
        return await self.send_call(1, arg_0)

    async def UNSET(self, arg_0: mapping) -> client.UnpackedRPCMsg[bool]:
        return await self.send_call(2, arg_0)

    async def GETPORT(self, arg_0: mapping) -> client.UnpackedRPCMsg[int]:
        return await self.send_call(3, arg_0)

    async def DUMP(self) -> client.UnpackedRPCMsg[typing.List[typing.Union[mapping, pmaplist]]]:
        return await self.send_call(4, )

    async def CALLIT(self, arg_0: call_args) -> client.UnpackedRPCMsg[call_result]:
        return await self.send_call(5, arg_0)

__all__ = ['mapping', 'pmaplist', 'call_args', 'call_result', 'PMAP_PROG_2_SERVER', 'TRUE', 'FALSE', 'PMAP_PORT', 'IPPROTO_TCP', 'IPPROTO_UDP']
