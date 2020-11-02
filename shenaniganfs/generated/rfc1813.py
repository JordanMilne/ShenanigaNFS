# Auto-generated from IDL file
import abc
import dataclasses
import typing
from dataclasses import dataclass

from shenaniganfs import rpchelp

TRUE = True
FALSE = False
NFS3_OK = 0
NFS3ERR_PERM = 1
NFS3ERR_NOENT = 2
NFS3ERR_IO = 5
NFS3ERR_NXIO = 6
NFS3ERR_ACCES = 13
NFS3ERR_EXIST = 17
NFS3ERR_XDEV = 18
NFS3ERR_NODEV = 19
NFS3ERR_NOTDIR = 20
NFS3ERR_ISDIR = 21
NFS3ERR_INVAL = 22
NFS3ERR_FBIG = 27
NFS3ERR_NOSPC = 28
NFS3ERR_ROFS = 30
NFS3ERR_MLINK = 31
NFS3ERR_NAMETOOLONG = 63
NFS3ERR_NOTEMPTY = 66
NFS3ERR_DQUOT = 69
NFS3ERR_STALE = 70
NFS3ERR_REMOTE = 71
NFS3ERR_BADHANDLE = 10001
NFS3ERR_NOT_SYNC = 10002
NFS3ERR_BAD_COOKIE = 10003
NFS3ERR_NOTSUPP = 10004
NFS3ERR_TOOSMALL = 10005
NFS3ERR_SERVERFAULT = 10006
NFS3ERR_BADTYPE = 10007
NFS3ERR_JUKEBOX = 10008
NF3REG = 1
NF3DIR = 2
NF3BLK = 3
NF3CHR = 4
NF3LNK = 5
NF3SOCK = 6
NF3FIFO = 7
DONT_CHANGE = 0
SET_TO_SERVER_TIME = 1
SET_TO_CLIENT_TIME = 2
UNSTABLE = 0
DATA_SYNC = 1
FILE_SYNC = 2
UNCHECKED = 0
GUARDED = 1
EXCLUSIVE = 2
MNT3_OK = 0
MNT3ERR_PERM = 1
MNT3ERR_NOENT = 2
MNT3ERR_IO = 5
MNT3ERR_ACCES = 13
MNT3ERR_NOTDIR = 20
MNT3ERR_INVAL = 22
MNT3ERR_NAMETOOLONG = 63
MNT3ERR_NOTSUPP = 10004
MNT3ERR_SERVERFAULT = 10006
NFS3_FHSIZE = 64
NFS3_COOKIEVERFSIZE = 8
NFS3_CREATEVERFSIZE = 8
NFS3_WRITEVERFSIZE = 8
Uint64 = rpchelp.r_uhyper
Int64 = rpchelp.r_hyper
Uint32 = rpchelp.r_uint
Int32 = rpchelp.r_int
Filename3 = rpchelp.Opaque(rpchelp.LengthType.VAR, None)
NFSPath3 = rpchelp.Opaque(rpchelp.LengthType.VAR, None)
Fileid3 = Uint64
Cookie3 = Uint64
Cookieverf3 = rpchelp.Opaque(rpchelp.LengthType.FIXED, NFS3_COOKIEVERFSIZE)
Createverf3 = rpchelp.Opaque(rpchelp.LengthType.FIXED, NFS3_CREATEVERFSIZE)
Writeverf3 = rpchelp.Opaque(rpchelp.LengthType.FIXED, NFS3_WRITEVERFSIZE)
Uid3 = Uint32
Gid3 = Uint32
Size3 = Uint64
Offset3 = Uint64
Mode3 = Uint32
Count3 = Uint32


class NFSStat3(rpchelp.Enum):  # nfsstat3
    NFS3_OK = 0
    NFS3ERR_PERM = 1
    NFS3ERR_NOENT = 2
    NFS3ERR_IO = 5
    NFS3ERR_NXIO = 6
    NFS3ERR_ACCES = 13
    NFS3ERR_EXIST = 17
    NFS3ERR_XDEV = 18
    NFS3ERR_NODEV = 19
    NFS3ERR_NOTDIR = 20
    NFS3ERR_ISDIR = 21
    NFS3ERR_INVAL = 22
    NFS3ERR_FBIG = 27
    NFS3ERR_NOSPC = 28
    NFS3ERR_ROFS = 30
    NFS3ERR_MLINK = 31
    NFS3ERR_NAMETOOLONG = 63
    NFS3ERR_NOTEMPTY = 66
    NFS3ERR_DQUOT = 69
    NFS3ERR_STALE = 70
    NFS3ERR_REMOTE = 71
    NFS3ERR_BADHANDLE = 10001
    NFS3ERR_NOT_SYNC = 10002
    NFS3ERR_BAD_COOKIE = 10003
    NFS3ERR_NOTSUPP = 10004
    NFS3ERR_TOOSMALL = 10005
    NFS3ERR_SERVERFAULT = 10006
    NFS3ERR_BADTYPE = 10007
    NFS3ERR_JUKEBOX = 10008


class Ftype3(rpchelp.Enum):  # ftype3
    NF3REG = 1
    NF3DIR = 2
    NF3BLK = 3
    NF3CHR = 4
    NF3LNK = 5
    NF3SOCK = 6
    NF3FIFO = 7


@dataclass
class SpecData3(rpchelp.Struct):  # specdata3
    specdata1: int = rpchelp.rpc_field(Uint32)
    specdata2: int = rpchelp.rpc_field(Uint32)


NFSFh3 = rpchelp.Opaque(rpchelp.LengthType.VAR, NFS3_FHSIZE)


@dataclass
class NFSTime3(rpchelp.Struct):  # nfstime3
    seconds: int = rpchelp.rpc_field(Uint32)
    nseconds: int = rpchelp.rpc_field(Uint32)


@dataclass
class FAttr3(rpchelp.Struct):  # fattr3
    type: typing.Union[Ftype3, int] = rpchelp.rpc_field(Ftype3)
    mode: int = rpchelp.rpc_field(Mode3)
    nlink: int = rpchelp.rpc_field(Uint32)
    uid: int = rpchelp.rpc_field(Uid3)
    gid: int = rpchelp.rpc_field(Gid3)
    size: int = rpchelp.rpc_field(Size3)
    used: int = rpchelp.rpc_field(Size3)
    rdev: SpecData3 = rpchelp.rpc_field(SpecData3)
    fsid: int = rpchelp.rpc_field(Uint64)
    fileid: int = rpchelp.rpc_field(Fileid3)
    atime: NFSTime3 = rpchelp.rpc_field(NFSTime3)
    mtime: NFSTime3 = rpchelp.rpc_field(NFSTime3)
    ctime: NFSTime3 = rpchelp.rpc_field(NFSTime3)


@dataclass
class WccAttr(rpchelp.Struct):  # wcc_attr
    size: int = rpchelp.rpc_field(Size3)
    mtime: NFSTime3 = rpchelp.rpc_field(NFSTime3)
    ctime: NFSTime3 = rpchelp.rpc_field(NFSTime3)


PostOpAttr = rpchelp.OptData(FAttr3)
PreOpAttr = rpchelp.OptData(WccAttr)


@dataclass
class WccData(rpchelp.Struct):  # wcc_data
    before: typing.Optional[WccAttr] = rpchelp.rpc_field(PreOpAttr)
    after: typing.Optional[FAttr3] = rpchelp.rpc_field(PostOpAttr)


PostOpFh3 = rpchelp.OptData(NFSFh3)


class TimeHow(rpchelp.Enum):  # time_how
    DONT_CHANGE = 0
    SET_TO_SERVER_TIME = 1
    SET_TO_CLIENT_TIME = 2


SetMode3 = rpchelp.OptData(Mode3)
SetUid3 = rpchelp.OptData(Uid3)
SetGid3 = rpchelp.OptData(Gid3)
SetSize3 = rpchelp.OptData(Size3)


@dataclass
class SetTime(rpchelp.Union):  # set_time
    SWITCH_OPTIONS = {None: None, SET_TO_CLIENT_TIME: 'time_val'}
    set_it: typing.Union[TimeHow, int] = rpchelp.rpc_field(TimeHow)
    time_val: typing.Optional[NFSTime3] = rpchelp.rpc_field(NFSTime3, default=None)


@dataclass
class SAttr3(rpchelp.Struct):  # sattr3
    mode: typing.Optional[int] = rpchelp.rpc_field(SetMode3)
    uid: typing.Optional[int] = rpchelp.rpc_field(SetUid3)
    gid: typing.Optional[int] = rpchelp.rpc_field(SetGid3)
    size: typing.Optional[int] = rpchelp.rpc_field(SetSize3)
    atime: SetTime = rpchelp.rpc_field(SetTime)
    mtime: SetTime = rpchelp.rpc_field(SetTime)


@dataclass
class DiropArgs3(rpchelp.Struct):  # diropargs3
    dir_handle: bytes = rpchelp.rpc_field(NFSFh3)
    name: bytes = rpchelp.rpc_field(Filename3)


@dataclass
class GETATTR3Args(rpchelp.Struct):  # GETATTR3args
    obj_handle: bytes = rpchelp.rpc_field(NFSFh3)


@dataclass
class GETATTR3ResOK(rpchelp.Struct):  # GETATTR3resok
    obj_attributes: FAttr3 = rpchelp.rpc_field(FAttr3)


@dataclass
class GETATTR3Res(rpchelp.Union):  # GETATTR3res
    SWITCH_OPTIONS = {None: None, NFS3_OK: 'resok'}
    status: typing.Union[NFSStat3, int] = rpchelp.rpc_field(NFSStat3)
    resok: typing.Optional[GETATTR3ResOK] = rpchelp.rpc_field(GETATTR3ResOK, default=None)


@dataclass
class Sattrguard3(rpchelp.Union):  # sattrguard3
    SWITCH_OPTIONS = {FALSE: None, TRUE: 'obj_ctime'}
    check: bool = rpchelp.rpc_field(rpchelp.r_bool)
    obj_ctime: typing.Optional[NFSTime3] = rpchelp.rpc_field(NFSTime3, default=None)


@dataclass
class SETATTR3Args(rpchelp.Struct):  # SETATTR3args
    obj_handle: bytes = rpchelp.rpc_field(NFSFh3)
    new_attributes: SAttr3 = rpchelp.rpc_field(SAttr3)
    guard: Sattrguard3 = rpchelp.rpc_field(Sattrguard3)


@dataclass
class SETATTR3ResOK(rpchelp.Struct):  # SETATTR3resok
    obj_wcc: WccData = rpchelp.rpc_field(WccData)


@dataclass
class SETATTR3ResFail(rpchelp.Struct):  # SETATTR3resfail
    obj_wcc: WccData = rpchelp.rpc_field(WccData)


@dataclass
class SETATTR3Res(rpchelp.Union):  # SETATTR3res
    SWITCH_OPTIONS = {None: 'resfail', NFS3_OK: 'resok'}
    status: typing.Union[NFSStat3, int] = rpchelp.rpc_field(NFSStat3)
    resfail: typing.Optional[SETATTR3ResFail] = rpchelp.rpc_field(SETATTR3ResFail, default=None)
    resok: typing.Optional[SETATTR3ResOK] = rpchelp.rpc_field(SETATTR3ResOK, default=None)


@dataclass
class LOOKUP3Args(rpchelp.Struct):  # LOOKUP3args
    what: DiropArgs3 = rpchelp.rpc_field(DiropArgs3)


@dataclass
class LOOKUP3ResOK(rpchelp.Struct):  # LOOKUP3resok
    obj_handle: bytes = rpchelp.rpc_field(NFSFh3)
    obj_attributes: typing.Optional[FAttr3] = rpchelp.rpc_field(PostOpAttr)
    dir_attributes: typing.Optional[FAttr3] = rpchelp.rpc_field(PostOpAttr)


@dataclass
class LOOKUP3ResFail(rpchelp.Struct):  # LOOKUP3resfail
    dir_attributes: typing.Optional[FAttr3] = rpchelp.rpc_field(PostOpAttr)


@dataclass
class LOOKUP3Res(rpchelp.Union):  # LOOKUP3res
    SWITCH_OPTIONS = {None: 'resfail', NFS3_OK: 'resok'}
    status: typing.Union[NFSStat3, int] = rpchelp.rpc_field(NFSStat3)
    resfail: typing.Optional[LOOKUP3ResFail] = rpchelp.rpc_field(LOOKUP3ResFail, default=None)
    resok: typing.Optional[LOOKUP3ResOK] = rpchelp.rpc_field(LOOKUP3ResOK, default=None)


ACCESS3_READ = 0x0001
ACCESS3_LOOKUP = 0x0002
ACCESS3_MODIFY = 0x0004
ACCESS3_EXTEND = 0x0008
ACCESS3_DELETE = 0x0010
ACCESS3_EXECUTE = 0x0020


@dataclass
class ACCESS3Args(rpchelp.Struct):  # ACCESS3args
    obj_handle: bytes = rpchelp.rpc_field(NFSFh3)
    access: int = rpchelp.rpc_field(Uint32)


@dataclass
class ACCESS3ResOK(rpchelp.Struct):  # ACCESS3resok
    obj_attributes: typing.Optional[FAttr3] = rpchelp.rpc_field(PostOpAttr)
    access: int = rpchelp.rpc_field(Uint32)


@dataclass
class ACCESS3ResFail(rpchelp.Struct):  # ACCESS3resfail
    obj_attributes: typing.Optional[FAttr3] = rpchelp.rpc_field(PostOpAttr)


@dataclass
class ACCESS3Res(rpchelp.Union):  # ACCESS3res
    SWITCH_OPTIONS = {None: 'resfail', NFS3_OK: 'resok'}
    status: typing.Union[NFSStat3, int] = rpchelp.rpc_field(NFSStat3)
    resfail: typing.Optional[ACCESS3ResFail] = rpchelp.rpc_field(ACCESS3ResFail, default=None)
    resok: typing.Optional[ACCESS3ResOK] = rpchelp.rpc_field(ACCESS3ResOK, default=None)


@dataclass
class READLINK3Args(rpchelp.Struct):  # READLINK3args
    symlink_handle: bytes = rpchelp.rpc_field(NFSFh3)


@dataclass
class READLINK3ResOK(rpchelp.Struct):  # READLINK3resok
    symlink_attributes: typing.Optional[FAttr3] = rpchelp.rpc_field(PostOpAttr)
    data: bytes = rpchelp.rpc_field(NFSPath3)


@dataclass
class READLINK3ResFail(rpchelp.Struct):  # READLINK3resfail
    symlink_attributes: typing.Optional[FAttr3] = rpchelp.rpc_field(PostOpAttr)


@dataclass
class READLINK3Res(rpchelp.Union):  # READLINK3res
    SWITCH_OPTIONS = {None: 'resfail', NFS3_OK: 'resok'}
    status: typing.Union[NFSStat3, int] = rpchelp.rpc_field(NFSStat3)
    resfail: typing.Optional[READLINK3ResFail] = rpchelp.rpc_field(READLINK3ResFail, default=None)
    resok: typing.Optional[READLINK3ResOK] = rpchelp.rpc_field(READLINK3ResOK, default=None)


@dataclass
class READ3Args(rpchelp.Struct):  # READ3args
    file_handle: bytes = rpchelp.rpc_field(NFSFh3)
    offset: int = rpchelp.rpc_field(Offset3)
    count: int = rpchelp.rpc_field(Count3)


@dataclass
class READ3ResOK(rpchelp.Struct):  # READ3resok
    file_attributes: typing.Optional[FAttr3] = rpchelp.rpc_field(PostOpAttr)
    count: int = rpchelp.rpc_field(Count3)
    eof: bool = rpchelp.rpc_field(rpchelp.r_bool)
    data: bytes = rpchelp.rpc_field(rpchelp.Opaque(rpchelp.LengthType.VAR, None))


@dataclass
class READ3ResFail(rpchelp.Struct):  # READ3resfail
    file_attributes: typing.Optional[FAttr3] = rpchelp.rpc_field(PostOpAttr)


@dataclass
class READ3Res(rpchelp.Union):  # READ3res
    SWITCH_OPTIONS = {None: 'resfail', NFS3_OK: 'resok'}
    status: typing.Union[NFSStat3, int] = rpchelp.rpc_field(NFSStat3)
    resfail: typing.Optional[READ3ResFail] = rpchelp.rpc_field(READ3ResFail, default=None)
    resok: typing.Optional[READ3ResOK] = rpchelp.rpc_field(READ3ResOK, default=None)


class StableHow(rpchelp.Enum):  # stable_how
    UNSTABLE = 0
    DATA_SYNC = 1
    FILE_SYNC = 2


@dataclass
class WRITE3Args(rpchelp.Struct):  # WRITE3args
    file_handle: bytes = rpchelp.rpc_field(NFSFh3)
    offset: int = rpchelp.rpc_field(Offset3)
    count: int = rpchelp.rpc_field(Count3)
    stable: typing.Union[StableHow, int] = rpchelp.rpc_field(StableHow)
    data: bytes = rpchelp.rpc_field(rpchelp.Opaque(rpchelp.LengthType.VAR, None))


@dataclass
class WRITE3ResOK(rpchelp.Struct):  # WRITE3resok
    file_wcc: WccData = rpchelp.rpc_field(WccData)
    count: int = rpchelp.rpc_field(Count3)
    committed: typing.Union[StableHow, int] = rpchelp.rpc_field(StableHow)
    verf: bytes = rpchelp.rpc_field(Writeverf3)


@dataclass
class WRITE3ResFail(rpchelp.Struct):  # WRITE3resfail
    file_wcc: WccData = rpchelp.rpc_field(WccData)


@dataclass
class WRITE3Res(rpchelp.Union):  # WRITE3res
    SWITCH_OPTIONS = {None: 'resfail', NFS3_OK: 'resok'}
    status: typing.Union[NFSStat3, int] = rpchelp.rpc_field(NFSStat3)
    resfail: typing.Optional[WRITE3ResFail] = rpchelp.rpc_field(WRITE3ResFail, default=None)
    resok: typing.Optional[WRITE3ResOK] = rpchelp.rpc_field(WRITE3ResOK, default=None)


class Createmode3(rpchelp.Enum):  # createmode3
    UNCHECKED = 0
    GUARDED = 1
    EXCLUSIVE = 2


@dataclass
class Createhow3(rpchelp.Union):  # createhow3
    SWITCH_OPTIONS = {UNCHECKED: 'obj_attributes', GUARDED: 'obj_attributes', EXCLUSIVE: 'verf'}
    mode: typing.Union[Createmode3, int] = rpchelp.rpc_field(Createmode3)
    obj_attributes: typing.Optional[SAttr3] = rpchelp.rpc_field(SAttr3, default=None)
    verf: typing.Optional[bytes] = rpchelp.rpc_field(Createverf3, default=None)


@dataclass
class CREATE3Args(rpchelp.Struct):  # CREATE3args
    where: DiropArgs3 = rpchelp.rpc_field(DiropArgs3)
    how: Createhow3 = rpchelp.rpc_field(Createhow3)


@dataclass
class CREATE3ResOK(rpchelp.Struct):  # CREATE3resok
    obj_handle: typing.Optional[bytes] = rpchelp.rpc_field(PostOpFh3)
    obj_attributes: typing.Optional[FAttr3] = rpchelp.rpc_field(PostOpAttr)
    dir_wcc: WccData = rpchelp.rpc_field(WccData)


@dataclass
class CREATE3ResFail(rpchelp.Struct):  # CREATE3resfail
    dir_wcc: WccData = rpchelp.rpc_field(WccData)


@dataclass
class CREATE3Res(rpchelp.Union):  # CREATE3res
    SWITCH_OPTIONS = {None: 'resfail', NFS3_OK: 'resok'}
    status: typing.Union[NFSStat3, int] = rpchelp.rpc_field(NFSStat3)
    resfail: typing.Optional[CREATE3ResFail] = rpchelp.rpc_field(CREATE3ResFail, default=None)
    resok: typing.Optional[CREATE3ResOK] = rpchelp.rpc_field(CREATE3ResOK, default=None)


@dataclass
class MKDIR3Args(rpchelp.Struct):  # MKDIR3args
    where: DiropArgs3 = rpchelp.rpc_field(DiropArgs3)
    attributes: SAttr3 = rpchelp.rpc_field(SAttr3)


@dataclass
class MKDIR3ResOK(rpchelp.Struct):  # MKDIR3resok
    obj_handle: typing.Optional[bytes] = rpchelp.rpc_field(PostOpFh3)
    obj_attributes: typing.Optional[FAttr3] = rpchelp.rpc_field(PostOpAttr)
    dir_wcc: WccData = rpchelp.rpc_field(WccData)


@dataclass
class MKDIR3ResFail(rpchelp.Struct):  # MKDIR3resfail
    dir_wcc: WccData = rpchelp.rpc_field(WccData)


@dataclass
class MKDIR3Res(rpchelp.Union):  # MKDIR3res
    SWITCH_OPTIONS = {None: 'resfail', NFS3_OK: 'resok'}
    status: typing.Union[NFSStat3, int] = rpchelp.rpc_field(NFSStat3)
    resfail: typing.Optional[MKDIR3ResFail] = rpchelp.rpc_field(MKDIR3ResFail, default=None)
    resok: typing.Optional[MKDIR3ResOK] = rpchelp.rpc_field(MKDIR3ResOK, default=None)


@dataclass
class SymlinkData3(rpchelp.Struct):  # symlinkdata3
    symlink_attributes: SAttr3 = rpchelp.rpc_field(SAttr3)
    symlink_data: bytes = rpchelp.rpc_field(NFSPath3)


@dataclass
class SYMLINK3Args(rpchelp.Struct):  # SYMLINK3args
    where: DiropArgs3 = rpchelp.rpc_field(DiropArgs3)
    symlink: SymlinkData3 = rpchelp.rpc_field(SymlinkData3)


@dataclass
class SYMLINK3ResOK(rpchelp.Struct):  # SYMLINK3resok
    obj_handle: typing.Optional[bytes] = rpchelp.rpc_field(PostOpFh3)
    obj_attributes: typing.Optional[FAttr3] = rpchelp.rpc_field(PostOpAttr)
    dir_wcc: WccData = rpchelp.rpc_field(WccData)


@dataclass
class SYMLINK3ResFail(rpchelp.Struct):  # SYMLINK3resfail
    dir_wcc: WccData = rpchelp.rpc_field(WccData)


@dataclass
class SYMLINK3Res(rpchelp.Union):  # SYMLINK3res
    SWITCH_OPTIONS = {None: 'resfail', NFS3_OK: 'resok'}
    status: typing.Union[NFSStat3, int] = rpchelp.rpc_field(NFSStat3)
    resfail: typing.Optional[SYMLINK3ResFail] = rpchelp.rpc_field(SYMLINK3ResFail, default=None)
    resok: typing.Optional[SYMLINK3ResOK] = rpchelp.rpc_field(SYMLINK3ResOK, default=None)


@dataclass
class DeviceData3(rpchelp.Struct):  # devicedata3
    dev_attributes: SAttr3 = rpchelp.rpc_field(SAttr3)
    spec: SpecData3 = rpchelp.rpc_field(SpecData3)


@dataclass
class MknodData3(rpchelp.Union):  # mknoddata3
    SWITCH_OPTIONS = {None: None, NF3BLK: 'blk_device', NF3CHR: 'chr_device', NF3FIFO: 'fifo_pipe_attributes', NF3SOCK: 'sock_pipe_attributes'}
    type: typing.Union[Ftype3, int] = rpchelp.rpc_field(Ftype3)
    blk_device: typing.Optional[DeviceData3] = rpchelp.rpc_field(DeviceData3, default=None)
    chr_device: typing.Optional[DeviceData3] = rpchelp.rpc_field(DeviceData3, default=None)
    fifo_pipe_attributes: typing.Optional[SAttr3] = rpchelp.rpc_field(SAttr3, default=None)
    sock_pipe_attributes: typing.Optional[SAttr3] = rpchelp.rpc_field(SAttr3, default=None)


@dataclass
class MKNOD3Args(rpchelp.Struct):  # MKNOD3args
    where: DiropArgs3 = rpchelp.rpc_field(DiropArgs3)
    what: MknodData3 = rpchelp.rpc_field(MknodData3)


@dataclass
class MKNOD3ResOK(rpchelp.Struct):  # MKNOD3resok
    obj_handle: typing.Optional[bytes] = rpchelp.rpc_field(PostOpFh3)
    obj_attributes: typing.Optional[FAttr3] = rpchelp.rpc_field(PostOpAttr)
    dir_wcc: WccData = rpchelp.rpc_field(WccData)


@dataclass
class MKNOD3ResFail(rpchelp.Struct):  # MKNOD3resfail
    dir_wcc: WccData = rpchelp.rpc_field(WccData)


@dataclass
class MKNOD3Res(rpchelp.Union):  # MKNOD3res
    SWITCH_OPTIONS = {None: 'resfail', NFS3_OK: 'resok'}
    status: typing.Union[NFSStat3, int] = rpchelp.rpc_field(NFSStat3)
    resfail: typing.Optional[MKNOD3ResFail] = rpchelp.rpc_field(MKNOD3ResFail, default=None)
    resok: typing.Optional[MKNOD3ResOK] = rpchelp.rpc_field(MKNOD3ResOK, default=None)


@dataclass
class REMOVE3Args(rpchelp.Struct):  # REMOVE3args
    object: DiropArgs3 = rpchelp.rpc_field(DiropArgs3)


@dataclass
class REMOVE3ResOK(rpchelp.Struct):  # REMOVE3resok
    dir_wcc: WccData = rpchelp.rpc_field(WccData)


@dataclass
class REMOVE3ResFail(rpchelp.Struct):  # REMOVE3resfail
    dir_wcc: WccData = rpchelp.rpc_field(WccData)


@dataclass
class REMOVE3Res(rpchelp.Union):  # REMOVE3res
    SWITCH_OPTIONS = {None: 'resfail', NFS3_OK: 'resok'}
    status: typing.Union[NFSStat3, int] = rpchelp.rpc_field(NFSStat3)
    resfail: typing.Optional[REMOVE3ResFail] = rpchelp.rpc_field(REMOVE3ResFail, default=None)
    resok: typing.Optional[REMOVE3ResOK] = rpchelp.rpc_field(REMOVE3ResOK, default=None)


@dataclass
class RMDIR3Args(rpchelp.Struct):  # RMDIR3args
    object: DiropArgs3 = rpchelp.rpc_field(DiropArgs3)


@dataclass
class RMDIR3ResOK(rpchelp.Struct):  # RMDIR3resok
    dir_wcc: WccData = rpchelp.rpc_field(WccData)


@dataclass
class RMDIR3ResFail(rpchelp.Struct):  # RMDIR3resfail
    dir_wcc: WccData = rpchelp.rpc_field(WccData)


@dataclass
class RMDIR3Res(rpchelp.Union):  # RMDIR3res
    SWITCH_OPTIONS = {None: 'resfail', NFS3_OK: 'resok'}
    status: typing.Union[NFSStat3, int] = rpchelp.rpc_field(NFSStat3)
    resfail: typing.Optional[RMDIR3ResFail] = rpchelp.rpc_field(RMDIR3ResFail, default=None)
    resok: typing.Optional[RMDIR3ResOK] = rpchelp.rpc_field(RMDIR3ResOK, default=None)


@dataclass
class RENAME3Args(rpchelp.Struct):  # RENAME3args
    from_: DiropArgs3 = rpchelp.rpc_field(DiropArgs3)
    to: DiropArgs3 = rpchelp.rpc_field(DiropArgs3)


@dataclass
class RENAME3ResOK(rpchelp.Struct):  # RENAME3resok
    fromdir_wcc: WccData = rpchelp.rpc_field(WccData)
    todir_wcc: WccData = rpchelp.rpc_field(WccData)


@dataclass
class RENAME3ResFail(rpchelp.Struct):  # RENAME3resfail
    fromdir_wcc: WccData = rpchelp.rpc_field(WccData)
    todir_wcc: WccData = rpchelp.rpc_field(WccData)


@dataclass
class RENAME3Res(rpchelp.Union):  # RENAME3res
    SWITCH_OPTIONS = {None: 'resfail', NFS3_OK: 'resok'}
    status: typing.Union[NFSStat3, int] = rpchelp.rpc_field(NFSStat3)
    resfail: typing.Optional[RENAME3ResFail] = rpchelp.rpc_field(RENAME3ResFail, default=None)
    resok: typing.Optional[RENAME3ResOK] = rpchelp.rpc_field(RENAME3ResOK, default=None)


@dataclass
class LINK3Args(rpchelp.Struct):  # LINK3args
    file_handle: bytes = rpchelp.rpc_field(NFSFh3)
    link: DiropArgs3 = rpchelp.rpc_field(DiropArgs3)


@dataclass
class LINK3ResOK(rpchelp.Struct):  # LINK3resok
    file_attributes: typing.Optional[FAttr3] = rpchelp.rpc_field(PostOpAttr)
    linkdir_wcc: WccData = rpchelp.rpc_field(WccData)


@dataclass
class LINK3ResFail(rpchelp.Struct):  # LINK3resfail
    file_attributes: typing.Optional[FAttr3] = rpchelp.rpc_field(PostOpAttr)
    linkdir_wcc: WccData = rpchelp.rpc_field(WccData)


@dataclass
class LINK3Res(rpchelp.Union):  # LINK3res
    SWITCH_OPTIONS = {None: 'resfail', NFS3_OK: 'resok'}
    status: typing.Union[NFSStat3, int] = rpchelp.rpc_field(NFSStat3)
    resfail: typing.Optional[LINK3ResFail] = rpchelp.rpc_field(LINK3ResFail, default=None)
    resok: typing.Optional[LINK3ResOK] = rpchelp.rpc_field(LINK3ResOK, default=None)


@dataclass
class READDIR3Args(rpchelp.Struct):  # READDIR3args
    dir_handle: bytes = rpchelp.rpc_field(NFSFh3)
    cookie: int = rpchelp.rpc_field(Cookie3)
    cookieverf: bytes = rpchelp.rpc_field(Cookieverf3)
    count: int = rpchelp.rpc_field(Count3)


@dataclass
class Entry3(rpchelp.LinkedList):  # entry3
    fileid: int = rpchelp.rpc_field(Fileid3)
    name: bytes = rpchelp.rpc_field(Filename3)
    cookie: int = rpchelp.rpc_field(Cookie3)


@dataclass
class DirList3(rpchelp.Struct):  # dirlist3
    entries: typing.List[Entry3] = rpchelp.rpc_field(rpchelp.OptData(Entry3))
    eof: bool = rpchelp.rpc_field(rpchelp.r_bool)


@dataclass
class READDIR3ResOK(rpchelp.Struct):  # READDIR3resok
    dir_attributes: typing.Optional[FAttr3] = rpchelp.rpc_field(PostOpAttr)
    cookieverf: bytes = rpchelp.rpc_field(Cookieverf3)
    reply: DirList3 = rpchelp.rpc_field(DirList3)


@dataclass
class READDIR3ResFail(rpchelp.Struct):  # READDIR3resfail
    dir_attributes: typing.Optional[FAttr3] = rpchelp.rpc_field(PostOpAttr)


@dataclass
class READDIR3Res(rpchelp.Union):  # READDIR3res
    SWITCH_OPTIONS = {None: 'resfail', NFS3_OK: 'resok'}
    status: typing.Union[NFSStat3, int] = rpchelp.rpc_field(NFSStat3)
    resfail: typing.Optional[READDIR3ResFail] = rpchelp.rpc_field(READDIR3ResFail, default=None)
    resok: typing.Optional[READDIR3ResOK] = rpchelp.rpc_field(READDIR3ResOK, default=None)


@dataclass
class READDIRPLUS3Args(rpchelp.Struct):  # READDIRPLUS3args
    dir_handle: bytes = rpchelp.rpc_field(NFSFh3)
    cookie: int = rpchelp.rpc_field(Cookie3)
    cookieverf: bytes = rpchelp.rpc_field(Cookieverf3)
    dircount: int = rpchelp.rpc_field(Count3)
    maxcount: int = rpchelp.rpc_field(Count3)


@dataclass
class Entryplus3(rpchelp.LinkedList):  # entryplus3
    fileid: int = rpchelp.rpc_field(Fileid3)
    name: bytes = rpchelp.rpc_field(Filename3)
    cookie: int = rpchelp.rpc_field(Cookie3)
    name_attributes: typing.Optional[FAttr3] = rpchelp.rpc_field(PostOpAttr)
    name_handle: typing.Optional[bytes] = rpchelp.rpc_field(PostOpFh3)


@dataclass
class Dirlistplus3(rpchelp.Struct):  # dirlistplus3
    entries: typing.List[Entryplus3] = rpchelp.rpc_field(rpchelp.OptData(Entryplus3))
    eof: bool = rpchelp.rpc_field(rpchelp.r_bool)


@dataclass
class READDIRPLUS3ResOK(rpchelp.Struct):  # READDIRPLUS3resok
    dir_attributes: typing.Optional[FAttr3] = rpchelp.rpc_field(PostOpAttr)
    cookieverf: bytes = rpchelp.rpc_field(Cookieverf3)
    reply: Dirlistplus3 = rpchelp.rpc_field(Dirlistplus3)


@dataclass
class READDIRPLUS3ResFail(rpchelp.Struct):  # READDIRPLUS3resfail
    dir_attributes: typing.Optional[FAttr3] = rpchelp.rpc_field(PostOpAttr)


@dataclass
class READDIRPLUS3Res(rpchelp.Union):  # READDIRPLUS3res
    SWITCH_OPTIONS = {None: 'resfail', NFS3_OK: 'resok'}
    status: typing.Union[NFSStat3, int] = rpchelp.rpc_field(NFSStat3)
    resfail: typing.Optional[READDIRPLUS3ResFail] = rpchelp.rpc_field(READDIRPLUS3ResFail, default=None)
    resok: typing.Optional[READDIRPLUS3ResOK] = rpchelp.rpc_field(READDIRPLUS3ResOK, default=None)


@dataclass
class FSSTAT3Args(rpchelp.Struct):  # FSSTAT3args
    fsroot_handle: bytes = rpchelp.rpc_field(NFSFh3)


@dataclass
class FSSTAT3ResOK(rpchelp.Struct):  # FSSTAT3resok
    obj_attributes: typing.Optional[FAttr3] = rpchelp.rpc_field(PostOpAttr)
    tbytes: int = rpchelp.rpc_field(Size3)
    fbytes: int = rpchelp.rpc_field(Size3)
    abytes: int = rpchelp.rpc_field(Size3)
    tfiles: int = rpchelp.rpc_field(Size3)
    ffiles: int = rpchelp.rpc_field(Size3)
    afiles: int = rpchelp.rpc_field(Size3)
    invarsec: int = rpchelp.rpc_field(Uint32)


@dataclass
class FSSTAT3ResFail(rpchelp.Struct):  # FSSTAT3resfail
    obj_attributes: typing.Optional[FAttr3] = rpchelp.rpc_field(PostOpAttr)


@dataclass
class FSSTAT3Res(rpchelp.Union):  # FSSTAT3res
    SWITCH_OPTIONS = {None: 'resfail', NFS3_OK: 'resok'}
    status: typing.Union[NFSStat3, int] = rpchelp.rpc_field(NFSStat3)
    resfail: typing.Optional[FSSTAT3ResFail] = rpchelp.rpc_field(FSSTAT3ResFail, default=None)
    resok: typing.Optional[FSSTAT3ResOK] = rpchelp.rpc_field(FSSTAT3ResOK, default=None)


FSF3_LINK = 0x0001
FSF3_SYMLINK = 0x0002
FSF3_HOMOGENEOUS = 0x0008
FSF3_CANSETTIME = 0x0010


@dataclass
class FSINFO3Args(rpchelp.Struct):  # FSINFO3args
    fsroot_handle: bytes = rpchelp.rpc_field(NFSFh3)


@dataclass
class FSINFO3ResOK(rpchelp.Struct):  # FSINFO3resok
    obj_attributes: typing.Optional[FAttr3] = rpchelp.rpc_field(PostOpAttr)
    rtmax: int = rpchelp.rpc_field(Uint32)
    rtpref: int = rpchelp.rpc_field(Uint32)
    rtmult: int = rpchelp.rpc_field(Uint32)
    wtmax: int = rpchelp.rpc_field(Uint32)
    wtpref: int = rpchelp.rpc_field(Uint32)
    wtmult: int = rpchelp.rpc_field(Uint32)
    dtpref: int = rpchelp.rpc_field(Uint32)
    maxfilesize: int = rpchelp.rpc_field(Size3)
    time_delta: NFSTime3 = rpchelp.rpc_field(NFSTime3)
    properties: int = rpchelp.rpc_field(Uint32)


@dataclass
class FSINFO3ResFail(rpchelp.Struct):  # FSINFO3resfail
    obj_attributes: typing.Optional[FAttr3] = rpchelp.rpc_field(PostOpAttr)


@dataclass
class FSINFO3Res(rpchelp.Union):  # FSINFO3res
    SWITCH_OPTIONS = {None: 'resfail', NFS3_OK: 'resok'}
    status: typing.Union[NFSStat3, int] = rpchelp.rpc_field(NFSStat3)
    resfail: typing.Optional[FSINFO3ResFail] = rpchelp.rpc_field(FSINFO3ResFail, default=None)
    resok: typing.Optional[FSINFO3ResOK] = rpchelp.rpc_field(FSINFO3ResOK, default=None)


@dataclass
class PATHCONF3Args(rpchelp.Struct):  # PATHCONF3args
    obj_handle: bytes = rpchelp.rpc_field(NFSFh3)


@dataclass
class PATHCONF3ResOK(rpchelp.Struct):  # PATHCONF3resok
    obj_attributes: typing.Optional[FAttr3] = rpchelp.rpc_field(PostOpAttr)
    linkmax: int = rpchelp.rpc_field(Uint32)
    name_max: int = rpchelp.rpc_field(Uint32)
    no_trunc: bool = rpchelp.rpc_field(rpchelp.r_bool)
    chown_restricted: bool = rpchelp.rpc_field(rpchelp.r_bool)
    case_insensitive: bool = rpchelp.rpc_field(rpchelp.r_bool)
    case_preserving: bool = rpchelp.rpc_field(rpchelp.r_bool)


@dataclass
class PATHCONF3ResFail(rpchelp.Struct):  # PATHCONF3resfail
    obj_attributes: typing.Optional[FAttr3] = rpchelp.rpc_field(PostOpAttr)


@dataclass
class PATHCONF3Res(rpchelp.Union):  # PATHCONF3res
    SWITCH_OPTIONS = {None: 'resfail', NFS3_OK: 'resok'}
    status: typing.Union[NFSStat3, int] = rpchelp.rpc_field(NFSStat3)
    resfail: typing.Optional[PATHCONF3ResFail] = rpchelp.rpc_field(PATHCONF3ResFail, default=None)
    resok: typing.Optional[PATHCONF3ResOK] = rpchelp.rpc_field(PATHCONF3ResOK, default=None)


@dataclass
class COMMIT3Args(rpchelp.Struct):  # COMMIT3args
    file_handle: bytes = rpchelp.rpc_field(NFSFh3)
    offset: int = rpchelp.rpc_field(Offset3)
    count: int = rpchelp.rpc_field(Count3)


@dataclass
class COMMIT3ResOK(rpchelp.Struct):  # COMMIT3resok
    file_wcc: WccData = rpchelp.rpc_field(WccData)
    verf: bytes = rpchelp.rpc_field(Writeverf3)


@dataclass
class COMMIT3ResFail(rpchelp.Struct):  # COMMIT3resfail
    file_wcc: WccData = rpchelp.rpc_field(WccData)


@dataclass
class COMMIT3Res(rpchelp.Union):  # COMMIT3res
    SWITCH_OPTIONS = {None: 'resfail', NFS3_OK: 'resok'}
    status: typing.Union[NFSStat3, int] = rpchelp.rpc_field(NFSStat3)
    resfail: typing.Optional[COMMIT3ResFail] = rpchelp.rpc_field(COMMIT3ResFail, default=None)
    resok: typing.Optional[COMMIT3ResOK] = rpchelp.rpc_field(COMMIT3ResOK, default=None)


MNTPATHLEN = 1024
MNTNAMLEN = 255
FHSIZE3 = 64
FHandle3 = rpchelp.Opaque(rpchelp.LengthType.VAR, FHSIZE3)
DirPath = rpchelp.Opaque(rpchelp.LengthType.VAR, MNTPATHLEN)
Name = rpchelp.Opaque(rpchelp.LengthType.VAR, MNTNAMLEN)


class MountStat3(rpchelp.Enum):  # mountstat3
    MNT3_OK = 0
    MNT3ERR_PERM = 1
    MNT3ERR_NOENT = 2
    MNT3ERR_IO = 5
    MNT3ERR_ACCES = 13
    MNT3ERR_NOTDIR = 20
    MNT3ERR_INVAL = 22
    MNT3ERR_NAMETOOLONG = 63
    MNT3ERR_NOTSUPP = 10004
    MNT3ERR_SERVERFAULT = 10006


@dataclass
class Mountres3OK(rpchelp.Struct):  # mountres3_ok
    fhandle: bytes = rpchelp.rpc_field(FHandle3)
    auth_flavors: typing.List[int] = rpchelp.rpc_field(rpchelp.Array(rpchelp.r_int, rpchelp.LengthType.VAR, None))


@dataclass
class MountRes3(rpchelp.Union):  # mountres3
    SWITCH_OPTIONS = {None: None, MNT3_OK: 'mountinfo'}
    fhs_status: typing.Union[MountStat3, int] = rpchelp.rpc_field(MountStat3)
    mountinfo: typing.Optional[Mountres3OK] = rpchelp.rpc_field(Mountres3OK, default=None)


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


class NFS_PROGRAM_3_SERVER(rpchelp.Prog):
    prog = 100003
    vers = 3
    procs = {
        0: rpchelp.Proc('NULL', rpchelp.r_void, []),
        1: rpchelp.Proc('GETATTR', GETATTR3Res, [GETATTR3Args]),
        2: rpchelp.Proc('SETATTR', SETATTR3Res, [SETATTR3Args]),
        3: rpchelp.Proc('LOOKUP', LOOKUP3Res, [LOOKUP3Args]),
        4: rpchelp.Proc('ACCESS', ACCESS3Res, [ACCESS3Args]),
        5: rpchelp.Proc('READLINK', READLINK3Res, [READLINK3Args]),
        6: rpchelp.Proc('READ', READ3Res, [READ3Args]),
        7: rpchelp.Proc('WRITE', WRITE3Res, [WRITE3Args]),
        8: rpchelp.Proc('CREATE', CREATE3Res, [CREATE3Args]),
        9: rpchelp.Proc('MKDIR', MKDIR3Res, [MKDIR3Args]),
        10: rpchelp.Proc('SYMLINK', SYMLINK3Res, [SYMLINK3Args]),
        11: rpchelp.Proc('MKNOD', MKNOD3Res, [MKNOD3Args]),
        12: rpchelp.Proc('REMOVE', REMOVE3Res, [REMOVE3Args]),
        13: rpchelp.Proc('RMDIR', RMDIR3Res, [RMDIR3Args]),
        14: rpchelp.Proc('RENAME', RENAME3Res, [RENAME3Args]),
        15: rpchelp.Proc('LINK', LINK3Res, [LINK3Args]),
        16: rpchelp.Proc('READDIR', READDIR3Res, [READDIR3Args]),
        17: rpchelp.Proc('READDIRPLUS', READDIRPLUS3Res, [READDIRPLUS3Args]),
        18: rpchelp.Proc('FSSTAT', FSSTAT3Res, [FSSTAT3Args]),
        19: rpchelp.Proc('FSINFO', FSINFO3Res, [FSINFO3Args]),
        20: rpchelp.Proc('PATHCONF', PATHCONF3Res, [PATHCONF3Args]),
        21: rpchelp.Proc('COMMIT', COMMIT3Res, [COMMIT3Args]),
    }

    @abc.abstractmethod
    async def NULL(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def GETATTR(self, arg_0: GETATTR3Args) -> GETATTR3Res:
        raise NotImplementedError()

    @abc.abstractmethod
    async def SETATTR(self, arg_0: SETATTR3Args) -> SETATTR3Res:
        raise NotImplementedError()

    @abc.abstractmethod
    async def LOOKUP(self, arg_0: LOOKUP3Args) -> LOOKUP3Res:
        raise NotImplementedError()

    @abc.abstractmethod
    async def ACCESS(self, arg_0: ACCESS3Args) -> ACCESS3Res:
        raise NotImplementedError()

    @abc.abstractmethod
    async def READLINK(self, arg_0: READLINK3Args) -> READLINK3Res:
        raise NotImplementedError()

    @abc.abstractmethod
    async def READ(self, arg_0: READ3Args) -> READ3Res:
        raise NotImplementedError()

    @abc.abstractmethod
    async def WRITE(self, arg_0: WRITE3Args) -> WRITE3Res:
        raise NotImplementedError()

    @abc.abstractmethod
    async def CREATE(self, arg_0: CREATE3Args) -> CREATE3Res:
        raise NotImplementedError()

    @abc.abstractmethod
    async def MKDIR(self, arg_0: MKDIR3Args) -> MKDIR3Res:
        raise NotImplementedError()

    @abc.abstractmethod
    async def SYMLINK(self, arg_0: SYMLINK3Args) -> SYMLINK3Res:
        raise NotImplementedError()

    @abc.abstractmethod
    async def MKNOD(self, arg_0: MKNOD3Args) -> MKNOD3Res:
        raise NotImplementedError()

    @abc.abstractmethod
    async def REMOVE(self, arg_0: REMOVE3Args) -> REMOVE3Res:
        raise NotImplementedError()

    @abc.abstractmethod
    async def RMDIR(self, arg_0: RMDIR3Args) -> RMDIR3Res:
        raise NotImplementedError()

    @abc.abstractmethod
    async def RENAME(self, arg_0: RENAME3Args) -> RENAME3Res:
        raise NotImplementedError()

    @abc.abstractmethod
    async def LINK(self, arg_0: LINK3Args) -> LINK3Res:
        raise NotImplementedError()

    @abc.abstractmethod
    async def READDIR(self, arg_0: READDIR3Args) -> READDIR3Res:
        raise NotImplementedError()

    @abc.abstractmethod
    async def READDIRPLUS(self, arg_0: READDIRPLUS3Args) -> READDIRPLUS3Res:
        raise NotImplementedError()

    @abc.abstractmethod
    async def FSSTAT(self, arg_0: FSSTAT3Args) -> FSSTAT3Res:
        raise NotImplementedError()

    @abc.abstractmethod
    async def FSINFO(self, arg_0: FSINFO3Args) -> FSINFO3Res:
        raise NotImplementedError()

    @abc.abstractmethod
    async def PATHCONF(self, arg_0: PATHCONF3Args) -> PATHCONF3Res:
        raise NotImplementedError()

    @abc.abstractmethod
    async def COMMIT(self, arg_0: COMMIT3Args) -> COMMIT3Res:
        raise NotImplementedError()


class NFS_PROGRAM_3_CLIENT(client.BaseClient):
    prog = 100003
    vers = 3
    procs = {
        0: rpchelp.Proc('NULL', rpchelp.r_void, []),
        1: rpchelp.Proc('GETATTR', GETATTR3Res, [GETATTR3Args]),
        2: rpchelp.Proc('SETATTR', SETATTR3Res, [SETATTR3Args]),
        3: rpchelp.Proc('LOOKUP', LOOKUP3Res, [LOOKUP3Args]),
        4: rpchelp.Proc('ACCESS', ACCESS3Res, [ACCESS3Args]),
        5: rpchelp.Proc('READLINK', READLINK3Res, [READLINK3Args]),
        6: rpchelp.Proc('READ', READ3Res, [READ3Args]),
        7: rpchelp.Proc('WRITE', WRITE3Res, [WRITE3Args]),
        8: rpchelp.Proc('CREATE', CREATE3Res, [CREATE3Args]),
        9: rpchelp.Proc('MKDIR', MKDIR3Res, [MKDIR3Args]),
        10: rpchelp.Proc('SYMLINK', SYMLINK3Res, [SYMLINK3Args]),
        11: rpchelp.Proc('MKNOD', MKNOD3Res, [MKNOD3Args]),
        12: rpchelp.Proc('REMOVE', REMOVE3Res, [REMOVE3Args]),
        13: rpchelp.Proc('RMDIR', RMDIR3Res, [RMDIR3Args]),
        14: rpchelp.Proc('RENAME', RENAME3Res, [RENAME3Args]),
        15: rpchelp.Proc('LINK', LINK3Res, [LINK3Args]),
        16: rpchelp.Proc('READDIR', READDIR3Res, [READDIR3Args]),
        17: rpchelp.Proc('READDIRPLUS', READDIRPLUS3Res, [READDIRPLUS3Args]),
        18: rpchelp.Proc('FSSTAT', FSSTAT3Res, [FSSTAT3Args]),
        19: rpchelp.Proc('FSINFO', FSINFO3Res, [FSINFO3Args]),
        20: rpchelp.Proc('PATHCONF', PATHCONF3Res, [PATHCONF3Args]),
        21: rpchelp.Proc('COMMIT', COMMIT3Res, [COMMIT3Args]),
    }

    async def NULL(self) -> client.UnpackedRPCMsg[None]:
        return await self.send_call(0, )

    async def GETATTR(self, arg_0: GETATTR3Args) -> client.UnpackedRPCMsg[GETATTR3Res]:
        return await self.send_call(1, arg_0)

    async def SETATTR(self, arg_0: SETATTR3Args) -> client.UnpackedRPCMsg[SETATTR3Res]:
        return await self.send_call(2, arg_0)

    async def LOOKUP(self, arg_0: LOOKUP3Args) -> client.UnpackedRPCMsg[LOOKUP3Res]:
        return await self.send_call(3, arg_0)

    async def ACCESS(self, arg_0: ACCESS3Args) -> client.UnpackedRPCMsg[ACCESS3Res]:
        return await self.send_call(4, arg_0)

    async def READLINK(self, arg_0: READLINK3Args) -> client.UnpackedRPCMsg[READLINK3Res]:
        return await self.send_call(5, arg_0)

    async def READ(self, arg_0: READ3Args) -> client.UnpackedRPCMsg[READ3Res]:
        return await self.send_call(6, arg_0)

    async def WRITE(self, arg_0: WRITE3Args) -> client.UnpackedRPCMsg[WRITE3Res]:
        return await self.send_call(7, arg_0)

    async def CREATE(self, arg_0: CREATE3Args) -> client.UnpackedRPCMsg[CREATE3Res]:
        return await self.send_call(8, arg_0)

    async def MKDIR(self, arg_0: MKDIR3Args) -> client.UnpackedRPCMsg[MKDIR3Res]:
        return await self.send_call(9, arg_0)

    async def SYMLINK(self, arg_0: SYMLINK3Args) -> client.UnpackedRPCMsg[SYMLINK3Res]:
        return await self.send_call(10, arg_0)

    async def MKNOD(self, arg_0: MKNOD3Args) -> client.UnpackedRPCMsg[MKNOD3Res]:
        return await self.send_call(11, arg_0)

    async def REMOVE(self, arg_0: REMOVE3Args) -> client.UnpackedRPCMsg[REMOVE3Res]:
        return await self.send_call(12, arg_0)

    async def RMDIR(self, arg_0: RMDIR3Args) -> client.UnpackedRPCMsg[RMDIR3Res]:
        return await self.send_call(13, arg_0)

    async def RENAME(self, arg_0: RENAME3Args) -> client.UnpackedRPCMsg[RENAME3Res]:
        return await self.send_call(14, arg_0)

    async def LINK(self, arg_0: LINK3Args) -> client.UnpackedRPCMsg[LINK3Res]:
        return await self.send_call(15, arg_0)

    async def READDIR(self, arg_0: READDIR3Args) -> client.UnpackedRPCMsg[READDIR3Res]:
        return await self.send_call(16, arg_0)

    async def READDIRPLUS(self, arg_0: READDIRPLUS3Args) -> client.UnpackedRPCMsg[READDIRPLUS3Res]:
        return await self.send_call(17, arg_0)

    async def FSSTAT(self, arg_0: FSSTAT3Args) -> client.UnpackedRPCMsg[FSSTAT3Res]:
        return await self.send_call(18, arg_0)

    async def FSINFO(self, arg_0: FSINFO3Args) -> client.UnpackedRPCMsg[FSINFO3Res]:
        return await self.send_call(19, arg_0)

    async def PATHCONF(self, arg_0: PATHCONF3Args) -> client.UnpackedRPCMsg[PATHCONF3Res]:
        return await self.send_call(20, arg_0)

    async def COMMIT(self, arg_0: COMMIT3Args) -> client.UnpackedRPCMsg[COMMIT3Res]:
        return await self.send_call(21, arg_0)


class MOUNT_PROGRAM_3_SERVER(rpchelp.Prog):
    prog = 100005
    vers = 3
    procs = {
        0: rpchelp.Proc('NULL', rpchelp.r_void, []),
        1: rpchelp.Proc('MNT', MountRes3, [DirPath]),
        2: rpchelp.Proc('DUMP', MountList, []),
        3: rpchelp.Proc('UMNT', rpchelp.r_void, [DirPath]),
        4: rpchelp.Proc('UMNTALL', rpchelp.r_void, []),
        5: rpchelp.Proc('EXPORT', ExportList, []),
    }

    @abc.abstractmethod
    async def NULL(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def MNT(self, arg_0: bytes) -> MountRes3:
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


class MOUNT_PROGRAM_3_CLIENT(client.BaseClient):
    prog = 100005
    vers = 3
    procs = {
        0: rpchelp.Proc('NULL', rpchelp.r_void, []),
        1: rpchelp.Proc('MNT', MountRes3, [DirPath]),
        2: rpchelp.Proc('DUMP', MountList, []),
        3: rpchelp.Proc('UMNT', rpchelp.r_void, [DirPath]),
        4: rpchelp.Proc('UMNTALL', rpchelp.r_void, []),
        5: rpchelp.Proc('EXPORT', ExportList, []),
    }

    async def NULL(self) -> client.UnpackedRPCMsg[None]:
        return await self.send_call(0, )

    async def MNT(self, arg_0: bytes) -> client.UnpackedRPCMsg[MountRes3]:
        return await self.send_call(1, arg_0)

    async def DUMP(self) -> client.UnpackedRPCMsg[typing.List[MountList]]:
        return await self.send_call(2, )

    async def UMNT(self, arg_0: bytes) -> client.UnpackedRPCMsg[None]:
        return await self.send_call(3, arg_0)

    async def UMNTALL(self) -> client.UnpackedRPCMsg[None]:
        return await self.send_call(4, )

    async def EXPORT(self) -> client.UnpackedRPCMsg[typing.List[ExportList]]:
        return await self.send_call(5, )


__all__ = ['NFS_PROGRAM_3_SERVER', 'NFS_PROGRAM_3_CLIENT', 'MOUNT_PROGRAM_3_SERVER', 'MOUNT_PROGRAM_3_CLIENT', 'TRUE', 'FALSE', 'NFS3_FHSIZE', 'NFS3_COOKIEVERFSIZE', 'NFS3_CREATEVERFSIZE', 'NFS3_WRITEVERFSIZE', 'NFS3_OK', 'NFS3ERR_PERM', 'NFS3ERR_NOENT', 'NFS3ERR_IO', 'NFS3ERR_NXIO', 'NFS3ERR_ACCES', 'NFS3ERR_EXIST', 'NFS3ERR_XDEV', 'NFS3ERR_NODEV', 'NFS3ERR_NOTDIR', 'NFS3ERR_ISDIR', 'NFS3ERR_INVAL', 'NFS3ERR_FBIG', 'NFS3ERR_NOSPC', 'NFS3ERR_ROFS', 'NFS3ERR_MLINK', 'NFS3ERR_NAMETOOLONG', 'NFS3ERR_NOTEMPTY', 'NFS3ERR_DQUOT', 'NFS3ERR_STALE', 'NFS3ERR_REMOTE', 'NFS3ERR_BADHANDLE', 'NFS3ERR_NOT_SYNC', 'NFS3ERR_BAD_COOKIE', 'NFS3ERR_NOTSUPP', 'NFS3ERR_TOOSMALL', 'NFS3ERR_SERVERFAULT', 'NFS3ERR_BADTYPE', 'NFS3ERR_JUKEBOX', 'NF3REG', 'NF3DIR', 'NF3BLK', 'NF3CHR', 'NF3LNK', 'NF3SOCK', 'NF3FIFO', 'DONT_CHANGE', 'SET_TO_SERVER_TIME', 'SET_TO_CLIENT_TIME', 'ACCESS3_READ', 'ACCESS3_LOOKUP', 'ACCESS3_MODIFY', 'ACCESS3_EXTEND', 'ACCESS3_DELETE', 'ACCESS3_EXECUTE', 'UNSTABLE', 'DATA_SYNC', 'FILE_SYNC', 'UNCHECKED', 'GUARDED', 'EXCLUSIVE', 'FSF3_LINK', 'FSF3_SYMLINK', 'FSF3_HOMOGENEOUS', 'FSF3_CANSETTIME', 'MNTPATHLEN', 'MNTNAMLEN', 'FHSIZE3', 'MNT3_OK', 'MNT3ERR_PERM', 'MNT3ERR_NOENT', 'MNT3ERR_IO', 'MNT3ERR_ACCES', 'MNT3ERR_NOTDIR', 'MNT3ERR_INVAL', 'MNT3ERR_NAMETOOLONG', 'MNT3ERR_NOTSUPP', 'MNT3ERR_SERVERFAULT', 'Uint64', 'Int64', 'Uint32', 'Int32', 'Filename3', 'NFSPath3', 'Fileid3', 'Cookie3', 'Cookieverf3', 'Createverf3', 'Writeverf3', 'Uid3', 'Gid3', 'Size3', 'Offset3', 'Mode3', 'Count3', 'NFSStat3', 'Ftype3', 'SpecData3', 'NFSFh3', 'NFSTime3', 'FAttr3', 'WccAttr', 'PostOpAttr', 'PreOpAttr', 'WccData', 'PostOpFh3', 'TimeHow', 'SetMode3', 'SetUid3', 'SetGid3', 'SetSize3', 'SetTime', 'SAttr3', 'DiropArgs3', 'GETATTR3Args', 'GETATTR3ResOK', 'GETATTR3Res', 'Sattrguard3', 'SETATTR3Args', 'SETATTR3ResOK', 'SETATTR3ResFail', 'SETATTR3Res', 'LOOKUP3Args', 'LOOKUP3ResOK', 'LOOKUP3ResFail', 'LOOKUP3Res', 'ACCESS3Args', 'ACCESS3ResOK', 'ACCESS3ResFail', 'ACCESS3Res', 'READLINK3Args', 'READLINK3ResOK', 'READLINK3ResFail', 'READLINK3Res', 'READ3Args', 'READ3ResOK', 'READ3ResFail', 'READ3Res', 'StableHow', 'WRITE3Args', 'WRITE3ResOK', 'WRITE3ResFail', 'WRITE3Res', 'Createmode3', 'Createhow3', 'CREATE3Args', 'CREATE3ResOK', 'CREATE3ResFail', 'CREATE3Res', 'MKDIR3Args', 'MKDIR3ResOK', 'MKDIR3ResFail', 'MKDIR3Res', 'SymlinkData3', 'SYMLINK3Args', 'SYMLINK3ResOK', 'SYMLINK3ResFail', 'SYMLINK3Res', 'DeviceData3', 'MknodData3', 'MKNOD3Args', 'MKNOD3ResOK', 'MKNOD3ResFail', 'MKNOD3Res', 'REMOVE3Args', 'REMOVE3ResOK', 'REMOVE3ResFail', 'REMOVE3Res', 'RMDIR3Args', 'RMDIR3ResOK', 'RMDIR3ResFail', 'RMDIR3Res', 'RENAME3Args', 'RENAME3ResOK', 'RENAME3ResFail', 'RENAME3Res', 'LINK3Args', 'LINK3ResOK', 'LINK3ResFail', 'LINK3Res', 'READDIR3Args', 'Entry3', 'DirList3', 'READDIR3ResOK', 'READDIR3ResFail', 'READDIR3Res', 'READDIRPLUS3Args', 'Entryplus3', 'Dirlistplus3', 'READDIRPLUS3ResOK', 'READDIRPLUS3ResFail', 'READDIRPLUS3Res', 'FSSTAT3Args', 'FSSTAT3ResOK', 'FSSTAT3ResFail', 'FSSTAT3Res', 'FSINFO3Args', 'FSINFO3ResOK', 'FSINFO3ResFail', 'FSINFO3Res', 'PATHCONF3Args', 'PATHCONF3ResOK', 'PATHCONF3ResFail', 'PATHCONF3Res', 'COMMIT3Args', 'COMMIT3ResOK', 'COMMIT3ResFail', 'COMMIT3Res', 'FHandle3', 'DirPath', 'Name', 'MountStat3', 'Mountres3OK', 'MountRes3', 'MountList', 'GroupList', 'ExportList']
