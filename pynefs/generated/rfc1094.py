# Auto-generated from IDL file
import abc
import dataclasses
import typing
from dataclasses import dataclass

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
nfsdata = rpchelp.opaque(rpchelp.LengthType.VAR, MAXDATA)


class stat(rpchelp.enum):
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


class ftype(rpchelp.enum):
    NFNON = 0
    NFREG = 1
    NFDIR = 2
    NFBLK = 3
    NFCHR = 4
    NFLNK = 5


fhandle = rpchelp.opaque(rpchelp.LengthType.FIXED, FHSIZE)


@dataclass
class timeval(rpchelp.struct):
    seconds: int = rpchelp.rpc_field(rpchelp.r_uint)
    useconds: int = rpchelp.rpc_field(rpchelp.r_uint)


@dataclass
class fattr(rpchelp.struct):
    type: ftype = rpchelp.rpc_field(ftype)
    mode: int = rpchelp.rpc_field(rpchelp.r_uint)
    nlink: int = rpchelp.rpc_field(rpchelp.r_uint)
    uid: int = rpchelp.rpc_field(rpchelp.r_uint)
    gid: int = rpchelp.rpc_field(rpchelp.r_uint)
    size: int = rpchelp.rpc_field(rpchelp.r_uint)
    blocksize: int = rpchelp.rpc_field(rpchelp.r_uint)
    rdev: int = rpchelp.rpc_field(rpchelp.r_uint)
    blocks: int = rpchelp.rpc_field(rpchelp.r_uint)
    fsid: int = rpchelp.rpc_field(rpchelp.r_uint)
    fileid: int = rpchelp.rpc_field(rpchelp.r_uint)
    atime: timeval = rpchelp.rpc_field(timeval)
    mtime: timeval = rpchelp.rpc_field(timeval)
    ctime: timeval = rpchelp.rpc_field(timeval)


@dataclass
class sattr(rpchelp.struct):
    mode: int = rpchelp.rpc_field(rpchelp.r_uint)
    uid: int = rpchelp.rpc_field(rpchelp.r_uint)
    gid: int = rpchelp.rpc_field(rpchelp.r_uint)
    size: int = rpchelp.rpc_field(rpchelp.r_uint)
    atime: timeval = rpchelp.rpc_field(timeval)
    mtime: timeval = rpchelp.rpc_field(timeval)


filename = rpchelp.string(rpchelp.LengthType.VAR, MAXNAMLEN)
path = rpchelp.string(rpchelp.LengthType.VAR, MAXPATHLEN)


@dataclass
class attrstat(rpchelp.union):
    SWITCH_OPTIONS = {NFS_OK: 'attributes', None: None}
    status: stat = rpchelp.rpc_field(stat)
    attributes: typing.Optional[fattr] = rpchelp.rpc_field(fattr, default=None)


@dataclass
class diropargs(rpchelp.struct):
    dir: bytes = rpchelp.rpc_field(fhandle)
    name: bytes = rpchelp.rpc_field(filename)


@dataclass
class diropres_diropok(rpchelp.struct):
    file: bytes = rpchelp.rpc_field(fhandle)
    attributes: fattr = rpchelp.rpc_field(fattr)


@dataclass
class diropres(rpchelp.union):
    SWITCH_OPTIONS = {NFS_OK: 'diropok', None: None}
    status: stat = rpchelp.rpc_field(stat)
    diropok: typing.Optional[diropres_diropok] = rpchelp.rpc_field(diropres_diropok, default=None)


@dataclass
class statfsres_info(rpchelp.struct):
    tsize: int = rpchelp.rpc_field(rpchelp.r_uint)
    bsize: int = rpchelp.rpc_field(rpchelp.r_uint)
    blocks: int = rpchelp.rpc_field(rpchelp.r_uint)
    bfree: int = rpchelp.rpc_field(rpchelp.r_uint)
    bavail: int = rpchelp.rpc_field(rpchelp.r_uint)


@dataclass
class statfsres(rpchelp.union):
    SWITCH_OPTIONS = {NFS_OK: 'info', None: None}
    status: stat = rpchelp.rpc_field(stat)
    info: typing.Optional[statfsres_info] = rpchelp.rpc_field(statfsres_info, default=None)


nfscookie = rpchelp.opaque(rpchelp.LengthType.FIXED, COOKIESIZE)


@dataclass
class readdirargs(rpchelp.struct):
    dir: bytes = rpchelp.rpc_field(fhandle)
    cookie: bytes = rpchelp.rpc_field(nfscookie)
    count: int = rpchelp.rpc_field(rpchelp.r_uint)


@dataclass
class entry(rpchelp.linked_list):
    fileid: int = rpchelp.rpc_field(rpchelp.r_uint)
    name: bytes = rpchelp.rpc_field(filename)
    cookie: bytes = rpchelp.rpc_field(nfscookie)


@dataclass
class readdirres_readdirok(rpchelp.struct):
    entries: typing.List[entry] = rpchelp.rpc_field(rpchelp.opt_data(entry))
    eof: bool = rpchelp.rpc_field(rpchelp.r_bool)


@dataclass
class readdirres(rpchelp.union):
    SWITCH_OPTIONS = {NFS_OK: 'readdirok', None: None}
    status: stat = rpchelp.rpc_field(stat)
    readdirok: typing.Optional[readdirres_readdirok] = rpchelp.rpc_field(readdirres_readdirok, default=None)


@dataclass
class symlinkargs(rpchelp.struct):
    from_: diropargs = rpchelp.rpc_field(diropargs)
    to: bytes = rpchelp.rpc_field(path)
    attributes: sattr = rpchelp.rpc_field(sattr)


@dataclass
class linkargs(rpchelp.struct):
    from_: bytes = rpchelp.rpc_field(fhandle)
    to: diropargs = rpchelp.rpc_field(diropargs)


@dataclass
class renameargs(rpchelp.struct):
    from_: diropargs = rpchelp.rpc_field(diropargs)
    to: diropargs = rpchelp.rpc_field(diropargs)


@dataclass
class createargs(rpchelp.struct):
    where: diropargs = rpchelp.rpc_field(diropargs)
    attributes: sattr = rpchelp.rpc_field(sattr)


@dataclass
class writeargs(rpchelp.struct):
    file: bytes = rpchelp.rpc_field(fhandle)
    beginoffset: int = rpchelp.rpc_field(rpchelp.r_uint)
    offset: int = rpchelp.rpc_field(rpchelp.r_uint)
    totalcount: int = rpchelp.rpc_field(rpchelp.r_uint)
    data: bytes = rpchelp.rpc_field(nfsdata)


@dataclass
class readargs(rpchelp.struct):
    file: bytes = rpchelp.rpc_field(fhandle)
    offset: int = rpchelp.rpc_field(rpchelp.r_uint)
    count: int = rpchelp.rpc_field(rpchelp.r_uint)
    totalcount: int = rpchelp.rpc_field(rpchelp.r_uint)


@dataclass
class attrdat(rpchelp.struct):
    attributes: fattr = rpchelp.rpc_field(fattr)
    data: bytes = rpchelp.rpc_field(nfsdata)


@dataclass
class readres(rpchelp.union):
    SWITCH_OPTIONS = {NFS_OK: 'attr_and_data', None: None}
    status: stat = rpchelp.rpc_field(stat)
    attr_and_data: typing.Optional[attrdat] = rpchelp.rpc_field(attrdat, default=None)


@dataclass
class readlinkres(rpchelp.union):
    SWITCH_OPTIONS = {NFS_OK: 'data', None: None}
    status: stat = rpchelp.rpc_field(stat)
    data: typing.Optional[bytes] = rpchelp.rpc_field(path, default=None)


@dataclass
class sattrargs(rpchelp.struct):
    file: bytes = rpchelp.rpc_field(fhandle)
    attributes: sattr = rpchelp.rpc_field(sattr)


MNTPATHLEN = 1024
dirpath = rpchelp.string(rpchelp.LengthType.VAR, MNTPATHLEN)
name = rpchelp.string(rpchelp.LengthType.VAR, MNTPATHLEN)


@dataclass
class fhstatus(rpchelp.union):
    SWITCH_OPTIONS = {0: 'directory', None: None}
    errno: int = rpchelp.rpc_field(rpchelp.r_uint)
    directory: typing.Optional[bytes] = rpchelp.rpc_field(fhandle, default=None)


@dataclass
class mountlist(rpchelp.linked_list):
    hostname: bytes = rpchelp.rpc_field(name)
    directory: bytes = rpchelp.rpc_field(dirpath)


@dataclass
class grouplist(rpchelp.linked_list):
    grname: bytes = rpchelp.rpc_field(name)


@dataclass
class exportlist(rpchelp.linked_list):
    filesys: bytes = rpchelp.rpc_field(dirpath)
    groups: typing.List[typing.Union[bytes, grouplist]] = rpchelp.rpc_field(grouplist)


from pynefs import client


class NFS_PROGRAM_2_SERVER(rpchelp.Prog):
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
        raise NotImplementedError()

    @abc.abstractmethod
    def GETATTR(self, arg_0: bytes) -> attrstat:
        raise NotImplementedError()

    @abc.abstractmethod
    def SETATTR(self, arg_0: sattrargs) -> attrstat:
        raise NotImplementedError()

    @abc.abstractmethod
    def ROOT(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def LOOKUP(self, arg_0: diropargs) -> diropres:
        raise NotImplementedError()

    @abc.abstractmethod
    def READLINK(self, arg_0: bytes) -> readlinkres:
        raise NotImplementedError()

    @abc.abstractmethod
    def READ(self, arg_0: readargs) -> readres:
        raise NotImplementedError()

    @abc.abstractmethod
    def WRITECACHE(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def WRITE(self, arg_0: writeargs) -> attrstat:
        raise NotImplementedError()

    @abc.abstractmethod
    def CREATE(self, arg_0: createargs) -> diropres:
        raise NotImplementedError()

    @abc.abstractmethod
    def REMOVE(self, arg_0: diropargs) -> stat:
        raise NotImplementedError()

    @abc.abstractmethod
    def RENAME(self, arg_0: renameargs) -> stat:
        raise NotImplementedError()

    @abc.abstractmethod
    def LINK(self, arg_0: linkargs) -> stat:
        raise NotImplementedError()

    @abc.abstractmethod
    def SYMLINK(self, arg_0: symlinkargs) -> stat:
        raise NotImplementedError()

    @abc.abstractmethod
    def MKDIR(self, arg_0: createargs) -> diropres:
        raise NotImplementedError()

    @abc.abstractmethod
    def RMDIR(self, arg_0: diropargs) -> stat:
        raise NotImplementedError()

    @abc.abstractmethod
    def READDIR(self, arg_0: readdirargs) -> readdirres:
        raise NotImplementedError()

    @abc.abstractmethod
    def STATFS(self, arg_0: bytes) -> statfsres:
        raise NotImplementedError()


class NFS_PROGRAM_2_CLIENT(client.BaseClient):
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

    async def NULL(self) -> client.UnpackedRPCMsg[None]:
        return await self.send_call(0, )

    async def GETATTR(self, arg_0: bytes) -> client.UnpackedRPCMsg[attrstat]:
        return await self.send_call(1, arg_0)

    async def SETATTR(self, arg_0: sattrargs) -> client.UnpackedRPCMsg[attrstat]:
        return await self.send_call(2, arg_0)

    async def ROOT(self) -> client.UnpackedRPCMsg[None]:
        return await self.send_call(3, )

    async def LOOKUP(self, arg_0: diropargs) -> client.UnpackedRPCMsg[diropres]:
        return await self.send_call(4, arg_0)

    async def READLINK(self, arg_0: bytes) -> client.UnpackedRPCMsg[readlinkres]:
        return await self.send_call(5, arg_0)

    async def READ(self, arg_0: readargs) -> client.UnpackedRPCMsg[readres]:
        return await self.send_call(6, arg_0)

    async def WRITECACHE(self) -> client.UnpackedRPCMsg[None]:
        return await self.send_call(7, )

    async def WRITE(self, arg_0: writeargs) -> client.UnpackedRPCMsg[attrstat]:
        return await self.send_call(8, arg_0)

    async def CREATE(self, arg_0: createargs) -> client.UnpackedRPCMsg[diropres]:
        return await self.send_call(9, arg_0)

    async def REMOVE(self, arg_0: diropargs) -> client.UnpackedRPCMsg[stat]:
        return await self.send_call(10, arg_0)

    async def RENAME(self, arg_0: renameargs) -> client.UnpackedRPCMsg[stat]:
        return await self.send_call(11, arg_0)

    async def LINK(self, arg_0: linkargs) -> client.UnpackedRPCMsg[stat]:
        return await self.send_call(12, arg_0)

    async def SYMLINK(self, arg_0: symlinkargs) -> client.UnpackedRPCMsg[stat]:
        return await self.send_call(13, arg_0)

    async def MKDIR(self, arg_0: createargs) -> client.UnpackedRPCMsg[diropres]:
        return await self.send_call(14, arg_0)

    async def RMDIR(self, arg_0: diropargs) -> client.UnpackedRPCMsg[stat]:
        return await self.send_call(15, arg_0)

    async def READDIR(self, arg_0: readdirargs) -> client.UnpackedRPCMsg[readdirres]:
        return await self.send_call(16, arg_0)

    async def STATFS(self, arg_0: bytes) -> client.UnpackedRPCMsg[statfsres]:
        return await self.send_call(17, arg_0)


class MOUNTPROG_1_SERVER(rpchelp.Prog):
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
        raise NotImplementedError()

    @abc.abstractmethod
    def MNT(self, arg_0: bytes) -> fhstatus:
        raise NotImplementedError()

    @abc.abstractmethod
    def DUMP(self) -> typing.List[mountlist]:
        raise NotImplementedError()

    @abc.abstractmethod
    def UMNT(self, arg_0: bytes) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def UMNTALL(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def EXPORT(self) -> typing.List[exportlist]:
        raise NotImplementedError()


class MOUNTPROG_1_CLIENT(client.BaseClient):
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

    async def NULL(self) -> client.UnpackedRPCMsg[None]:
        return await self.send_call(0, )

    async def MNT(self, arg_0: bytes) -> client.UnpackedRPCMsg[fhstatus]:
        return await self.send_call(1, arg_0)

    async def DUMP(self) -> client.UnpackedRPCMsg[typing.List[mountlist]]:
        return await self.send_call(2, )

    async def UMNT(self, arg_0: bytes) -> client.UnpackedRPCMsg[None]:
        return await self.send_call(3, arg_0)

    async def UMNTALL(self) -> client.UnpackedRPCMsg[None]:
        return await self.send_call(4, )

    async def EXPORT(self) -> client.UnpackedRPCMsg[typing.List[exportlist]]:
        return await self.send_call(5, )


__all__ = ['NFS_PROGRAM_2_SERVER', 'NFS_PROGRAM_2_CLIENT', 'MOUNTPROG_1_SERVER', 'MOUNTPROG_1_CLIENT', 'TRUE', 'FALSE', 'MAXDATA', 'MAXPATHLEN', 'MAXNAMLEN', 'COOKIESIZE', 'FHSIZE', 'NFS_OK', 'NFSERR_PERM', 'NFSERR_NOENT', 'NFSERR_IO', 'NFSERR_NXIO', 'NFSERR_ACCES', 'NFSERR_EXIST', 'NFSERR_NODEV', 'NFSERR_NOTDIR', 'NFSERR_ISDIR', 'NFSERR_FBIG', 'NFSERR_NOSPC', 'NFSERR_ROFS', 'NFSERR_NAMETOOLONG', 'NFSERR_NOTEMPTY', 'NFSERR_DQUOT', 'NFSERR_STALE', 'NFSERR_WFLUSH', 'NFNON', 'NFREG', 'NFDIR', 'NFBLK', 'NFCHR', 'NFLNK', 'MNTPATHLEN', 'nfsdata', 'stat', 'ftype', 'fhandle', 'timeval', 'fattr', 'sattr', 'filename', 'path', 'attrstat', 'diropargs', 'diropres_diropok', 'diropres', 'statfsres_info', 'statfsres', 'nfscookie', 'readdirargs', 'entry', 'readdirres_readdirok', 'readdirres', 'symlinkargs', 'linkargs', 'renameargs', 'createargs', 'writeargs', 'readargs', 'attrdat', 'readres', 'readlinkres', 'sattrargs', 'dirpath', 'name', 'fhstatus', 'mountlist', 'grouplist', 'exportlist']
