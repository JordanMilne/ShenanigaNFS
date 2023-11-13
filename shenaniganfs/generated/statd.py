# Auto-generated from IDL file
import abc
import dataclasses
import typing
from dataclasses import dataclass

from shenaniganfs import rpchelp

TRUE = True
FALSE = False
stat_succ = 0
stat_fail = 1
SM_MAXSTRLEN = 1024
SM_PRIV_SIZE = 16


@dataclass
class SmName(rpchelp.Struct):  # sm_name
    mon_name: bytes = rpchelp.rpc_field(rpchelp.Opaque(rpchelp.LengthType.VAR, SM_MAXSTRLEN))


@dataclass
class MyId(rpchelp.Struct):  # my_id
    my_name: bytes = rpchelp.rpc_field(rpchelp.Opaque(rpchelp.LengthType.VAR, SM_MAXSTRLEN))
    my_prog: int = rpchelp.rpc_field(rpchelp.r_int)
    my_vers: int = rpchelp.rpc_field(rpchelp.r_int)
    my_proc: int = rpchelp.rpc_field(rpchelp.r_int)


@dataclass
class MonId(rpchelp.Struct):  # mon_id
    mon_name: bytes = rpchelp.rpc_field(rpchelp.Opaque(rpchelp.LengthType.VAR, SM_MAXSTRLEN))
    my_id: MyId = rpchelp.rpc_field(MyId)


@dataclass
class Mon(rpchelp.Struct):  # mon
    mon_id: MonId = rpchelp.rpc_field(MonId)
    priv: bytes = rpchelp.rpc_field(rpchelp.Opaque(rpchelp.LengthType.FIXED, SM_PRIV_SIZE))


@dataclass
class StatChge(rpchelp.Struct):  # stat_chge
    mon_name: bytes = rpchelp.rpc_field(rpchelp.Opaque(rpchelp.LengthType.VAR, SM_MAXSTRLEN))
    state: int = rpchelp.rpc_field(rpchelp.r_int)


@dataclass
class SmStat(rpchelp.Struct):  # sm_stat
    state: int = rpchelp.rpc_field(rpchelp.r_int)


class Res(rpchelp.Enum):  # res
    stat_succ = 0
    stat_fail = 1


@dataclass
class SmStatRes(rpchelp.Struct):  # sm_stat_res
    res_stat: typing.Union[Res, int] = rpchelp.rpc_field(Res)
    state: int = rpchelp.rpc_field(rpchelp.r_int)


@dataclass
class Status(rpchelp.Struct):  # status
    mon_name: bytes = rpchelp.rpc_field(rpchelp.Opaque(rpchelp.LengthType.VAR, SM_MAXSTRLEN))
    state: int = rpchelp.rpc_field(rpchelp.r_int)
    priv: bytes = rpchelp.rpc_field(rpchelp.Opaque(rpchelp.LengthType.FIXED, SM_PRIV_SIZE))


from shenaniganfs import client, transport


class SM_PROG_1_SERVER(transport.Prog):
    prog = 100024
    vers = 1
    procs = {
        0: rpchelp.Proc('NULL', rpchelp.r_void, []),
        1: rpchelp.Proc('STAT', SmStatRes, [SmName]),
        2: rpchelp.Proc('MON', SmStatRes, [Mon]),
        3: rpchelp.Proc('UNMON', SmStat, [MonId]),
        4: rpchelp.Proc('UNMON_ALL', SmStat, [MyId]),
        5: rpchelp.Proc('SIMU_CRASH', rpchelp.r_void, []),
        6: rpchelp.Proc('NOTIFY', rpchelp.r_void, [StatChge]),
    }

    @abc.abstractmethod
    async def NULL(self, call_ctx: transport.CallContext) \
            -> transport.ProcRet[None]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def STAT(self, call_ctx: transport.CallContext, arg_0: SmName) \
            -> transport.ProcRet[SmStatRes]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def MON(self, call_ctx: transport.CallContext, arg_0: Mon) \
            -> transport.ProcRet[SmStatRes]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def UNMON(self, call_ctx: transport.CallContext, arg_0: MonId) \
            -> transport.ProcRet[SmStat]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def UNMON_ALL(self, call_ctx: transport.CallContext, arg_0: MyId) \
            -> transport.ProcRet[SmStat]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def SIMU_CRASH(self, call_ctx: transport.CallContext) \
            -> transport.ProcRet[None]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def NOTIFY(self, call_ctx: transport.CallContext, arg_0: StatChge) \
            -> transport.ProcRet[None]:
        raise NotImplementedError()


class SM_PROG_1_CLIENT(client.BaseClient):
    prog = 100024
    vers = 1
    procs = {
        0: rpchelp.Proc('NULL', rpchelp.r_void, []),
        1: rpchelp.Proc('STAT', SmStatRes, [SmName]),
        2: rpchelp.Proc('MON', SmStatRes, [Mon]),
        3: rpchelp.Proc('UNMON', SmStat, [MonId]),
        4: rpchelp.Proc('UNMON_ALL', SmStat, [MyId]),
        5: rpchelp.Proc('SIMU_CRASH', rpchelp.r_void, []),
        6: rpchelp.Proc('NOTIFY', rpchelp.r_void, [StatChge]),
    }

    async def NULL(self) -> client.UnpackedRPCMsg[None]:
        return await self.send_call(0, )

    async def STAT(self, arg_0: SmName) -> client.UnpackedRPCMsg[SmStatRes]:
        return await self.send_call(1, arg_0)

    async def MON(self, arg_0: Mon) -> client.UnpackedRPCMsg[SmStatRes]:
        return await self.send_call(2, arg_0)

    async def UNMON(self, arg_0: MonId) -> client.UnpackedRPCMsg[SmStat]:
        return await self.send_call(3, arg_0)

    async def UNMON_ALL(self, arg_0: MyId) -> client.UnpackedRPCMsg[SmStat]:
        return await self.send_call(4, arg_0)

    async def SIMU_CRASH(self) -> client.UnpackedRPCMsg[None]:
        return await self.send_call(5, )

    async def NOTIFY(self, arg_0: StatChge) -> client.UnpackedRPCMsg[None]:
        return await self.send_call(6, arg_0)


__all__ = ['SM_PROG_1_SERVER', 'SM_PROG_1_CLIENT', 'TRUE', 'FALSE', 'SM_MAXSTRLEN', 'SM_PRIV_SIZE', 'stat_succ', 'stat_fail', 'SmName', 'MyId', 'MonId', 'Mon', 'StatChge', 'SmStat', 'Res', 'SmStatRes', 'Status']
