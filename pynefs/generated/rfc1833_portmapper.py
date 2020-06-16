# Auto-generated at Tue, 16 Jun 2020 13:11:32 +0000 from pynefs/idl/rfc1833_portmapper.x

import abc
from dataclasses import dataclass
import typing

from pynefs import rpchelp

TRUE = True
FALSE = False

PMAP_PORT = 111
mapping = rpchelp.struct('mapping', [('prog', rpchelp.r_uint), ('vers', rpchelp.r_uint), ('prot', rpchelp.r_uint), ('port', rpchelp.r_uint)])
IPPROTO_TCP = 6
IPPROTO_UDP = 17
pmaplist = rpchelp.linked_list('pmaplist', [('map', mapping)])
call_args = rpchelp.struct('call_args', [('prog', rpchelp.r_uint), ('vers', rpchelp.r_uint), ('proc', rpchelp.r_uint), ('args', rpchelp.opaque(rpchelp.var, None))])
call_result = rpchelp.struct('call_result', [('port', rpchelp.r_uint), ('res', rpchelp.opaque(rpchelp.var, None))])
@dataclass
class v_mapping(rpchelp.struct_val_base):
	prog: int
	vers: int
	prot: int
	port: int


mapping.val_base_class = v_mapping


@dataclass
class v_pmaplist(rpchelp.struct_val_base):
	map: v_mapping


pmaplist.val_base_class = v_pmaplist


@dataclass
class v_call_args(rpchelp.struct_val_base):
	prog: int
	vers: int
	proc: int
	args: bytes


call_args.val_base_class = v_call_args


@dataclass
class v_call_result(rpchelp.struct_val_base):
	port: int
	res: bytes


call_result.val_base_class = v_call_result





class PMAP_PROG_2(rpchelp.Server):
	prog = 100000
	vers = 2
	procs = {
		0: rpchelp.Proc('NULL', rpchelp.r_void, [rpchelp.r_void]),
		1: rpchelp.Proc('SET', rpchelp.r_bool, [mapping]),
		2: rpchelp.Proc('UNSET', rpchelp.r_bool, [mapping]),
		3: rpchelp.Proc('GETPORT', rpchelp.r_uint, [mapping]),
		4: rpchelp.Proc('DUMP', pmaplist, [rpchelp.r_void]),
		5: rpchelp.Proc('CALLIT', call_result, [call_args]),
	}

	@abc.abstractmethod
	def NULL(self, arg_0: None) -> None:
		pass

	@abc.abstractmethod
	def SET(self, arg_0: v_mapping) -> bool:
		pass

	@abc.abstractmethod
	def UNSET(self, arg_0: v_mapping) -> bool:
		pass

	@abc.abstractmethod
	def GETPORT(self, arg_0: v_mapping) -> int:
		pass

	@abc.abstractmethod
	def DUMP(self, arg_0: None) -> typing.List[typing.Union[v_mapping, v_pmaplist]]:
		pass

	@abc.abstractmethod
	def CALLIT(self, arg_0: v_call_args) -> v_call_result:
		pass


__all__ = ['v_mapping', 'v_pmaplist', 'v_call_args', 'v_call_result', 'PMAP_PROG_2', 'TRUE', 'FALSE', 'PMAP_PORT', 'IPPROTO_TCP', 'IPPROTO_UDP']
