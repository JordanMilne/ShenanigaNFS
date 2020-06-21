# Auto-generated from IDL file
import abc
import dataclasses
import typing
from dataclasses import dataclass

from pynefs import rpchelp

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


class auth_flavor(rpchelp.enum):
    AUTH_NONE = 0
    AUTH_SYS = 1
    AUTH_SHORT = 2


@dataclass
class opaque_auth(rpchelp.struct):
    flavor: auth_flavor = rpchelp.rpc_field(auth_flavor)
    body: bytes = rpchelp.rpc_field(rpchelp.opaque(rpchelp.LengthType.VAR, 400))


@dataclass
class authsys_parms(rpchelp.struct):
    stamp: int = rpchelp.rpc_field(rpchelp.r_uint)
    machinename: bytes = rpchelp.rpc_field(rpchelp.string(rpchelp.LengthType.VAR, 255))
    uid: int = rpchelp.rpc_field(rpchelp.r_uint)
    gid: int = rpchelp.rpc_field(rpchelp.r_uint)
    gids: typing.List[int] = rpchelp.rpc_field(rpchelp.arr(rpchelp.r_uint, rpchelp.LengthType.VAR, 16))


class msg_type(rpchelp.enum):
    CALL = 0
    REPLY = 1


class reply_stat(rpchelp.enum):
    MSG_ACCEPTED = 0
    MSG_DENIED = 1


class accept_stat(rpchelp.enum):
    SUCCESS = 0
    PROG_UNAVAIL = 1
    PROG_MISMATCH = 2
    PROC_UNAVAIL = 3
    GARBAGE_ARGS = 4
    SYSTEM_ERR = 5


class reject_stat(rpchelp.enum):
    RPC_MISMATCH = 0
    AUTH_ERROR = 1


class auth_stat(rpchelp.enum):
    AUTH_OK = 0
    AUTH_BADCRED = 1
    AUTH_REJECTEDCRED = 2
    AUTH_BADVERF = 3
    AUTH_REJECTEDVERF = 4
    AUTH_TOOWEAK = 5
    AUTH_INVALIDRESP = 6
    AUTH_FAILED = 7


@dataclass
class call_body(rpchelp.struct):
    rpcvers: int = rpchelp.rpc_field(rpchelp.r_uint)
    prog: int = rpchelp.rpc_field(rpchelp.r_uint)
    vers: int = rpchelp.rpc_field(rpchelp.r_uint)
    proc: int = rpchelp.rpc_field(rpchelp.r_uint)
    cred: opaque_auth = rpchelp.rpc_field(opaque_auth)
    verf: opaque_auth = rpchelp.rpc_field(opaque_auth)


@dataclass
class mismatch_info(rpchelp.struct):
    low: int = rpchelp.rpc_field(rpchelp.r_uint)
    high: int = rpchelp.rpc_field(rpchelp.r_uint)


@dataclass
class reply_data(rpchelp.union):
    SWITCH_OPTIONS = {SUCCESS: None, PROG_MISMATCH: 'mismatch', None: None}
    stat: accept_stat = rpchelp.rpc_field(accept_stat)
    mismatch: typing.Optional[mismatch_info] = rpchelp.rpc_field(mismatch_info, default=None)


@dataclass
class accepted_reply(rpchelp.struct):
    verf: opaque_auth = rpchelp.rpc_field(opaque_auth)
    data: reply_data = rpchelp.rpc_field(reply_data)


@dataclass
class rejected_reply_mismatch_info(rpchelp.struct):
    low: int = rpchelp.rpc_field(rpchelp.r_uint)
    high: int = rpchelp.rpc_field(rpchelp.r_uint)


@dataclass
class rejected_reply(rpchelp.union):
    SWITCH_OPTIONS = {RPC_MISMATCH: 'mismatch_info', AUTH_ERROR: 'auth_error'}
    r_stat: reject_stat = rpchelp.rpc_field(reject_stat)
    auth_error: typing.Optional[auth_stat] = rpchelp.rpc_field(auth_stat, default=None)
    mismatch_info: typing.Optional[rejected_reply_mismatch_info] = rpchelp.rpc_field(rejected_reply_mismatch_info, default=None)


@dataclass
class reply_body(rpchelp.union):
    SWITCH_OPTIONS = {MSG_ACCEPTED: 'areply', MSG_DENIED: 'rreply'}
    stat: reply_stat = rpchelp.rpc_field(reply_stat)
    rreply: typing.Optional[rejected_reply] = rpchelp.rpc_field(rejected_reply, default=None)
    areply: typing.Optional[accepted_reply] = rpchelp.rpc_field(accepted_reply, default=None)


@dataclass
class rpc_body(rpchelp.union):
    SWITCH_OPTIONS = {CALL: 'cbody', REPLY: 'rbody'}
    mtype: msg_type = rpchelp.rpc_field(msg_type)
    cbody: typing.Optional[call_body] = rpchelp.rpc_field(call_body, default=None)
    rbody: typing.Optional[reply_body] = rpchelp.rpc_field(reply_body, default=None)


@dataclass
class rpc_msg(rpchelp.struct):
    xid: int = rpchelp.rpc_field(rpchelp.r_uint)
    header: rpc_body = rpchelp.rpc_field(rpc_body)


__all__ = ['TRUE', 'FALSE', 'AUTH_NONE', 'AUTH_SYS', 'AUTH_SHORT', 'CALL', 'REPLY', 'MSG_ACCEPTED', 'MSG_DENIED', 'SUCCESS', 'PROG_UNAVAIL', 'PROG_MISMATCH', 'PROC_UNAVAIL', 'GARBAGE_ARGS', 'SYSTEM_ERR', 'RPC_MISMATCH', 'AUTH_ERROR', 'AUTH_OK', 'AUTH_BADCRED', 'AUTH_REJECTEDCRED', 'AUTH_BADVERF', 'AUTH_REJECTEDVERF', 'AUTH_TOOWEAK', 'AUTH_INVALIDRESP', 'AUTH_FAILED', 'auth_flavor', 'opaque_auth', 'authsys_parms', 'msg_type', 'reply_stat', 'accept_stat', 'reject_stat', 'auth_stat', 'call_body', 'mismatch_info', 'reply_data', 'accepted_reply', 'rejected_reply_mismatch_info', 'rejected_reply', 'reply_body', 'rpc_body', 'rpc_msg']
