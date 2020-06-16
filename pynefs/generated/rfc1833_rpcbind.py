# Auto-generated at Tue, 16 Jun 2020 13:13:33 +0000 from pynefs/idl/rfc1833_rpcbind.x

import abc
from dataclasses import dataclass
import typing

from pynefs import rpchelp

TRUE = True
FALSE = False

RPCB_PORT = 111
rpcb = rpchelp.struct('rpcb', [('r_prog', rpchelp.r_uint), ('r_vers', rpchelp.r_uint), ('r_netid', rpchelp.string(rpchelp.var, None)), ('r_addr', rpchelp.string(rpchelp.var, None)), ('r_owner', rpchelp.string(rpchelp.var, None))])
rp__list = rpchelp.linked_list('rp__list', [('rpcb_map', rpcb)])
rpcblist = rp__list
rpcb_rmtcallargs = rpchelp.struct('rpcb_rmtcallargs', [('prog', rpchelp.r_uint), ('vers', rpchelp.r_uint), ('proc', rpchelp.r_uint), ('args', rpchelp.opaque(rpchelp.var, None))])
rpcb_rmtcallres = rpchelp.struct('rpcb_rmtcallres', [('addr', rpchelp.string(rpchelp.var, None)), ('results', rpchelp.opaque(rpchelp.var, None))])
rpcb_entry = rpchelp.struct('rpcb_entry', [('r_maddr', rpchelp.string(rpchelp.var, None)), ('r_nc_netid', rpchelp.string(rpchelp.var, None)), ('r_nc_semantics', rpchelp.r_uint), ('r_nc_protofmly', rpchelp.string(rpchelp.var, None)), ('r_nc_proto', rpchelp.string(rpchelp.var, None))])
rpcb_entry_list = rpchelp.linked_list('rpcb_entry_list', [('rpcb_entry_map', rpcb_entry)])
rpcb_highproc_2 = 5
rpcb_highproc_3 = 8
rpcb_highproc_4 = 12
RPCBSTAT_HIGHPROC = 13
RPCBVERS_STAT = 3
RPCBVERS_4_STAT = 2
RPCBVERS_3_STAT = 1
RPCBVERS_2_STAT = 0
rpcbs_addrlist = rpchelp.linked_list('rpcbs_addrlist', [('prog', rpchelp.r_uint), ('vers', rpchelp.r_uint), ('success', rpchelp.r_int), ('failure', rpchelp.r_int), ('netid', rpchelp.string(rpchelp.var, None))])
rpcbs_rmtcalllist = rpchelp.linked_list('rpcbs_rmtcalllist', [('prog', rpchelp.r_uint), ('vers', rpchelp.r_uint), ('proc', rpchelp.r_uint), ('success', rpchelp.r_int), ('failure', rpchelp.r_int), ('indirect', rpchelp.r_int), ('netid', rpchelp.string(rpchelp.var, None))])
rpcbs_proc = rpchelp.arr(rpchelp.r_int, rpchelp.fixed, RPCBSTAT_HIGHPROC)
rpcb_stat = rpchelp.struct('rpcb_stat', [('info', rpcbs_proc), ('setinfo', rpchelp.r_int), ('unsetinfo', rpchelp.r_int), ('addrinfo', rpchelp.opt_data(rpcbs_addrlist)), ('rmtinfo', rpchelp.opt_data(rpcbs_rmtcalllist))])
rpcb_stat_byvers = rpchelp.arr(rpcb_stat, rpchelp.fixed, RPCBVERS_STAT)
netbuf = rpchelp.struct('netbuf', [('maxlen', rpchelp.r_uint), ('buf', rpchelp.opaque(rpchelp.var, None))])
@dataclass
class v_rpcb(rpchelp.struct_val_base):
	r_prog: int
	r_vers: int
	r_netid: bytes
	r_addr: bytes
	r_owner: bytes


rpcb.val_base_class = v_rpcb


@dataclass
class v_rp__list(rpchelp.struct_val_base):
	rpcb_map: v_rpcb


rp__list.val_base_class = v_rp__list


@dataclass
class v_rp__list(rpchelp.struct_val_base):
	rpcb_map: v_rpcb


rp__list.val_base_class = v_rp__list


@dataclass
class v_rpcb_rmtcallargs(rpchelp.struct_val_base):
	prog: int
	vers: int
	proc: int
	args: bytes


rpcb_rmtcallargs.val_base_class = v_rpcb_rmtcallargs


@dataclass
class v_rpcb_rmtcallres(rpchelp.struct_val_base):
	addr: bytes
	results: bytes


rpcb_rmtcallres.val_base_class = v_rpcb_rmtcallres


@dataclass
class v_rpcb_entry(rpchelp.struct_val_base):
	r_maddr: bytes
	r_nc_netid: bytes
	r_nc_semantics: int
	r_nc_protofmly: bytes
	r_nc_proto: bytes


rpcb_entry.val_base_class = v_rpcb_entry


@dataclass
class v_rpcb_entry_list(rpchelp.struct_val_base):
	rpcb_entry_map: v_rpcb_entry


rpcb_entry_list.val_base_class = v_rpcb_entry_list


@dataclass
class v_rpcbs_addrlist(rpchelp.struct_val_base):
	prog: int
	vers: int
	success: int
	failure: int
	netid: bytes


rpcbs_addrlist.val_base_class = v_rpcbs_addrlist


@dataclass
class v_rpcbs_rmtcalllist(rpchelp.struct_val_base):
	prog: int
	vers: int
	proc: int
	success: int
	failure: int
	indirect: int
	netid: bytes


rpcbs_rmtcalllist.val_base_class = v_rpcbs_rmtcalllist


@dataclass
class v_rpcb_stat(rpchelp.struct_val_base):
	info: typing.List[int]
	setinfo: int
	unsetinfo: int
	addrinfo: typing.List[v_rpcbs_addrlist]
	rmtinfo: typing.List[v_rpcbs_rmtcalllist]


rpcb_stat.val_base_class = v_rpcb_stat


@dataclass
class v_netbuf(rpchelp.struct_val_base):
	maxlen: int
	buf: bytes


netbuf.val_base_class = v_netbuf





class RPCBPROG_3(rpchelp.Server):
	prog = 100000
	vers = 3
	procs = {
		0: rpchelp.Proc('NULL', rpchelp.r_void, [rpchelp.r_void]),
		1: rpchelp.Proc('SET', rpchelp.r_bool, [rpcb]),
		2: rpchelp.Proc('UNSET', rpchelp.r_bool, [rpcb]),
		3: rpchelp.Proc('GETADDR', rpchelp.r_string, [rpcb]),
		4: rpchelp.Proc('DUMP', rpcblist, [rpchelp.r_void]),
		5: rpchelp.Proc('CALLIT', rpcb_rmtcallres, [rpcb_rmtcallargs]),
		6: rpchelp.Proc('GETTIME', rpchelp.r_uint, [rpchelp.r_void]),
		7: rpchelp.Proc('UADDR2TADDR', netbuf, [rpchelp.r_string]),
		8: rpchelp.Proc('TADDR2UADDR', rpchelp.r_string, [netbuf]),
	}

	@abc.abstractmethod
	def NULL(self, arg_0: None) -> None:
		pass

	@abc.abstractmethod
	def SET(self, arg_0: v_rpcb) -> bool:
		pass

	@abc.abstractmethod
	def UNSET(self, arg_0: v_rpcb) -> bool:
		pass

	@abc.abstractmethod
	def GETADDR(self, arg_0: v_rpcb) -> bytes:
		pass

	@abc.abstractmethod
	def DUMP(self, arg_0: None) -> typing.List[typing.Union[v_rpcb, v_rp__list]]:
		pass

	@abc.abstractmethod
	def CALLIT(self, arg_0: v_rpcb_rmtcallargs) -> v_rpcb_rmtcallres:
		pass

	@abc.abstractmethod
	def GETTIME(self, arg_0: None) -> int:
		pass

	@abc.abstractmethod
	def UADDR2TADDR(self, arg_0: bytes) -> v_netbuf:
		pass

	@abc.abstractmethod
	def TADDR2UADDR(self, arg_0: v_netbuf) -> bytes:
		pass


class RPCBPROG_4(rpchelp.Server):
	prog = 100000
	vers = 4
	procs = {
		0: rpchelp.Proc('NULL', rpchelp.r_void, [rpchelp.r_void]),
		1: rpchelp.Proc('SET', rpchelp.r_bool, [rpcb]),
		2: rpchelp.Proc('UNSET', rpchelp.r_bool, [rpcb]),
		3: rpchelp.Proc('GETADDR', rpchelp.r_string, [rpcb]),
		4: rpchelp.Proc('DUMP', rpcblist, [rpchelp.r_void]),
		5: rpchelp.Proc('BCAST', rpcb_rmtcallres, [rpcb_rmtcallargs]),
		6: rpchelp.Proc('GETTIME', rpchelp.r_uint, [rpchelp.r_void]),
		7: rpchelp.Proc('UADDR2TADDR', netbuf, [rpchelp.r_string]),
		8: rpchelp.Proc('TADDR2UADDR', rpchelp.r_string, [netbuf]),
		9: rpchelp.Proc('GETVERSADDR', rpchelp.r_string, [rpcb]),
		10: rpchelp.Proc('INDIRECT', rpcb_rmtcallres, [rpcb_rmtcallargs]),
		11: rpchelp.Proc('GETADDRLIST', rpcb_entry_list, [rpcb]),
		12: rpchelp.Proc('GETSTAT', rpcb_stat_byvers, [rpchelp.r_void]),
	}

	@abc.abstractmethod
	def NULL(self, arg_0: None) -> None:
		pass

	@abc.abstractmethod
	def SET(self, arg_0: v_rpcb) -> bool:
		pass

	@abc.abstractmethod
	def UNSET(self, arg_0: v_rpcb) -> bool:
		pass

	@abc.abstractmethod
	def GETADDR(self, arg_0: v_rpcb) -> bytes:
		pass

	@abc.abstractmethod
	def DUMP(self, arg_0: None) -> typing.List[typing.Union[v_rpcb, v_rp__list]]:
		pass

	@abc.abstractmethod
	def BCAST(self, arg_0: v_rpcb_rmtcallargs) -> v_rpcb_rmtcallres:
		pass

	@abc.abstractmethod
	def GETTIME(self, arg_0: None) -> int:
		pass

	@abc.abstractmethod
	def UADDR2TADDR(self, arg_0: bytes) -> v_netbuf:
		pass

	@abc.abstractmethod
	def TADDR2UADDR(self, arg_0: v_netbuf) -> bytes:
		pass

	@abc.abstractmethod
	def GETVERSADDR(self, arg_0: v_rpcb) -> bytes:
		pass

	@abc.abstractmethod
	def INDIRECT(self, arg_0: v_rpcb_rmtcallargs) -> v_rpcb_rmtcallres:
		pass

	@abc.abstractmethod
	def GETADDRLIST(self, arg_0: v_rpcb) -> typing.List[typing.Union[v_rpcb_entry, v_rpcb_entry_list]]:
		pass

	@abc.abstractmethod
	def GETSTAT(self, arg_0: None) -> typing.List[v_rpcb_stat]:
		pass


__all__ = ['v_rpcb', 'v_rp__list', 'v_rp__list', 'v_rpcb_rmtcallargs', 'v_rpcb_rmtcallres', 'v_rpcb_entry', 'v_rpcb_entry_list', 'v_rpcbs_addrlist', 'v_rpcbs_rmtcalllist', 'v_rpcb_stat', 'v_netbuf', 'RPCBPROG_3', 'RPCBPROG_4', 'TRUE', 'FALSE', 'RPCB_PORT', 'rpcb_highproc_2', 'rpcb_highproc_3', 'rpcb_highproc_4', 'RPCBSTAT_HIGHPROC', 'RPCBVERS_STAT', 'RPCBVERS_4_STAT', 'RPCBVERS_3_STAT', 'RPCBVERS_2_STAT']
