"""
A statd stub so that new versions of macOS can connect without extra options,
see https://github.com/apple/darwin-xnu/blob/2ff845c2e033bd0ff64b5b6aa6063a1f8f65aa32/bsd/nfs/nfs_vfsops.c#L4622-L4655

Previously mount on macOS was hanging unless an option was passed to mount without locks.
"""

from shenaniganfs import transport
from shenaniganfs.generated.statd import *


class StatDV1Server(SM_PROG_1_SERVER):
    async def NULL(self, call_ctx: transport.CallContext) -> transport.ProcRet[None]:
        pass

    async def STAT(self, call_ctx: transport.CallContext, arg_0: SmName) -> transport.ProcRet[SmStatRes]:
        # Just say fail no matter what
        return SmStatRes(
            res_stat=Res.stat_fail,
            state=0,
        )

    async def MON(self, call_ctx: transport.CallContext, arg_0: Mon) -> transport.ProcRet[SmStatRes]:
        raise NotImplementedError()

    async def UNMON(self, call_ctx: transport.CallContext, arg_0: MonId) -> transport.ProcRet[SmStat]:
        raise NotImplementedError()

    async def UNMON_ALL(self, call_ctx: transport.CallContext, arg_0: MyId) -> transport.ProcRet[SmStat]:
        raise NotImplementedError()

    async def SIMU_CRASH(self, call_ctx: transport.CallContext) -> transport.ProcRet[None]:
        raise NotImplementedError()

    async def NOTIFY(self, call_ctx: transport.CallContext, arg_0: StatChge) -> transport.ProcRet[None]:
        raise NotImplementedError()
