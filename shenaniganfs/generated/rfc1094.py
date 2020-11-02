# Auto-generated from IDL file
import abc
import dataclasses
import typing
from dataclasses import dataclass

from shenaniganfs import rpchelp

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
NFSData = rpchelp.Opaque(rpchelp.LengthType.VAR, MAXDATA)


class Stat(rpchelp.Enum):  # stat
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


class Ftype(rpchelp.Enum):  # ftype
    NFNON = 0
    NFREG = 1
    NFDIR = 2
    NFBLK = 3
    NFCHR = 4
    NFLNK = 5


FHandle = rpchelp.Opaque(rpchelp.LengthType.FIXED, FHSIZE)


@dataclass
class Timeval(rpchelp.Struct):  # timeval
    seconds: int = rpchelp.rpc_field(rpchelp.r_uint)
    useconds: int = rpchelp.rpc_field(rpchelp.r_uint)


@dataclass
class FAttr(rpchelp.Struct):  # fattr
    type: typing.Union[Ftype, int] = rpchelp.rpc_field(Ftype)
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
    atime: Timeval = rpchelp.rpc_field(Timeval)
    mtime: Timeval = rpchelp.rpc_field(Timeval)
    ctime: Timeval = rpchelp.rpc_field(Timeval)


@dataclass
class SAttr(rpchelp.Struct):  # sattr
    mode: int = rpchelp.rpc_field(rpchelp.r_uint)
    uid: int = rpchelp.rpc_field(rpchelp.r_uint)
    gid: int = rpchelp.rpc_field(rpchelp.r_uint)
    size: int = rpchelp.rpc_field(rpchelp.r_uint)
    atime: Timeval = rpchelp.rpc_field(Timeval)
    mtime: Timeval = rpchelp.rpc_field(Timeval)


Filename = rpchelp.Opaque(rpchelp.LengthType.VAR, MAXNAMLEN)
Path = rpchelp.Opaque(rpchelp.LengthType.VAR, MAXPATHLEN)


@dataclass
class AttrStat(rpchelp.Union):  # attrstat
    SWITCH_OPTIONS = {None: None, NFS_OK: 'attributes'}
    status: typing.Union[Stat, int] = rpchelp.rpc_field(Stat)
    attributes: typing.Optional[FAttr] = rpchelp.rpc_field(FAttr, default=None)


@dataclass
class DiropArgs(rpchelp.Struct):  # diropargs
    dir: bytes = rpchelp.rpc_field(FHandle)
    name: bytes = rpchelp.rpc_field(Filename)


@dataclass
class DiropOK(rpchelp.Struct):  # diropok
    file: bytes = rpchelp.rpc_field(FHandle)
    attributes: FAttr = rpchelp.rpc_field(FAttr)


@dataclass
class DiropRes(rpchelp.Union):  # diropres
    SWITCH_OPTIONS = {None: None, NFS_OK: 'diropok'}
    status: typing.Union[Stat, int] = rpchelp.rpc_field(Stat)
    diropok: typing.Optional[DiropOK] = rpchelp.rpc_field(DiropOK, default=None)


@dataclass
class FsInfo(rpchelp.Struct):  # fs_info
    tsize: int = rpchelp.rpc_field(rpchelp.r_uint)
    bsize: int = rpchelp.rpc_field(rpchelp.r_uint)
    blocks: int = rpchelp.rpc_field(rpchelp.r_uint)
    bfree: int = rpchelp.rpc_field(rpchelp.r_uint)
    bavail: int = rpchelp.rpc_field(rpchelp.r_uint)


@dataclass
class StatfsRes(rpchelp.Union):  # statfsres
    SWITCH_OPTIONS = {None: None, NFS_OK: 'fs_info'}
    status: typing.Union[Stat, int] = rpchelp.rpc_field(Stat)
    fs_info: typing.Optional[FsInfo] = rpchelp.rpc_field(FsInfo, default=None)


NFScookie = rpchelp.Opaque(rpchelp.LengthType.FIXED, COOKIESIZE)


@dataclass
class ReaddirArgs(rpchelp.Struct):  # readdirargs
    dir: bytes = rpchelp.rpc_field(FHandle)
    cookie: bytes = rpchelp.rpc_field(NFScookie)
    count: int = rpchelp.rpc_field(rpchelp.r_uint)


@dataclass
class DirEntry(rpchelp.LinkedList):  # dir_entry
    fileid: int = rpchelp.rpc_field(rpchelp.r_uint)
    name: bytes = rpchelp.rpc_field(Filename)
    cookie: bytes = rpchelp.rpc_field(NFScookie)


@dataclass
class ReaddirOK(rpchelp.Struct):  # readdirok
    entries: typing.List[DirEntry] = rpchelp.rpc_field(rpchelp.OptData(DirEntry))
    eof: bool = rpchelp.rpc_field(rpchelp.r_bool)


@dataclass
class ReaddirRes(rpchelp.Union):  # readdirres
    SWITCH_OPTIONS = {None: None, NFS_OK: 'readdirok'}
    status: typing.Union[Stat, int] = rpchelp.rpc_field(Stat)
    readdirok: typing.Optional[ReaddirOK] = rpchelp.rpc_field(ReaddirOK, default=None)


@dataclass
class SymlinkArgs(rpchelp.Struct):  # symlinkargs
    from_: DiropArgs = rpchelp.rpc_field(DiropArgs)
    to: bytes = rpchelp.rpc_field(Path)
    attributes: SAttr = rpchelp.rpc_field(SAttr)


@dataclass
class LinkArgs(rpchelp.Struct):  # linkargs
    from_: bytes = rpchelp.rpc_field(FHandle)
    to: DiropArgs = rpchelp.rpc_field(DiropArgs)


@dataclass
class RenameArgs(rpchelp.Struct):  # renameargs
    from_: DiropArgs = rpchelp.rpc_field(DiropArgs)
    to: DiropArgs = rpchelp.rpc_field(DiropArgs)


@dataclass
class CreateArgs(rpchelp.Struct):  # createargs
    where: DiropArgs = rpchelp.rpc_field(DiropArgs)
    attributes: SAttr = rpchelp.rpc_field(SAttr)


@dataclass
class WriteArgs(rpchelp.Struct):  # writeargs
    file: bytes = rpchelp.rpc_field(FHandle)
    beginoffset: int = rpchelp.rpc_field(rpchelp.r_uint)
    offset: int = rpchelp.rpc_field(rpchelp.r_uint)
    totalcount: int = rpchelp.rpc_field(rpchelp.r_uint)
    data: bytes = rpchelp.rpc_field(NFSData)


@dataclass
class ReadArgs(rpchelp.Struct):  # readargs
    file: bytes = rpchelp.rpc_field(FHandle)
    offset: int = rpchelp.rpc_field(rpchelp.r_uint)
    count: int = rpchelp.rpc_field(rpchelp.r_uint)
    totalcount: int = rpchelp.rpc_field(rpchelp.r_uint)


@dataclass
class AttrDat(rpchelp.Struct):  # attrdat
    attributes: FAttr = rpchelp.rpc_field(FAttr)
    data: bytes = rpchelp.rpc_field(NFSData)


@dataclass
class ReadRes(rpchelp.Union):  # readres
    SWITCH_OPTIONS = {None: None, NFS_OK: 'attr_and_data'}
    status: typing.Union[Stat, int] = rpchelp.rpc_field(Stat)
    attr_and_data: typing.Optional[AttrDat] = rpchelp.rpc_field(AttrDat, default=None)


@dataclass
class ReadlinkRes(rpchelp.Union):  # readlinkres
    SWITCH_OPTIONS = {None: None, NFS_OK: 'data'}
    status: typing.Union[Stat, int] = rpchelp.rpc_field(Stat)
    data: typing.Optional[bytes] = rpchelp.rpc_field(Path, default=None)


@dataclass
class SattrArgs(rpchelp.Struct):  # sattrargs
    file: bytes = rpchelp.rpc_field(FHandle)
    attributes: SAttr = rpchelp.rpc_field(SAttr)


MNTPATHLEN = 1024
DirPath = rpchelp.Opaque(rpchelp.LengthType.VAR, MNTPATHLEN)
Name = rpchelp.Opaque(rpchelp.LengthType.VAR, MNTPATHLEN)


@dataclass
class FHStatus(rpchelp.Union):  # fhstatus
    SWITCH_OPTIONS = {None: None, 0: 'directory'}
    errno: int = rpchelp.rpc_field(rpchelp.r_uint)
    directory: typing.Optional[bytes] = rpchelp.rpc_field(FHandle, default=None)


@dataclass
class MountList(rpchelp.LinkedList):  # mountlist
    hostname: bytes = rpchelp.rpc_field(Name)
    directory: bytes = rpchelp.rpc_field(DirPath)


@dataclass
class GroupList(rpchelp.LinkedList):  # grouplist
    grname: bytes = rpchelp.rpc_field(Name)


@dataclass
class ExportList(rpchelp.LinkedList):  # exportlist
    filesys: bytes = rpchelp.rpc_field(DirPath)
    groups: typing.List[bytes] = rpchelp.rpc_field(GroupList)


from shenaniganfs import client


class NFS_PROGRAM_2_SERVER(rpchelp.Prog):
    prog = 100003
    vers = 2
    procs = {
        0: rpchelp.Proc('NULL', rpchelp.r_void, []),
        1: rpchelp.Proc('GETATTR', AttrStat, [FHandle]),
        2: rpchelp.Proc('SETATTR', AttrStat, [SattrArgs]),
        3: rpchelp.Proc('ROOT', rpchelp.r_void, []),
        4: rpchelp.Proc('LOOKUP', DiropRes, [DiropArgs]),
        5: rpchelp.Proc('READLINK', ReadlinkRes, [FHandle]),
        6: rpchelp.Proc('READ', ReadRes, [ReadArgs]),
        7: rpchelp.Proc('WRITECACHE', rpchelp.r_void, []),
        8: rpchelp.Proc('WRITE', AttrStat, [WriteArgs]),
        9: rpchelp.Proc('CREATE', DiropRes, [CreateArgs]),
        10: rpchelp.Proc('REMOVE', Stat, [DiropArgs]),
        11: rpchelp.Proc('RENAME', Stat, [RenameArgs]),
        12: rpchelp.Proc('LINK', Stat, [LinkArgs]),
        13: rpchelp.Proc('SYMLINK', Stat, [SymlinkArgs]),
        14: rpchelp.Proc('MKDIR', DiropRes, [CreateArgs]),
        15: rpchelp.Proc('RMDIR', Stat, [DiropArgs]),
        16: rpchelp.Proc('READDIR', ReaddirRes, [ReaddirArgs]),
        17: rpchelp.Proc('STATFS', StatfsRes, [FHandle]),
    }

    @abc.abstractmethod
    async def NULL(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def GETATTR(self, arg_0: bytes) -> AttrStat:
        raise NotImplementedError()

    @abc.abstractmethod
    async def SETATTR(self, arg_0: SattrArgs) -> AttrStat:
        raise NotImplementedError()

    @abc.abstractmethod
    async def ROOT(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def LOOKUP(self, arg_0: DiropArgs) -> DiropRes:
        raise NotImplementedError()

    @abc.abstractmethod
    async def READLINK(self, arg_0: bytes) -> ReadlinkRes:
        raise NotImplementedError()

    @abc.abstractmethod
    async def READ(self, arg_0: ReadArgs) -> ReadRes:
        raise NotImplementedError()

    @abc.abstractmethod
    async def WRITECACHE(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def WRITE(self, arg_0: WriteArgs) -> AttrStat:
        raise NotImplementedError()

    @abc.abstractmethod
    async def CREATE(self, arg_0: CreateArgs) -> DiropRes:
        raise NotImplementedError()

    @abc.abstractmethod
    async def REMOVE(self, arg_0: DiropArgs) -> typing.Union[Stat, int]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def RENAME(self, arg_0: RenameArgs) -> typing.Union[Stat, int]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def LINK(self, arg_0: LinkArgs) -> typing.Union[Stat, int]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def SYMLINK(self, arg_0: SymlinkArgs) -> typing.Union[Stat, int]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def MKDIR(self, arg_0: CreateArgs) -> DiropRes:
        raise NotImplementedError()

    @abc.abstractmethod
    async def RMDIR(self, arg_0: DiropArgs) -> typing.Union[Stat, int]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def READDIR(self, arg_0: ReaddirArgs) -> ReaddirRes:
        raise NotImplementedError()

    @abc.abstractmethod
    async def STATFS(self, arg_0: bytes) -> StatfsRes:
        raise NotImplementedError()


class NFS_PROGRAM_2_CLIENT(client.BaseClient):
    prog = 100003
    vers = 2
    procs = {
        0: rpchelp.Proc('NULL', rpchelp.r_void, []),
        1: rpchelp.Proc('GETATTR', AttrStat, [FHandle]),
        2: rpchelp.Proc('SETATTR', AttrStat, [SattrArgs]),
        3: rpchelp.Proc('ROOT', rpchelp.r_void, []),
        4: rpchelp.Proc('LOOKUP', DiropRes, [DiropArgs]),
        5: rpchelp.Proc('READLINK', ReadlinkRes, [FHandle]),
        6: rpchelp.Proc('READ', ReadRes, [ReadArgs]),
        7: rpchelp.Proc('WRITECACHE', rpchelp.r_void, []),
        8: rpchelp.Proc('WRITE', AttrStat, [WriteArgs]),
        9: rpchelp.Proc('CREATE', DiropRes, [CreateArgs]),
        10: rpchelp.Proc('REMOVE', Stat, [DiropArgs]),
        11: rpchelp.Proc('RENAME', Stat, [RenameArgs]),
        12: rpchelp.Proc('LINK', Stat, [LinkArgs]),
        13: rpchelp.Proc('SYMLINK', Stat, [SymlinkArgs]),
        14: rpchelp.Proc('MKDIR', DiropRes, [CreateArgs]),
        15: rpchelp.Proc('RMDIR', Stat, [DiropArgs]),
        16: rpchelp.Proc('READDIR', ReaddirRes, [ReaddirArgs]),
        17: rpchelp.Proc('STATFS', StatfsRes, [FHandle]),
    }

    async def NULL(self) -> client.UnpackedRPCMsg[None]:
        return await self.send_call(0, )

    async def GETATTR(self, arg_0: bytes) -> client.UnpackedRPCMsg[AttrStat]:
        return await self.send_call(1, arg_0)

    async def SETATTR(self, arg_0: SattrArgs) -> client.UnpackedRPCMsg[AttrStat]:
        return await self.send_call(2, arg_0)

    async def ROOT(self) -> client.UnpackedRPCMsg[None]:
        return await self.send_call(3, )

    async def LOOKUP(self, arg_0: DiropArgs) -> client.UnpackedRPCMsg[DiropRes]:
        return await self.send_call(4, arg_0)

    async def READLINK(self, arg_0: bytes) -> client.UnpackedRPCMsg[ReadlinkRes]:
        return await self.send_call(5, arg_0)

    async def READ(self, arg_0: ReadArgs) -> client.UnpackedRPCMsg[ReadRes]:
        return await self.send_call(6, arg_0)

    async def WRITECACHE(self) -> client.UnpackedRPCMsg[None]:
        return await self.send_call(7, )

    async def WRITE(self, arg_0: WriteArgs) -> client.UnpackedRPCMsg[AttrStat]:
        return await self.send_call(8, arg_0)

    async def CREATE(self, arg_0: CreateArgs) -> client.UnpackedRPCMsg[DiropRes]:
        return await self.send_call(9, arg_0)

    async def REMOVE(self, arg_0: DiropArgs) -> client.UnpackedRPCMsg[typing.Union[Stat, int]]:
        return await self.send_call(10, arg_0)

    async def RENAME(self, arg_0: RenameArgs) -> client.UnpackedRPCMsg[typing.Union[Stat, int]]:
        return await self.send_call(11, arg_0)

    async def LINK(self, arg_0: LinkArgs) -> client.UnpackedRPCMsg[typing.Union[Stat, int]]:
        return await self.send_call(12, arg_0)

    async def SYMLINK(self, arg_0: SymlinkArgs) -> client.UnpackedRPCMsg[typing.Union[Stat, int]]:
        return await self.send_call(13, arg_0)

    async def MKDIR(self, arg_0: CreateArgs) -> client.UnpackedRPCMsg[DiropRes]:
        return await self.send_call(14, arg_0)

    async def RMDIR(self, arg_0: DiropArgs) -> client.UnpackedRPCMsg[typing.Union[Stat, int]]:
        return await self.send_call(15, arg_0)

    async def READDIR(self, arg_0: ReaddirArgs) -> client.UnpackedRPCMsg[ReaddirRes]:
        return await self.send_call(16, arg_0)

    async def STATFS(self, arg_0: bytes) -> client.UnpackedRPCMsg[StatfsRes]:
        return await self.send_call(17, arg_0)


class MOUNTPROG_1_SERVER(rpchelp.Prog):
    prog = 100005
    vers = 1
    procs = {
        0: rpchelp.Proc('NULL', rpchelp.r_void, []),
        1: rpchelp.Proc('MNT', FHStatus, [DirPath]),
        2: rpchelp.Proc('DUMP', MountList, []),
        3: rpchelp.Proc('UMNT', rpchelp.r_void, [DirPath]),
        4: rpchelp.Proc('UMNTALL', rpchelp.r_void, []),
        5: rpchelp.Proc('EXPORT', ExportList, []),
    }

    @abc.abstractmethod
    async def NULL(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def MNT(self, arg_0: bytes) -> FHStatus:
        raise NotImplementedError()

    @abc.abstractmethod
    async def DUMP(self) -> typing.List[MountList]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def UMNT(self, arg_0: bytes) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def UMNTALL(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def EXPORT(self) -> typing.List[ExportList]:
        raise NotImplementedError()


class MOUNTPROG_1_CLIENT(client.BaseClient):
    prog = 100005
    vers = 1
    procs = {
        0: rpchelp.Proc('NULL', rpchelp.r_void, []),
        1: rpchelp.Proc('MNT', FHStatus, [DirPath]),
        2: rpchelp.Proc('DUMP', MountList, []),
        3: rpchelp.Proc('UMNT', rpchelp.r_void, [DirPath]),
        4: rpchelp.Proc('UMNTALL', rpchelp.r_void, []),
        5: rpchelp.Proc('EXPORT', ExportList, []),
    }

    async def NULL(self) -> client.UnpackedRPCMsg[None]:
        return await self.send_call(0, )

    async def MNT(self, arg_0: bytes) -> client.UnpackedRPCMsg[FHStatus]:
        return await self.send_call(1, arg_0)

    async def DUMP(self) -> client.UnpackedRPCMsg[typing.List[MountList]]:
        return await self.send_call(2, )

    async def UMNT(self, arg_0: bytes) -> client.UnpackedRPCMsg[None]:
        return await self.send_call(3, arg_0)

    async def UMNTALL(self) -> client.UnpackedRPCMsg[None]:
        return await self.send_call(4, )

    async def EXPORT(self) -> client.UnpackedRPCMsg[typing.List[ExportList]]:
        return await self.send_call(5, )


__all__ = ['NFS_PROGRAM_2_SERVER', 'NFS_PROGRAM_2_CLIENT', 'MOUNTPROG_1_SERVER', 'MOUNTPROG_1_CLIENT', 'TRUE', 'FALSE', 'MAXDATA', 'MAXPATHLEN', 'MAXNAMLEN', 'COOKIESIZE', 'FHSIZE', 'NFS_OK', 'NFSERR_PERM', 'NFSERR_NOENT', 'NFSERR_IO', 'NFSERR_NXIO', 'NFSERR_ACCES', 'NFSERR_EXIST', 'NFSERR_NODEV', 'NFSERR_NOTDIR', 'NFSERR_ISDIR', 'NFSERR_FBIG', 'NFSERR_NOSPC', 'NFSERR_ROFS', 'NFSERR_NAMETOOLONG', 'NFSERR_NOTEMPTY', 'NFSERR_DQUOT', 'NFSERR_STALE', 'NFSERR_WFLUSH', 'NFNON', 'NFREG', 'NFDIR', 'NFBLK', 'NFCHR', 'NFLNK', 'MNTPATHLEN', 'NFSData', 'Stat', 'Ftype', 'FHandle', 'Timeval', 'FAttr', 'SAttr', 'Filename', 'Path', 'AttrStat', 'DiropArgs', 'DiropOK', 'DiropRes', 'FsInfo', 'StatfsRes', 'NFScookie', 'ReaddirArgs', 'DirEntry', 'ReaddirOK', 'ReaddirRes', 'SymlinkArgs', 'LinkArgs', 'RenameArgs', 'CreateArgs', 'WriteArgs', 'ReadArgs', 'AttrDat', 'ReadRes', 'ReadlinkRes', 'SattrArgs', 'DirPath', 'Name', 'FHStatus', 'MountList', 'GroupList', 'ExportList']
