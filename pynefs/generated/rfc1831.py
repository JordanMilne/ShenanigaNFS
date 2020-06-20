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

reply_data = rpchelp.union('reply_data', accept_stat, 'stat', {SUCCESS: (None, rpchelp.r_void), PROG_MISMATCH: ('mismatch', mismatch_info), None: (None, rpchelp.r_void)}, from_parser=True)
@dataclass
class v_reply_data:
    stat: accept_stat
    mismatch: typing.Optional[mismatch_info] = None


reply_data.val_base_class = v_reply_data



@dataclass
class accepted_reply(rpchelp.struct):
    verf: opaque_auth = rpchelp.rpc_field(opaque_auth)
    data: v_reply_data = rpchelp.rpc_field(reply_data)

@dataclass
class rejected_reply_mismatch_info(rpchelp.struct):
    low: int = rpchelp.rpc_field(rpchelp.r_uint)
    high: int = rpchelp.rpc_field(rpchelp.r_uint)

rejected_reply = rpchelp.union('rejected_reply', reject_stat, 'reject_stat', {RPC_MISMATCH: ('mismatch_info', rejected_reply_mismatch_info), AUTH_ERROR: ('auth_stat', auth_stat)}, from_parser=True)
@dataclass
class v_rejected_reply:
    reject_stat: reject_stat
    mismatch_info: typing.Optional[rejected_reply_mismatch_info] = None
    auth_stat: typing.Optional[auth_stat] = None


rejected_reply.val_base_class = v_rejected_reply



reply_body = rpchelp.union('reply_body', reply_stat, 'stat', {MSG_ACCEPTED: ('areply', accepted_reply), MSG_DENIED: ('rreply', rejected_reply)}, from_parser=True)
@dataclass
class v_reply_body:
    stat: reply_stat
    areply: typing.Optional[accepted_reply] = None
    rreply: typing.Optional[v_rejected_reply] = None


reply_body.val_base_class = v_reply_body



rpc_body = rpchelp.union('rpc_body', msg_type, 'mtype', {CALL: ('cbody', call_body), REPLY: ('rbody', reply_body)}, from_parser=True)
@dataclass
class v_rpc_body:
    mtype: msg_type
    cbody: typing.Optional[call_body] = None
    rbody: typing.Optional[v_reply_body] = None


rpc_body.val_base_class = v_rpc_body



@dataclass
class rpc_msg(rpchelp.struct):
    xid: int = rpchelp.rpc_field(rpchelp.r_uint)
    header: v_rpc_body = rpchelp.rpc_field(rpc_body)




__all__ = ['auth_flavor', 'opaque_auth', 'authsys_parms', 'msg_type', 'reply_stat', 'accept_stat', 'reject_stat', 'auth_stat', 'call_body', 'mismatch_info', 'v_reply_data', 'accepted_reply', 'rejected_reply_mismatch_info', 'v_rejected_reply', 'v_reply_body', 'v_rpc_body', 'rpc_msg', 'TRUE', 'FALSE', 'AUTH_NONE', 'AUTH_SYS', 'AUTH_SHORT', 'CALL', 'REPLY', 'MSG_ACCEPTED', 'MSG_DENIED', 'SUCCESS', 'PROG_UNAVAIL', 'PROG_MISMATCH', 'PROC_UNAVAIL', 'GARBAGE_ARGS', 'SYSTEM_ERR', 'RPC_MISMATCH', 'AUTH_ERROR', 'AUTH_OK', 'AUTH_BADCRED', 'AUTH_REJECTEDCRED', 'AUTH_BADVERF', 'AUTH_REJECTEDVERF', 'AUTH_TOOWEAK', 'AUTH_INVALIDRESP', 'AUTH_FAILED']
