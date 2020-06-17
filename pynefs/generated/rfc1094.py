# Auto-generated from IDL file

import abc
from dataclasses import dataclass
import typing

from pynefs import rpchelp

TRUE = True
FALSE = False
NFS_OK = 0
NFSERR_PERM = 1
NFSERR_NOENT = 2
NFSERR_IO = 5
NFSERR_NXIO = 6
NFSERR_ACCES = 13
NFSERR_EXIST = 17
NFSERR_NODEV = 19
NFSERR_NOTDIR = 20
NFSERR_ISDIR = 21
NFSERR_FBIG = 27
NFSERR_NOSPC = 28
NFSERR_ROFS = 30
NFSERR_NAMETOOLONG = 63
NFSERR_NOTEMPTY = 66
NFSERR_DQUOT = 69
NFSERR_STALE = 70
NFSERR_WFLUSH = 99
NFNON = 0
NFREG = 1
NFDIR = 2
NFBLK = 3
NFCHR = 4
NFLNK = 5
MAXDATA = 8192
MAXPATHLEN = 1024
MAXNAMLEN = 255
COOKIESIZE = 4
FHSIZE = 32
nfsdata = rpchelp.opaque(rpchelp.var, MAXDATA)
stat = rpchelp.r_int
ftype = rpchelp.r_int
fhandle = rpchelp.opaque(rpchelp.fixed, FHSIZE)
timeval = rpchelp.struct('timeval', [('seconds', rpchelp.r_uint), ('useconds', rpchelp.r_uint)])
fattr = rpchelp.struct('fattr', [('type', ftype), ('mode', rpchelp.r_uint), ('nlink', rpchelp.r_uint), ('uid', rpchelp.r_uint), ('gid', rpchelp.r_uint), ('size', rpchelp.r_uint), ('blocksize', rpchelp.r_uint), ('rdev', rpchelp.r_uint), ('blocks', rpchelp.r_uint), ('fsid', rpchelp.r_uint), ('fileid', rpchelp.r_uint), ('atime', timeval), ('mtime', timeval), ('ctime', timeval)])
sattr = rpchelp.struct('sattr', [('mode', rpchelp.r_uint), ('uid', rpchelp.r_uint), ('gid', rpchelp.r_uint), ('size', rpchelp.r_uint), ('atime', timeval), ('mtime', timeval)])
filename = rpchelp.string(rpchelp.var, MAXNAMLEN)
path = rpchelp.string(rpchelp.var, MAXPATHLEN)
attrstat = rpchelp.union('attrstat', stat, 'status', {NFS_OK: fattr, None: rpchelp.r_void}, from_parser=True)
diropargs = rpchelp.struct('diropargs', [('dir', fhandle), ('name', filename)])
diropres_diropok = rpchelp.struct('diropres_diropok', [('file', fhandle), ('attributes', fattr)])
diropres = rpchelp.union('diropres', stat, 'status', {NFS_OK: diropres_diropok, None: rpchelp.r_void}, from_parser=True)
statfsres_info = rpchelp.struct('statfsres_info', [('tsize', rpchelp.r_uint), ('bsize', rpchelp.r_uint), ('blocks', rpchelp.r_uint), ('bfree', rpchelp.r_uint), ('bavail', rpchelp.r_uint)])
statfsres = rpchelp.union('statfsres', stat, 'status', {NFS_OK: statfsres_info, None: rpchelp.r_void}, from_parser=True)
nfscookie = rpchelp.opaque(rpchelp.fixed, COOKIESIZE)
readdirargs = rpchelp.struct('readdirargs', [('dir', fhandle), ('cookie', nfscookie), ('count', rpchelp.r_uint)])
entry = rpchelp.linked_list('entry', [('fileid', rpchelp.r_uint), ('name', filename), ('cookie', nfscookie)])
readdirres_readdirok = rpchelp.struct('readdirres_readdirok', [('entries', rpchelp.opt_data(entry)), ('eof', rpchelp.r_bool)])
readdirres = rpchelp.union('readdirres', stat, 'status', {NFS_OK: readdirres_readdirok, None: rpchelp.r_void}, from_parser=True)
symlinkargs = rpchelp.struct('symlinkargs', [('from_', diropargs), ('to', path), ('attributes', sattr)])
linkargs = rpchelp.struct('linkargs', [('from_', fhandle), ('to', diropargs)])
renameargs = rpchelp.struct('renameargs', [('from_', diropargs), ('to', diropargs)])
createargs = rpchelp.struct('createargs', [('where', diropargs), ('attributes', sattr)])
writeargs = rpchelp.struct('writeargs', [('file', fhandle), ('beginoffset', rpchelp.r_uint), ('offset', rpchelp.r_uint), ('totalcount', rpchelp.r_uint), ('data', nfsdata)])
readargs = rpchelp.struct('readargs', [('file', fhandle), ('offset', rpchelp.r_uint), ('count', rpchelp.r_uint), ('totalcount', rpchelp.r_uint)])
attrdat = rpchelp.struct('attrdat', [('attributes', fattr), ('data', nfsdata)])
readres = rpchelp.union('readres', stat, 'status', {NFS_OK: attrdat, None: rpchelp.r_void}, from_parser=True)
readlinkres = rpchelp.union('readlinkres', stat, 'status', {NFS_OK: path, None: rpchelp.r_void}, from_parser=True)
sattrargs = rpchelp.struct('sattrargs', [('file', fhandle), ('attributes', sattr)])

MNTPATHLEN = 1024
dirpath = rpchelp.string(rpchelp.var, MNTPATHLEN)
name = rpchelp.string(rpchelp.var, MNTPATHLEN)
fhstatus = rpchelp.union('fhstatus', rpchelp.r_uint, 'status', {0: fhandle, None: rpchelp.r_void}, from_parser=True)
mountlist = rpchelp.linked_list('mountlist', [('hostname', name), ('directory', dirpath)])
grouplist = rpchelp.linked_list('grouplist', [('grname', name)])
exportlist = rpchelp.linked_list('exportlist', [('filesys', dirpath), ('groups', grouplist)])
@dataclass
class v_timeval(rpchelp.struct_val_base):
	seconds: int
	useconds: int


timeval.val_base_class = v_timeval


@dataclass
class v_fattr(rpchelp.struct_val_base):
	type: int
	mode: int
	nlink: int
	uid: int
	gid: int
	size: int
	blocksize: int
	rdev: int
	blocks: int
	fsid: int
	fileid: int
	atime: v_timeval
	mtime: v_timeval
	ctime: v_timeval


fattr.val_base_class = v_fattr


@dataclass
class v_sattr(rpchelp.struct_val_base):
	mode: int
	uid: int
	gid: int
	size: int
	atime: v_timeval
	mtime: v_timeval


sattr.val_base_class = v_sattr


@dataclass
class v_attrstat(rpchelp.struct_val_base):
	status: int
	val: typing.Union[v_fattr, None]


attrstat.val_base_class = v_attrstat


@dataclass
class v_diropargs(rpchelp.struct_val_base):
	dir: bytes
	name: bytes


diropargs.val_base_class = v_diropargs


@dataclass
class v_diropres_diropok(rpchelp.struct_val_base):
	file: bytes
	attributes: v_fattr


diropres_diropok.val_base_class = v_diropres_diropok


@dataclass
class v_diropres(rpchelp.struct_val_base):
	status: int
	val: typing.Union[v_diropres_diropok, None]


diropres.val_base_class = v_diropres


@dataclass
class v_statfsres_info(rpchelp.struct_val_base):
	tsize: int
	bsize: int
	blocks: int
	bfree: int
	bavail: int


statfsres_info.val_base_class = v_statfsres_info


@dataclass
class v_statfsres(rpchelp.struct_val_base):
	status: int
	val: typing.Union[v_statfsres_info, None]


statfsres.val_base_class = v_statfsres


@dataclass
class v_readdirargs(rpchelp.struct_val_base):
	dir: bytes
	cookie: bytes
	count: int


readdirargs.val_base_class = v_readdirargs


@dataclass
class v_entry(rpchelp.struct_val_base):
	fileid: int
	name: bytes
	cookie: bytes


entry.val_base_class = v_entry


@dataclass
class v_readdirres_readdirok(rpchelp.struct_val_base):
	entries: typing.List[v_entry]
	eof: bool


readdirres_readdirok.val_base_class = v_readdirres_readdirok


@dataclass
class v_readdirres(rpchelp.struct_val_base):
	status: int
	val: typing.Union[v_readdirres_readdirok, None]


readdirres.val_base_class = v_readdirres


@dataclass
class v_symlinkargs(rpchelp.struct_val_base):
	from_: v_diropargs
	to: bytes
	attributes: v_sattr


symlinkargs.val_base_class = v_symlinkargs


@dataclass
class v_linkargs(rpchelp.struct_val_base):
	from_: bytes
	to: v_diropargs


linkargs.val_base_class = v_linkargs


@dataclass
class v_renameargs(rpchelp.struct_val_base):
	from_: v_diropargs
	to: v_diropargs


renameargs.val_base_class = v_renameargs


@dataclass
class v_createargs(rpchelp.struct_val_base):
	where: v_diropargs
	attributes: v_sattr


createargs.val_base_class = v_createargs


@dataclass
class v_writeargs(rpchelp.struct_val_base):
	file: bytes
	beginoffset: int
	offset: int
	totalcount: int
	data: bytes


writeargs.val_base_class = v_writeargs


@dataclass
class v_readargs(rpchelp.struct_val_base):
	file: bytes
	offset: int
	count: int
	totalcount: int


readargs.val_base_class = v_readargs


@dataclass
class v_attrdat(rpchelp.struct_val_base):
	attributes: v_fattr
	data: bytes


attrdat.val_base_class = v_attrdat


@dataclass
class v_readres(rpchelp.struct_val_base):
	status: int
	val: typing.Union[v_attrdat, None]


readres.val_base_class = v_readres


@dataclass
class v_readlinkres(rpchelp.struct_val_base):
	status: int
	val: typing.Union[bytes, None]


readlinkres.val_base_class = v_readlinkres


@dataclass
class v_sattrargs(rpchelp.struct_val_base):
	file: bytes
	attributes: v_sattr


sattrargs.val_base_class = v_sattrargs


@dataclass
class v_fhstatus(rpchelp.struct_val_base):
	status: int
	val: typing.Union[bytes, None]


fhstatus.val_base_class = v_fhstatus


@dataclass
class v_mountlist(rpchelp.struct_val_base):
	hostname: bytes
	directory: bytes


mountlist.val_base_class = v_mountlist


@dataclass
class v_grouplist(rpchelp.struct_val_base):
	grname: bytes


grouplist.val_base_class = v_grouplist


@dataclass
class v_exportlist(rpchelp.struct_val_base):
	filesys: bytes
	groups: typing.List[typing.Union[bytes, v_grouplist]]


exportlist.val_base_class = v_exportlist



from pynefs import rpc



class NFS_PROGRAM_2_SERVER(rpc.Server):
	prog = 100003
	vers = 2
	procs = {
		0: rpchelp.Proc('NULL', rpchelp.r_void, []),
		1: rpchelp.Proc('GETATTR', attrstat, [fhandle]),
		2: rpchelp.Proc('SETATTR', attrstat, [sattrargs]),
		3: rpchelp.Proc('ROOT', rpchelp.r_void, []),
		4: rpchelp.Proc('LOOKUP', diropres, [diropargs]),
		5: rpchelp.Proc('READLINK', readlinkres, [fhandle]),
		6: rpchelp.Proc('READ', readres, [readargs]),
		7: rpchelp.Proc('WRITECACHE', rpchelp.r_void, []),
		8: rpchelp.Proc('WRITE', attrstat, [writeargs]),
		9: rpchelp.Proc('CREATE', diropres, [createargs]),
		10: rpchelp.Proc('REMOVE', stat, [diropargs]),
		11: rpchelp.Proc('RENAME', stat, [renameargs]),
		12: rpchelp.Proc('LINK', stat, [linkargs]),
		13: rpchelp.Proc('SYMLINK', stat, [symlinkargs]),
		14: rpchelp.Proc('MKDIR', diropres, [createargs]),
		15: rpchelp.Proc('RMDIR', stat, [diropargs]),
		16: rpchelp.Proc('READDIR', readdirres, [readdirargs]),
		17: rpchelp.Proc('STATFS', statfsres, [fhandle]),
	}

	@abc.abstractmethod
	def NULL(self) -> None:
		pass

	@abc.abstractmethod
	def GETATTR(self, arg_0: bytes) -> v_attrstat:
		pass

	@abc.abstractmethod
	def SETATTR(self, arg_0: v_sattrargs) -> v_attrstat:
		pass

	@abc.abstractmethod
	def ROOT(self) -> None:
		pass

	@abc.abstractmethod
	def LOOKUP(self, arg_0: v_diropargs) -> v_diropres:
		pass

	@abc.abstractmethod
	def READLINK(self, arg_0: bytes) -> v_readlinkres:
		pass

	@abc.abstractmethod
	def READ(self, arg_0: v_readargs) -> v_readres:
		pass

	@abc.abstractmethod
	def WRITECACHE(self) -> None:
		pass

	@abc.abstractmethod
	def WRITE(self, arg_0: v_writeargs) -> v_attrstat:
		pass

	@abc.abstractmethod
	def CREATE(self, arg_0: v_createargs) -> v_diropres:
		pass

	@abc.abstractmethod
	def REMOVE(self, arg_0: v_diropargs) -> int:
		pass

	@abc.abstractmethod
	def RENAME(self, arg_0: v_renameargs) -> int:
		pass

	@abc.abstractmethod
	def LINK(self, arg_0: v_linkargs) -> int:
		pass

	@abc.abstractmethod
	def SYMLINK(self, arg_0: v_symlinkargs) -> int:
		pass

	@abc.abstractmethod
	def MKDIR(self, arg_0: v_createargs) -> v_diropres:
		pass

	@abc.abstractmethod
	def RMDIR(self, arg_0: v_diropargs) -> int:
		pass

	@abc.abstractmethod
	def READDIR(self, arg_0: v_readdirargs) -> v_readdirres:
		pass

	@abc.abstractmethod
	def STATFS(self, arg_0: bytes) -> v_statfsres:
		pass


class NFS_PROGRAM_2_CLIENT(rpc.BaseClient):
	prog = 100003
	vers = 2
	procs = {
		0: rpchelp.Proc('NULL', rpchelp.r_void, []),
		1: rpchelp.Proc('GETATTR', attrstat, [fhandle]),
		2: rpchelp.Proc('SETATTR', attrstat, [sattrargs]),
		3: rpchelp.Proc('ROOT', rpchelp.r_void, []),
		4: rpchelp.Proc('LOOKUP', diropres, [diropargs]),
		5: rpchelp.Proc('READLINK', readlinkres, [fhandle]),
		6: rpchelp.Proc('READ', readres, [readargs]),
		7: rpchelp.Proc('WRITECACHE', rpchelp.r_void, []),
		8: rpchelp.Proc('WRITE', attrstat, [writeargs]),
		9: rpchelp.Proc('CREATE', diropres, [createargs]),
		10: rpchelp.Proc('REMOVE', stat, [diropargs]),
		11: rpchelp.Proc('RENAME', stat, [renameargs]),
		12: rpchelp.Proc('LINK', stat, [linkargs]),
		13: rpchelp.Proc('SYMLINK', stat, [symlinkargs]),
		14: rpchelp.Proc('MKDIR', diropres, [createargs]),
		15: rpchelp.Proc('RMDIR', stat, [diropargs]),
		16: rpchelp.Proc('READDIR', readdirres, [readdirargs]),
		17: rpchelp.Proc('STATFS', statfsres, [fhandle]),
	}

	async def NULL(self) -> typing.Tuple[rpc.v_rpc_msg, typing.Optional[None]]:
		return await self.send_call(0, [])

	async def GETATTR(self, arg_0: bytes) -> typing.Tuple[rpc.v_rpc_msg, typing.Optional[v_attrstat]]:
		return await self.send_call(1, [arg_0])

	async def SETATTR(self, arg_0: v_sattrargs) -> typing.Tuple[rpc.v_rpc_msg, typing.Optional[v_attrstat]]:
		return await self.send_call(2, [arg_0])

	async def ROOT(self) -> typing.Tuple[rpc.v_rpc_msg, typing.Optional[None]]:
		return await self.send_call(3, [])

	async def LOOKUP(self, arg_0: v_diropargs) -> typing.Tuple[rpc.v_rpc_msg, typing.Optional[v_diropres]]:
		return await self.send_call(4, [arg_0])

	async def READLINK(self, arg_0: bytes) -> typing.Tuple[rpc.v_rpc_msg, typing.Optional[v_readlinkres]]:
		return await self.send_call(5, [arg_0])

	async def READ(self, arg_0: v_readargs) -> typing.Tuple[rpc.v_rpc_msg, typing.Optional[v_readres]]:
		return await self.send_call(6, [arg_0])

	async def WRITECACHE(self) -> typing.Tuple[rpc.v_rpc_msg, typing.Optional[None]]:
		return await self.send_call(7, [])

	async def WRITE(self, arg_0: v_writeargs) -> typing.Tuple[rpc.v_rpc_msg, typing.Optional[v_attrstat]]:
		return await self.send_call(8, [arg_0])

	async def CREATE(self, arg_0: v_createargs) -> typing.Tuple[rpc.v_rpc_msg, typing.Optional[v_diropres]]:
		return await self.send_call(9, [arg_0])

	async def REMOVE(self, arg_0: v_diropargs) -> typing.Tuple[rpc.v_rpc_msg, typing.Optional[int]]:
		return await self.send_call(10, [arg_0])

	async def RENAME(self, arg_0: v_renameargs) -> typing.Tuple[rpc.v_rpc_msg, typing.Optional[int]]:
		return await self.send_call(11, [arg_0])

	async def LINK(self, arg_0: v_linkargs) -> typing.Tuple[rpc.v_rpc_msg, typing.Optional[int]]:
		return await self.send_call(12, [arg_0])

	async def SYMLINK(self, arg_0: v_symlinkargs) -> typing.Tuple[rpc.v_rpc_msg, typing.Optional[int]]:
		return await self.send_call(13, [arg_0])

	async def MKDIR(self, arg_0: v_createargs) -> typing.Tuple[rpc.v_rpc_msg, typing.Optional[v_diropres]]:
		return await self.send_call(14, [arg_0])

	async def RMDIR(self, arg_0: v_diropargs) -> typing.Tuple[rpc.v_rpc_msg, typing.Optional[int]]:
		return await self.send_call(15, [arg_0])

	async def READDIR(self, arg_0: v_readdirargs) -> typing.Tuple[rpc.v_rpc_msg, typing.Optional[v_readdirres]]:
		return await self.send_call(16, [arg_0])

	async def STATFS(self, arg_0: bytes) -> typing.Tuple[rpc.v_rpc_msg, typing.Optional[v_statfsres]]:
		return await self.send_call(17, [arg_0])


class MOUNTPROG_1_SERVER(rpc.Server):
	prog = 100005
	vers = 1
	procs = {
		0: rpchelp.Proc('NULL', rpchelp.r_void, []),
		1: rpchelp.Proc('MNT', fhstatus, [dirpath]),
		2: rpchelp.Proc('DUMP', mountlist, []),
		3: rpchelp.Proc('UMNT', rpchelp.r_void, [dirpath]),
		4: rpchelp.Proc('UMNTALL', rpchelp.r_void, []),
		5: rpchelp.Proc('EXPORT', exportlist, []),
	}

	@abc.abstractmethod
	def NULL(self) -> None:
		pass

	@abc.abstractmethod
	def MNT(self, arg_0: bytes) -> v_fhstatus:
		pass

	@abc.abstractmethod
	def DUMP(self) -> typing.List[v_mountlist]:
		pass

	@abc.abstractmethod
	def UMNT(self, arg_0: bytes) -> None:
		pass

	@abc.abstractmethod
	def UMNTALL(self) -> None:
		pass

	@abc.abstractmethod
	def EXPORT(self) -> typing.List[v_exportlist]:
		pass


class MOUNTPROG_1_CLIENT(rpc.BaseClient):
	prog = 100005
	vers = 1
	procs = {
		0: rpchelp.Proc('NULL', rpchelp.r_void, []),
		1: rpchelp.Proc('MNT', fhstatus, [dirpath]),
		2: rpchelp.Proc('DUMP', mountlist, []),
		3: rpchelp.Proc('UMNT', rpchelp.r_void, [dirpath]),
		4: rpchelp.Proc('UMNTALL', rpchelp.r_void, []),
		5: rpchelp.Proc('EXPORT', exportlist, []),
	}

	async def NULL(self) -> typing.Tuple[rpc.v_rpc_msg, typing.Optional[None]]:
		return await self.send_call(0, [])

	async def MNT(self, arg_0: bytes) -> typing.Tuple[rpc.v_rpc_msg, typing.Optional[v_fhstatus]]:
		return await self.send_call(1, [arg_0])

	async def DUMP(self) -> typing.Tuple[rpc.v_rpc_msg, typing.Optional[typing.List[v_mountlist]]]:
		return await self.send_call(2, [])

	async def UMNT(self, arg_0: bytes) -> typing.Tuple[rpc.v_rpc_msg, typing.Optional[None]]:
		return await self.send_call(3, [arg_0])

	async def UMNTALL(self) -> typing.Tuple[rpc.v_rpc_msg, typing.Optional[None]]:
		return await self.send_call(4, [])

	async def EXPORT(self) -> typing.Tuple[rpc.v_rpc_msg, typing.Optional[typing.List[v_exportlist]]]:
		return await self.send_call(5, [])


__all__ = ['v_timeval', 'v_fattr', 'v_sattr', 'v_attrstat', 'v_diropargs', 'v_diropres_diropok', 'v_diropres', 'v_statfsres_info', 'v_statfsres', 'v_readdirargs', 'v_entry', 'v_readdirres_readdirok', 'v_readdirres', 'v_symlinkargs', 'v_linkargs', 'v_renameargs', 'v_createargs', 'v_writeargs', 'v_readargs', 'v_attrdat', 'v_readres', 'v_readlinkres', 'v_sattrargs', 'v_fhstatus', 'v_mountlist', 'v_grouplist', 'v_exportlist', 'NFS_PROGRAM_2_SERVER', 'MOUNTPROG_1_SERVER', 'TRUE', 'FALSE', 'NFS_OK', 'NFSERR_PERM', 'NFSERR_NOENT', 'NFSERR_IO', 'NFSERR_NXIO', 'NFSERR_ACCES', 'NFSERR_EXIST', 'NFSERR_NODEV', 'NFSERR_NOTDIR', 'NFSERR_ISDIR', 'NFSERR_FBIG', 'NFSERR_NOSPC', 'NFSERR_ROFS', 'NFSERR_NAMETOOLONG', 'NFSERR_NOTEMPTY', 'NFSERR_DQUOT', 'NFSERR_STALE', 'NFSERR_WFLUSH', 'NFNON', 'NFREG', 'NFDIR', 'NFBLK', 'NFCHR', 'NFLNK', 'MAXDATA', 'MAXPATHLEN', 'MAXNAMLEN', 'COOKIESIZE', 'FHSIZE', 'MNTPATHLEN']
