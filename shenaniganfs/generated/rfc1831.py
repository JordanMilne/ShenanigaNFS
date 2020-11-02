# Auto-generated from IDL file
import abc
import dataclasses
import typing
from dataclasses import dataclass

from shenaniganfs import rpchelp

TRUE = True
FALSE = False
AUTH_NONE = 0
AUTH_SYS = 1
AUTH_SHORT = 2
CALL = 0
REPLY = 1
MSG_ACCEPTED = 0
MSG_DENIED = 1
SUCCESS = 0
PROG_UNAVAIL = 1
PROG_MISMATCH = 2
PROC_UNAVAIL = 3
GARBAGE_ARGS = 4
SYSTEM_ERR = 5
RPC_MISMATCH = 0
AUTH_ERROR = 1
AUTH_OK = 0
AUTH_BADCRED = 1
AUTH_REJECTEDCRED = 2
AUTH_BADVERF = 3
AUTH_REJECTEDVERF = 4
AUTH_TOOWEAK = 5
AUTH_INVALIDRESP = 6
AUTH_FAILED = 7


class AuthFlavor(rpchelp.Enum):  # auth_flavor
    AUTH_NONE = 0
    AUTH_SYS = 1
    AUTH_SHORT = 2


@dataclass
class OpaqueAuth(rpchelp.Struct):  # opaque_auth
    flavor: typing.Union[AuthFlavor, int] = rpchelp.rpc_field(AuthFlavor)
    body: bytes = rpchelp.rpc_field(rpchelp.Opaque(rpchelp.LengthType.VAR, 400))


@dataclass
class AuthsysParms(rpchelp.Struct):  # authsys_parms
    stamp: int = rpchelp.rpc_field(rpchelp.r_uint)
    machinename: bytes = rpchelp.rpc_field(rpchelp.Opaque(rpchelp.LengthType.VAR, 255))
    uid: int = rpchelp.rpc_field(rpchelp.r_uint)
    gid: int = rpchelp.rpc_field(rpchelp.r_uint)
    gids: typing.List[int] = rpchelp.rpc_field(rpchelp.Array(rpchelp.r_uint, rpchelp.LengthType.VAR, 16))


class MsgType(rpchelp.Enum):  # msg_type
    CALL = 0
    REPLY = 1


class ReplyStat(rpchelp.Enum):  # reply_stat
    MSG_ACCEPTED = 0
    MSG_DENIED = 1


class AcceptStat(rpchelp.Enum):  # accept_stat
    SUCCESS = 0
    PROG_UNAVAIL = 1
    PROG_MISMATCH = 2
    PROC_UNAVAIL = 3
    GARBAGE_ARGS = 4
    SYSTEM_ERR = 5


class RejectStat(rpchelp.Enum):  # reject_stat
    RPC_MISMATCH = 0
    AUTH_ERROR = 1


class AuthStat(rpchelp.Enum):  # auth_stat
    AUTH_OK = 0
    AUTH_BADCRED = 1
    AUTH_REJECTEDCRED = 2
    AUTH_BADVERF = 3
    AUTH_REJECTEDVERF = 4
    AUTH_TOOWEAK = 5
    AUTH_INVALIDRESP = 6
    AUTH_FAILED = 7


@dataclass
class CallBody(rpchelp.Struct):  # call_body
    rpcvers: int = rpchelp.rpc_field(rpchelp.r_uint)
    prog: int = rpchelp.rpc_field(rpchelp.r_uint)
    vers: int = rpchelp.rpc_field(rpchelp.r_uint)
    proc: int = rpchelp.rpc_field(rpchelp.r_uint)
    cred: OpaqueAuth = rpchelp.rpc_field(OpaqueAuth)
    verf: OpaqueAuth = rpchelp.rpc_field(OpaqueAuth)


@dataclass
class MismatchInfo(rpchelp.Struct):  # mismatch_info
    low: int = rpchelp.rpc_field(rpchelp.r_uint)
    high: int = rpchelp.rpc_field(rpchelp.r_uint)


@dataclass
class ReplyData(rpchelp.Union):  # reply_data
    SWITCH_OPTIONS = {SUCCESS: None, None: None, PROG_MISMATCH: 'mismatch'}
    stat: typing.Union[AcceptStat, int] = rpchelp.rpc_field(AcceptStat)
    mismatch: typing.Optional[MismatchInfo] = rpchelp.rpc_field(MismatchInfo, default=None)


@dataclass
class AcceptedReply(rpchelp.Struct):  # accepted_reply
    verf: OpaqueAuth = rpchelp.rpc_field(OpaqueAuth)
    data: ReplyData = rpchelp.rpc_field(ReplyData)


@dataclass
class MismatchInfo(rpchelp.Struct):  # mismatch_info
    low: int = rpchelp.rpc_field(rpchelp.r_uint)
    high: int = rpchelp.rpc_field(rpchelp.r_uint)


@dataclass
class RejectedReply(rpchelp.Union):  # rejected_reply
    SWITCH_OPTIONS = {AUTH_ERROR: 'auth_error', RPC_MISMATCH: 'mismatch_info'}
    r_stat: typing.Union[RejectStat, int] = rpchelp.rpc_field(RejectStat)
    auth_error: typing.Optional[typing.Union[AuthStat, int]] = rpchelp.rpc_field(AuthStat, default=None)
    mismatch_info: typing.Optional[MismatchInfo] = rpchelp.rpc_field(MismatchInfo, default=None)


@dataclass
class ReplyBody(rpchelp.Union):  # reply_body
    SWITCH_OPTIONS = {MSG_ACCEPTED: 'areply', MSG_DENIED: 'rreply'}
    stat: typing.Union[ReplyStat, int] = rpchelp.rpc_field(ReplyStat)
    areply: typing.Optional[AcceptedReply] = rpchelp.rpc_field(AcceptedReply, default=None)
    rreply: typing.Optional[RejectedReply] = rpchelp.rpc_field(RejectedReply, default=None)


@dataclass
class RPCBody(rpchelp.Union):  # rpc_body
    SWITCH_OPTIONS = {CALL: 'cbody', REPLY: 'rbody'}
    mtype: typing.Union[MsgType, int] = rpchelp.rpc_field(MsgType)
    cbody: typing.Optional[CallBody] = rpchelp.rpc_field(CallBody, default=None)
    rbody: typing.Optional[ReplyBody] = rpchelp.rpc_field(ReplyBody, default=None)


@dataclass
class RPCMsg(rpchelp.Struct):  # rpc_msg
    xid: int = rpchelp.rpc_field(rpchelp.r_uint)
    header: RPCBody = rpchelp.rpc_field(RPCBody)


__all__ = ['TRUE', 'FALSE', 'AUTH_NONE', 'AUTH_SYS', 'AUTH_SHORT', 'CALL', 'REPLY', 'MSG_ACCEPTED', 'MSG_DENIED', 'SUCCESS', 'PROG_UNAVAIL', 'PROG_MISMATCH', 'PROC_UNAVAIL', 'GARBAGE_ARGS', 'SYSTEM_ERR', 'RPC_MISMATCH', 'AUTH_ERROR', 'AUTH_OK', 'AUTH_BADCRED', 'AUTH_REJECTEDCRED', 'AUTH_BADVERF', 'AUTH_REJECTEDVERF', 'AUTH_TOOWEAK', 'AUTH_INVALIDRESP', 'AUTH_FAILED', 'AuthFlavor', 'OpaqueAuth', 'AuthsysParms', 'MsgType', 'ReplyStat', 'AcceptStat', 'RejectStat', 'AuthStat', 'CallBody', 'MismatchInfo', 'ReplyData', 'AcceptedReply', 'RejectedReply', 'ReplyBody', 'RPCBody', 'RPCMsg']
