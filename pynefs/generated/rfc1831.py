# Auto-generated from IDL file

import abc
from dataclasses import dataclass
import typing

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
auth_flavor = rpchelp.r_int
opaque_auth = rpchelp.struct('opaque_auth', [('flavor', auth_flavor), ('body', rpchelp.opaque(rpchelp.var, 400))])
authsys_parms = rpchelp.struct('authsys_parms', [('stamp', rpchelp.r_uint), ('machinename', rpchelp.string(rpchelp.var, 255)), ('uid', rpchelp.r_uint), ('gid', rpchelp.r_uint), ('gids', rpchelp.arr(rpchelp.r_uint, rpchelp.var, 16))])
msg_type = rpchelp.r_int
reply_stat = rpchelp.r_int
accept_stat = rpchelp.r_int
reject_stat = rpchelp.r_int
auth_stat = rpchelp.r_int
call_body = rpchelp.struct('call_body', [('rpcvers', rpchelp.r_uint), ('prog', rpchelp.r_uint), ('vers', rpchelp.r_uint), ('proc', rpchelp.r_uint), ('cred', opaque_auth), ('verf', opaque_auth)])
mismatch_info = rpchelp.struct('mismatch_info', [('low', rpchelp.r_uint), ('high', rpchelp.r_uint)])
reply_data = rpchelp.union('reply_data', accept_stat, 'stat', {SUCCESS: rpchelp.r_void, PROG_MISMATCH: mismatch_info, None: rpchelp.r_void}, from_parser=True)
accepted_reply = rpchelp.struct('accepted_reply', [('verf', opaque_auth), ('data', reply_data)])
rejected_reply_mismatch_info = rpchelp.struct('rejected_reply_mismatch_info', [('low', rpchelp.r_uint), ('high', rpchelp.r_uint)])
rejected_reply = rpchelp.union('rejected_reply', reject_stat, 'stat', {RPC_MISMATCH: rejected_reply_mismatch_info, AUTH_ERROR: auth_stat}, from_parser=True)
reply_body = rpchelp.union('reply_body', reply_stat, 'stat', {MSG_ACCEPTED: accepted_reply, MSG_DENIED: rejected_reply}, from_parser=True)
rpc_body = rpchelp.union('rpc_body', msg_type, 'mtype', {CALL: call_body, REPLY: reply_body}, from_parser=True)
rpc_msg = rpchelp.struct('rpc_msg', [('xid', rpchelp.r_uint), ('body', rpc_body)])
@dataclass
class v_opaque_auth(rpchelp.struct_val_base):
	flavor: int
	body: bytes


opaque_auth.val_base_class = v_opaque_auth


@dataclass
class v_authsys_parms(rpchelp.struct_val_base):
	stamp: int
	machinename: bytes
	uid: int
	gid: int
	gids: typing.List[int]


authsys_parms.val_base_class = v_authsys_parms


@dataclass
class v_call_body(rpchelp.struct_val_base):
	rpcvers: int
	prog: int
	vers: int
	proc: int
	cred: v_opaque_auth
	verf: v_opaque_auth


call_body.val_base_class = v_call_body


@dataclass
class v_mismatch_info(rpchelp.struct_val_base):
	low: int
	high: int


mismatch_info.val_base_class = v_mismatch_info


@dataclass
class v_reply_data(rpchelp.struct_val_base):
	stat: int
	val: typing.Union[None, v_mismatch_info, None]


reply_data.val_base_class = v_reply_data


@dataclass
class v_accepted_reply(rpchelp.struct_val_base):
	verf: v_opaque_auth
	data: v_reply_data


accepted_reply.val_base_class = v_accepted_reply


@dataclass
class v_rejected_reply_mismatch_info(rpchelp.struct_val_base):
	low: int
	high: int


rejected_reply_mismatch_info.val_base_class = v_rejected_reply_mismatch_info


@dataclass
class v_rejected_reply(rpchelp.struct_val_base):
	stat: int
	val: typing.Union[v_rejected_reply_mismatch_info, int]


rejected_reply.val_base_class = v_rejected_reply


@dataclass
class v_reply_body(rpchelp.struct_val_base):
	stat: int
	val: typing.Union[v_accepted_reply, v_rejected_reply]


reply_body.val_base_class = v_reply_body


@dataclass
class v_rpc_body(rpchelp.struct_val_base):
	mtype: int
	val: typing.Union[v_call_body, v_reply_body]


rpc_body.val_base_class = v_rpc_body


@dataclass
class v_rpc_msg(rpchelp.struct_val_base):
	xid: int
	body: v_rpc_body


rpc_msg.val_base_class = v_rpc_msg






__all__ = ['v_opaque_auth', 'v_authsys_parms', 'v_call_body', 'v_mismatch_info', 'v_reply_data', 'v_accepted_reply', 'v_rejected_reply_mismatch_info', 'v_rejected_reply', 'v_reply_body', 'v_rpc_body', 'v_rpc_msg', 'TRUE', 'FALSE', 'AUTH_NONE', 'AUTH_SYS', 'AUTH_SHORT', 'CALL', 'REPLY', 'MSG_ACCEPTED', 'MSG_DENIED', 'SUCCESS', 'PROG_UNAVAIL', 'PROG_MISMATCH', 'PROC_UNAVAIL', 'GARBAGE_ARGS', 'SYSTEM_ERR', 'RPC_MISMATCH', 'AUTH_ERROR', 'AUTH_OK', 'AUTH_BADCRED', 'AUTH_REJECTEDCRED', 'AUTH_BADVERF', 'AUTH_REJECTEDVERF', 'AUTH_TOOWEAK', 'AUTH_INVALIDRESP', 'AUTH_FAILED']
