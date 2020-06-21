# Auto-generated from IDL file
import abc
import dataclasses
import typing
from dataclasses import dataclass

from pynefs import rpchelp

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
uint64 = rpchelp.r_uhyper
int64 = rpchelp.r_hyper
uint32 = rpchelp.r_uint
int32 = rpchelp.r_int
filename3 = rpchelp.string(rpchelp.LengthType.VAR, None)
nfspath3 = rpchelp.string(rpchelp.LengthType.VAR, None)
fileid3 = uint64
cookie3 = uint64
cookieverf3 = rpchelp.opaque(rpchelp.LengthType.FIXED, NFS3_COOKIEVERFSIZE)
createverf3 = rpchelp.opaque(rpchelp.LengthType.FIXED, NFS3_CREATEVERFSIZE)
writeverf3 = rpchelp.opaque(rpchelp.LengthType.FIXED, NFS3_WRITEVERFSIZE)
uid3 = uint32
gid3 = uint32
size3 = uint64
offset3 = uint64
mode3 = uint32
count3 = uint32


class nfsstat3(rpchelp.enum):
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


class ftype3(rpchelp.enum):
    NF3REG = 1
    NF3DIR = 2
    NF3BLK = 3
    NF3CHR = 4
    NF3LNK = 5
    NF3SOCK = 6
    NF3FIFO = 7


@dataclass
class specdata3(rpchelp.struct):
    specdata1: int = rpchelp.rpc_field(uint32)
    specdata2: int = rpchelp.rpc_field(uint32)


nfs_fh3 = rpchelp.opaque(rpchelp.LengthType.VAR, NFS3_FHSIZE)


@dataclass
class nfstime3(rpchelp.struct):
    seconds: int = rpchelp.rpc_field(uint32)
    nseconds: int = rpchelp.rpc_field(uint32)


@dataclass
class fattr3(rpchelp.struct):
    type: ftype3 = rpchelp.rpc_field(ftype3)
    mode: int = rpchelp.rpc_field(mode3)
    nlink: int = rpchelp.rpc_field(uint32)
    uid: int = rpchelp.rpc_field(uid3)
    gid: int = rpchelp.rpc_field(gid3)
    size: int = rpchelp.rpc_field(size3)
    used: int = rpchelp.rpc_field(size3)
    rdev: specdata3 = rpchelp.rpc_field(specdata3)
    fsid: int = rpchelp.rpc_field(uint64)
    fileid: int = rpchelp.rpc_field(fileid3)
    atime: nfstime3 = rpchelp.rpc_field(nfstime3)
    mtime: nfstime3 = rpchelp.rpc_field(nfstime3)
    ctime: nfstime3 = rpchelp.rpc_field(nfstime3)


@dataclass
class wcc_attr(rpchelp.struct):
    size: int = rpchelp.rpc_field(size3)
    mtime: nfstime3 = rpchelp.rpc_field(nfstime3)
    ctime: nfstime3 = rpchelp.rpc_field(nfstime3)


post_op_attr = rpchelp.opt_data(fattr3)
pre_op_attr = rpchelp.opt_data(wcc_attr)


@dataclass
class wcc_data(rpchelp.struct):
    before: typing.Optional[wcc_attr] = rpchelp.rpc_field(pre_op_attr)
    after: typing.Optional[fattr3] = rpchelp.rpc_field(post_op_attr)


post_op_fh3 = rpchelp.opt_data(nfs_fh3)


class time_how(rpchelp.enum):
    DONT_CHANGE = 0
    SET_TO_SERVER_TIME = 1
    SET_TO_CLIENT_TIME = 2


set_mode3 = rpchelp.opt_data(mode3)
set_uid3 = rpchelp.opt_data(uid3)
set_gid3 = rpchelp.opt_data(gid3)
set_size3 = rpchelp.opt_data(size3)


@dataclass
class set_atime(rpchelp.union):
    SWITCH_OPTIONS = {SET_TO_CLIENT_TIME: 'atime', None: None}
    set_it: time_how = rpchelp.rpc_field(time_how)
    atime: typing.Optional[nfstime3] = rpchelp.rpc_field(nfstime3, default=None)


@dataclass
class set_mtime(rpchelp.union):
    SWITCH_OPTIONS = {SET_TO_CLIENT_TIME: 'mtime', None: None}
    set_it: time_how = rpchelp.rpc_field(time_how)
    mtime: typing.Optional[nfstime3] = rpchelp.rpc_field(nfstime3, default=None)


@dataclass
class sattr3(rpchelp.struct):
    mode: typing.Optional[int] = rpchelp.rpc_field(set_mode3)
    uid: typing.Optional[int] = rpchelp.rpc_field(set_uid3)
    gid: typing.Optional[int] = rpchelp.rpc_field(set_gid3)
    size: typing.Optional[int] = rpchelp.rpc_field(set_size3)
    atime: set_atime = rpchelp.rpc_field(set_atime)
    mtime: set_mtime = rpchelp.rpc_field(set_mtime)


@dataclass
class diropargs3(rpchelp.struct):
    dir_handle: bytes = rpchelp.rpc_field(nfs_fh3)
    name: bytes = rpchelp.rpc_field(filename3)


@dataclass
class GETATTR3args(rpchelp.struct):
    obj_handle: bytes = rpchelp.rpc_field(nfs_fh3)


@dataclass
class GETATTR3resok(rpchelp.struct):
    obj_attributes: fattr3 = rpchelp.rpc_field(fattr3)


@dataclass
class GETATTR3res(rpchelp.union):
    SWITCH_OPTIONS = {NFS3_OK: 'resok', None: None}
    status: nfsstat3 = rpchelp.rpc_field(nfsstat3)
    resok: typing.Optional[GETATTR3resok] = rpchelp.rpc_field(GETATTR3resok, default=None)


@dataclass
class sattrguard3(rpchelp.union):
    SWITCH_OPTIONS = {TRUE: 'obj_ctime', FALSE: None}
    check: bool = rpchelp.rpc_field(rpchelp.r_bool)
    obj_ctime: typing.Optional[nfstime3] = rpchelp.rpc_field(nfstime3, default=None)


@dataclass
class SETATTR3args(rpchelp.struct):
    obj_handle: bytes = rpchelp.rpc_field(nfs_fh3)
    new_attributes: sattr3 = rpchelp.rpc_field(sattr3)
    guard: sattrguard3 = rpchelp.rpc_field(sattrguard3)


@dataclass
class SETATTR3resok(rpchelp.struct):
    obj_wcc: wcc_data = rpchelp.rpc_field(wcc_data)


@dataclass
class SETATTR3resfail(rpchelp.struct):
    obj_wcc: wcc_data = rpchelp.rpc_field(wcc_data)


@dataclass
class SETATTR3res(rpchelp.union):
    SWITCH_OPTIONS = {NFS3_OK: 'resok', None: 'resfail'}
    status: nfsstat3 = rpchelp.rpc_field(nfsstat3)
    resok: typing.Optional[SETATTR3resok] = rpchelp.rpc_field(SETATTR3resok, default=None)
    resfail: typing.Optional[SETATTR3resfail] = rpchelp.rpc_field(SETATTR3resfail, default=None)


@dataclass
class LOOKUP3args(rpchelp.struct):
    what: diropargs3 = rpchelp.rpc_field(diropargs3)


@dataclass
class LOOKUP3resok(rpchelp.struct):
    obj_handle: bytes = rpchelp.rpc_field(nfs_fh3)
    obj_attributes: typing.Optional[fattr3] = rpchelp.rpc_field(post_op_attr)
    dir_attributes: typing.Optional[fattr3] = rpchelp.rpc_field(post_op_attr)


@dataclass
class LOOKUP3resfail(rpchelp.struct):
    dir_attributes: typing.Optional[fattr3] = rpchelp.rpc_field(post_op_attr)


@dataclass
class LOOKUP3res(rpchelp.union):
    SWITCH_OPTIONS = {NFS3_OK: 'resok', None: 'resfail'}
    status: nfsstat3 = rpchelp.rpc_field(nfsstat3)
    resok: typing.Optional[LOOKUP3resok] = rpchelp.rpc_field(LOOKUP3resok, default=None)
    resfail: typing.Optional[LOOKUP3resfail] = rpchelp.rpc_field(LOOKUP3resfail, default=None)


ACCESS3_READ = 0x0001
ACCESS3_LOOKUP = 0x0002
ACCESS3_MODIFY = 0x0004
ACCESS3_EXTEND = 0x0008
ACCESS3_DELETE = 0x0010
ACCESS3_EXECUTE = 0x0020


@dataclass
class ACCESS3args(rpchelp.struct):
    obj_handle: bytes = rpchelp.rpc_field(nfs_fh3)
    access: int = rpchelp.rpc_field(uint32)


@dataclass
class ACCESS3resok(rpchelp.struct):
    obj_attributes: typing.Optional[fattr3] = rpchelp.rpc_field(post_op_attr)
    access: int = rpchelp.rpc_field(uint32)


@dataclass
class ACCESS3resfail(rpchelp.struct):
    obj_attributes: typing.Optional[fattr3] = rpchelp.rpc_field(post_op_attr)


@dataclass
class ACCESS3res(rpchelp.union):
    SWITCH_OPTIONS = {NFS3_OK: 'resok', None: 'resfail'}
    status: nfsstat3 = rpchelp.rpc_field(nfsstat3)
    resok: typing.Optional[ACCESS3resok] = rpchelp.rpc_field(ACCESS3resok, default=None)
    resfail: typing.Optional[ACCESS3resfail] = rpchelp.rpc_field(ACCESS3resfail, default=None)


@dataclass
class READLINK3args(rpchelp.struct):
    symlink_handle: bytes = rpchelp.rpc_field(nfs_fh3)


@dataclass
class READLINK3resok(rpchelp.struct):
    symlink_attributes: typing.Optional[fattr3] = rpchelp.rpc_field(post_op_attr)
    data: bytes = rpchelp.rpc_field(nfspath3)


@dataclass
class READLINK3resfail(rpchelp.struct):
    symlink_attributes: typing.Optional[fattr3] = rpchelp.rpc_field(post_op_attr)


@dataclass
class READLINK3res(rpchelp.union):
    SWITCH_OPTIONS = {NFS3_OK: 'resok', None: 'resfail'}
    status: nfsstat3 = rpchelp.rpc_field(nfsstat3)
    resok: typing.Optional[READLINK3resok] = rpchelp.rpc_field(READLINK3resok, default=None)
    resfail: typing.Optional[READLINK3resfail] = rpchelp.rpc_field(READLINK3resfail, default=None)


@dataclass
class READ3args(rpchelp.struct):
    file_handle: bytes = rpchelp.rpc_field(nfs_fh3)
    offset: int = rpchelp.rpc_field(offset3)
    count: int = rpchelp.rpc_field(count3)


@dataclass
class READ3resok(rpchelp.struct):
    file_attributes: typing.Optional[fattr3] = rpchelp.rpc_field(post_op_attr)
    count: int = rpchelp.rpc_field(count3)
    eof: bool = rpchelp.rpc_field(rpchelp.r_bool)
    data: bytes = rpchelp.rpc_field(rpchelp.opaque(rpchelp.LengthType.VAR, None))


@dataclass
class READ3resfail(rpchelp.struct):
    file_attributes: typing.Optional[fattr3] = rpchelp.rpc_field(post_op_attr)


@dataclass
class READ3res(rpchelp.union):
    SWITCH_OPTIONS = {NFS3_OK: 'resok', None: 'resfail'}
    status: nfsstat3 = rpchelp.rpc_field(nfsstat3)
    resfail: typing.Optional[READ3resfail] = rpchelp.rpc_field(READ3resfail, default=None)
    resok: typing.Optional[READ3resok] = rpchelp.rpc_field(READ3resok, default=None)


class stable_how(rpchelp.enum):
    UNSTABLE = 0
    DATA_SYNC = 1
    FILE_SYNC = 2


@dataclass
class WRITE3args(rpchelp.struct):
    file_handle: bytes = rpchelp.rpc_field(nfs_fh3)
    offset: int = rpchelp.rpc_field(offset3)
    count: int = rpchelp.rpc_field(count3)
    stable: stable_how = rpchelp.rpc_field(stable_how)
    data: bytes = rpchelp.rpc_field(rpchelp.opaque(rpchelp.LengthType.VAR, None))


@dataclass
class WRITE3resok(rpchelp.struct):
    file_wcc: wcc_data = rpchelp.rpc_field(wcc_data)
    count: int = rpchelp.rpc_field(count3)
    committed: stable_how = rpchelp.rpc_field(stable_how)
    verf: bytes = rpchelp.rpc_field(writeverf3)


@dataclass
class WRITE3resfail(rpchelp.struct):
    file_wcc: wcc_data = rpchelp.rpc_field(wcc_data)


@dataclass
class WRITE3res(rpchelp.union):
    SWITCH_OPTIONS = {NFS3_OK: 'resok', None: 'resfail'}
    status: nfsstat3 = rpchelp.rpc_field(nfsstat3)
    resfail: typing.Optional[WRITE3resfail] = rpchelp.rpc_field(WRITE3resfail, default=None)
    resok: typing.Optional[WRITE3resok] = rpchelp.rpc_field(WRITE3resok, default=None)


class createmode3(rpchelp.enum):
    UNCHECKED = 0
    GUARDED = 1
    EXCLUSIVE = 2


@dataclass
class createhow3(rpchelp.union):
    SWITCH_OPTIONS = {UNCHECKED: 'obj_attributes', GUARDED: 'obj_attributes', EXCLUSIVE: 'verf'}
    mode: createmode3 = rpchelp.rpc_field(createmode3)
    verf: typing.Optional[bytes] = rpchelp.rpc_field(createverf3, default=None)
    obj_attributes: typing.Optional[sattr3] = rpchelp.rpc_field(sattr3, default=None)


@dataclass
class CREATE3args(rpchelp.struct):
    where: diropargs3 = rpchelp.rpc_field(diropargs3)
    how: createhow3 = rpchelp.rpc_field(createhow3)


@dataclass
class CREATE3resok(rpchelp.struct):
    obj_handle: typing.Optional[bytes] = rpchelp.rpc_field(post_op_fh3)
    obj_attributes: typing.Optional[fattr3] = rpchelp.rpc_field(post_op_attr)
    dir_wcc: wcc_data = rpchelp.rpc_field(wcc_data)


@dataclass
class CREATE3resfail(rpchelp.struct):
    dir_wcc: wcc_data = rpchelp.rpc_field(wcc_data)


@dataclass
class CREATE3res(rpchelp.union):
    SWITCH_OPTIONS = {NFS3_OK: 'resok', None: 'resfail'}
    status: nfsstat3 = rpchelp.rpc_field(nfsstat3)
    resok: typing.Optional[CREATE3resok] = rpchelp.rpc_field(CREATE3resok, default=None)
    resfail: typing.Optional[CREATE3resfail] = rpchelp.rpc_field(CREATE3resfail, default=None)


@dataclass
class MKDIR3args(rpchelp.struct):
    where: diropargs3 = rpchelp.rpc_field(diropargs3)
    attributes: sattr3 = rpchelp.rpc_field(sattr3)


@dataclass
class MKDIR3resok(rpchelp.struct):
    obj_handle: typing.Optional[bytes] = rpchelp.rpc_field(post_op_fh3)
    obj_attributes: typing.Optional[fattr3] = rpchelp.rpc_field(post_op_attr)
    dir_wcc: wcc_data = rpchelp.rpc_field(wcc_data)


@dataclass
class MKDIR3resfail(rpchelp.struct):
    dir_wcc: wcc_data = rpchelp.rpc_field(wcc_data)


@dataclass
class MKDIR3res(rpchelp.union):
    SWITCH_OPTIONS = {NFS3_OK: 'resok', None: 'resfail'}
    status: nfsstat3 = rpchelp.rpc_field(nfsstat3)
    resok: typing.Optional[MKDIR3resok] = rpchelp.rpc_field(MKDIR3resok, default=None)
    resfail: typing.Optional[MKDIR3resfail] = rpchelp.rpc_field(MKDIR3resfail, default=None)


@dataclass
class symlinkdata3(rpchelp.struct):
    symlink_attributes: sattr3 = rpchelp.rpc_field(sattr3)
    symlink_data: bytes = rpchelp.rpc_field(nfspath3)


@dataclass
class SYMLINK3args(rpchelp.struct):
    where: diropargs3 = rpchelp.rpc_field(diropargs3)
    symlink: symlinkdata3 = rpchelp.rpc_field(symlinkdata3)


@dataclass
class SYMLINK3resok(rpchelp.struct):
    obj_handle: typing.Optional[bytes] = rpchelp.rpc_field(post_op_fh3)
    obj_attributes: typing.Optional[fattr3] = rpchelp.rpc_field(post_op_attr)
    dir_wcc: wcc_data = rpchelp.rpc_field(wcc_data)


@dataclass
class SYMLINK3resfail(rpchelp.struct):
    dir_wcc: wcc_data = rpchelp.rpc_field(wcc_data)


@dataclass
class SYMLINK3res(rpchelp.union):
    SWITCH_OPTIONS = {NFS3_OK: 'resok', None: 'resfail'}
    status: nfsstat3 = rpchelp.rpc_field(nfsstat3)
    resok: typing.Optional[SYMLINK3resok] = rpchelp.rpc_field(SYMLINK3resok, default=None)
    resfail: typing.Optional[SYMLINK3resfail] = rpchelp.rpc_field(SYMLINK3resfail, default=None)


@dataclass
class devicedata3(rpchelp.struct):
    dev_attributes: sattr3 = rpchelp.rpc_field(sattr3)
    spec: specdata3 = rpchelp.rpc_field(specdata3)


@dataclass
class mknoddata3(rpchelp.union):
    SWITCH_OPTIONS = {NF3CHR: 'chr_device', NF3BLK: 'blk_device', NF3SOCK: 'sock_pipe_attributes', NF3FIFO: 'fifo_pipe_attributes', None: None}
    type: ftype3 = rpchelp.rpc_field(ftype3)
    fifo_pipe_attributes: typing.Optional[sattr3] = rpchelp.rpc_field(sattr3, default=None)
    chr_device: typing.Optional[devicedata3] = rpchelp.rpc_field(devicedata3, default=None)
    sock_pipe_attributes: typing.Optional[sattr3] = rpchelp.rpc_field(sattr3, default=None)
    blk_device: typing.Optional[devicedata3] = rpchelp.rpc_field(devicedata3, default=None)


@dataclass
class MKNOD3args(rpchelp.struct):
    where: diropargs3 = rpchelp.rpc_field(diropargs3)
    what: mknoddata3 = rpchelp.rpc_field(mknoddata3)


@dataclass
class MKNOD3resok(rpchelp.struct):
    obj_handle: typing.Optional[bytes] = rpchelp.rpc_field(post_op_fh3)
    obj_attributes: typing.Optional[fattr3] = rpchelp.rpc_field(post_op_attr)
    dir_wcc: wcc_data = rpchelp.rpc_field(wcc_data)


@dataclass
class MKNOD3resfail(rpchelp.struct):
    dir_wcc: wcc_data = rpchelp.rpc_field(wcc_data)


@dataclass
class MKNOD3res(rpchelp.union):
    SWITCH_OPTIONS = {NFS3_OK: 'resok', None: 'resfail'}
    status: nfsstat3 = rpchelp.rpc_field(nfsstat3)
    resok: typing.Optional[MKNOD3resok] = rpchelp.rpc_field(MKNOD3resok, default=None)
    resfail: typing.Optional[MKNOD3resfail] = rpchelp.rpc_field(MKNOD3resfail, default=None)


@dataclass
class REMOVE3args(rpchelp.struct):
    object: diropargs3 = rpchelp.rpc_field(diropargs3)


@dataclass
class REMOVE3resok(rpchelp.struct):
    dir_wcc: wcc_data = rpchelp.rpc_field(wcc_data)


@dataclass
class REMOVE3resfail(rpchelp.struct):
    dir_wcc: wcc_data = rpchelp.rpc_field(wcc_data)


@dataclass
class REMOVE3res(rpchelp.union):
    SWITCH_OPTIONS = {NFS3_OK: 'resok', None: 'resfail'}
    status: nfsstat3 = rpchelp.rpc_field(nfsstat3)
    resfail: typing.Optional[REMOVE3resfail] = rpchelp.rpc_field(REMOVE3resfail, default=None)
    resok: typing.Optional[REMOVE3resok] = rpchelp.rpc_field(REMOVE3resok, default=None)


@dataclass
class RMDIR3args(rpchelp.struct):
    object: diropargs3 = rpchelp.rpc_field(diropargs3)


@dataclass
class RMDIR3resok(rpchelp.struct):
    dir_wcc: wcc_data = rpchelp.rpc_field(wcc_data)


@dataclass
class RMDIR3resfail(rpchelp.struct):
    dir_wcc: wcc_data = rpchelp.rpc_field(wcc_data)


@dataclass
class RMDIR3res(rpchelp.union):
    SWITCH_OPTIONS = {NFS3_OK: 'resok', None: 'resfail'}
    status: nfsstat3 = rpchelp.rpc_field(nfsstat3)
    resok: typing.Optional[RMDIR3resok] = rpchelp.rpc_field(RMDIR3resok, default=None)
    resfail: typing.Optional[RMDIR3resfail] = rpchelp.rpc_field(RMDIR3resfail, default=None)


@dataclass
class RENAME3args(rpchelp.struct):
    from_: diropargs3 = rpchelp.rpc_field(diropargs3)
    to: diropargs3 = rpchelp.rpc_field(diropargs3)


@dataclass
class RENAME3resok(rpchelp.struct):
    fromdir_wcc: wcc_data = rpchelp.rpc_field(wcc_data)
    todir_wcc: wcc_data = rpchelp.rpc_field(wcc_data)


@dataclass
class RENAME3resfail(rpchelp.struct):
    fromdir_wcc: wcc_data = rpchelp.rpc_field(wcc_data)
    todir_wcc: wcc_data = rpchelp.rpc_field(wcc_data)


@dataclass
class RENAME3res(rpchelp.union):
    SWITCH_OPTIONS = {NFS3_OK: 'resok', None: 'resfail'}
    status: nfsstat3 = rpchelp.rpc_field(nfsstat3)
    resok: typing.Optional[RENAME3resok] = rpchelp.rpc_field(RENAME3resok, default=None)
    resfail: typing.Optional[RENAME3resfail] = rpchelp.rpc_field(RENAME3resfail, default=None)


@dataclass
class LINK3args(rpchelp.struct):
    file_handle: bytes = rpchelp.rpc_field(nfs_fh3)
    link: diropargs3 = rpchelp.rpc_field(diropargs3)


@dataclass
class LINK3resok(rpchelp.struct):
    file_attributes: typing.Optional[fattr3] = rpchelp.rpc_field(post_op_attr)
    linkdir_wcc: wcc_data = rpchelp.rpc_field(wcc_data)


@dataclass
class LINK3resfail(rpchelp.struct):
    file_attributes: typing.Optional[fattr3] = rpchelp.rpc_field(post_op_attr)
    linkdir_wcc: wcc_data = rpchelp.rpc_field(wcc_data)


@dataclass
class LINK3res(rpchelp.union):
    SWITCH_OPTIONS = {NFS3_OK: 'resok', None: 'resfail'}
    status: nfsstat3 = rpchelp.rpc_field(nfsstat3)
    resok: typing.Optional[LINK3resok] = rpchelp.rpc_field(LINK3resok, default=None)
    resfail: typing.Optional[LINK3resfail] = rpchelp.rpc_field(LINK3resfail, default=None)


@dataclass
class READDIR3args(rpchelp.struct):
    dir_handle: bytes = rpchelp.rpc_field(nfs_fh3)
    cookie: int = rpchelp.rpc_field(cookie3)
    cookieverf: bytes = rpchelp.rpc_field(cookieverf3)
    count: int = rpchelp.rpc_field(count3)


@dataclass
class entry3(rpchelp.linked_list):
    fileid: int = rpchelp.rpc_field(fileid3)
    name: bytes = rpchelp.rpc_field(filename3)
    cookie: int = rpchelp.rpc_field(cookie3)


@dataclass
class dirlist3(rpchelp.struct):
    entries: typing.List[entry3] = rpchelp.rpc_field(rpchelp.opt_data(entry3))
    eof: bool = rpchelp.rpc_field(rpchelp.r_bool)


@dataclass
class READDIR3resok(rpchelp.struct):
    dir_attributes: typing.Optional[fattr3] = rpchelp.rpc_field(post_op_attr)
    cookieverf: bytes = rpchelp.rpc_field(cookieverf3)
    reply: dirlist3 = rpchelp.rpc_field(dirlist3)


@dataclass
class READDIR3resfail(rpchelp.struct):
    dir_attributes: typing.Optional[fattr3] = rpchelp.rpc_field(post_op_attr)


@dataclass
class READDIR3res(rpchelp.union):
    SWITCH_OPTIONS = {NFS3_OK: 'resok', None: 'resfail'}
    status: nfsstat3 = rpchelp.rpc_field(nfsstat3)
    resok: typing.Optional[READDIR3resok] = rpchelp.rpc_field(READDIR3resok, default=None)
    resfail: typing.Optional[READDIR3resfail] = rpchelp.rpc_field(READDIR3resfail, default=None)


@dataclass
class READDIRPLUS3args(rpchelp.struct):
    dir_handle: bytes = rpchelp.rpc_field(nfs_fh3)
    cookie: int = rpchelp.rpc_field(cookie3)
    cookieverf: bytes = rpchelp.rpc_field(cookieverf3)
    dircount: int = rpchelp.rpc_field(count3)
    maxcount: int = rpchelp.rpc_field(count3)


@dataclass
class entryplus3(rpchelp.linked_list):
    fileid: int = rpchelp.rpc_field(fileid3)
    name: bytes = rpchelp.rpc_field(filename3)
    cookie: int = rpchelp.rpc_field(cookie3)
    name_attributes: typing.Optional[fattr3] = rpchelp.rpc_field(post_op_attr)
    name_handle: typing.Optional[bytes] = rpchelp.rpc_field(post_op_fh3)


@dataclass
class dirlistplus3(rpchelp.struct):
    entries: typing.List[entryplus3] = rpchelp.rpc_field(rpchelp.opt_data(entryplus3))
    eof: bool = rpchelp.rpc_field(rpchelp.r_bool)


@dataclass
class READDIRPLUS3resok(rpchelp.struct):
    dir_attributes: typing.Optional[fattr3] = rpchelp.rpc_field(post_op_attr)
    cookieverf: bytes = rpchelp.rpc_field(cookieverf3)
    reply: dirlistplus3 = rpchelp.rpc_field(dirlistplus3)


@dataclass
class READDIRPLUS3resfail(rpchelp.struct):
    dir_attributes: typing.Optional[fattr3] = rpchelp.rpc_field(post_op_attr)


@dataclass
class READDIRPLUS3res(rpchelp.union):
    SWITCH_OPTIONS = {NFS3_OK: 'resok', None: 'resfail'}
    status: nfsstat3 = rpchelp.rpc_field(nfsstat3)
    resfail: typing.Optional[READDIRPLUS3resfail] = rpchelp.rpc_field(READDIRPLUS3resfail, default=None)
    resok: typing.Optional[READDIRPLUS3resok] = rpchelp.rpc_field(READDIRPLUS3resok, default=None)


@dataclass
class FSSTAT3args(rpchelp.struct):
    fsroot_handle: bytes = rpchelp.rpc_field(nfs_fh3)


@dataclass
class FSSTAT3resok(rpchelp.struct):
    obj_attributes: typing.Optional[fattr3] = rpchelp.rpc_field(post_op_attr)
    tbytes: int = rpchelp.rpc_field(size3)
    fbytes: int = rpchelp.rpc_field(size3)
    abytes: int = rpchelp.rpc_field(size3)
    tfiles: int = rpchelp.rpc_field(size3)
    ffiles: int = rpchelp.rpc_field(size3)
    afiles: int = rpchelp.rpc_field(size3)
    invarsec: int = rpchelp.rpc_field(uint32)


@dataclass
class FSSTAT3resfail(rpchelp.struct):
    obj_attributes: typing.Optional[fattr3] = rpchelp.rpc_field(post_op_attr)


@dataclass
class FSSTAT3res(rpchelp.union):
    SWITCH_OPTIONS = {NFS3_OK: 'resok', None: 'resfail'}
    status: nfsstat3 = rpchelp.rpc_field(nfsstat3)
    resok: typing.Optional[FSSTAT3resok] = rpchelp.rpc_field(FSSTAT3resok, default=None)
    resfail: typing.Optional[FSSTAT3resfail] = rpchelp.rpc_field(FSSTAT3resfail, default=None)


FSF3_LINK = 0x0001
FSF3_SYMLINK = 0x0002
FSF3_HOMOGENEOUS = 0x0008
FSF3_CANSETTIME = 0x0010


@dataclass
class FSINFO3args(rpchelp.struct):
    fsroot_handle: bytes = rpchelp.rpc_field(nfs_fh3)


@dataclass
class FSINFO3resok(rpchelp.struct):
    obj_attributes: typing.Optional[fattr3] = rpchelp.rpc_field(post_op_attr)
    rtmax: int = rpchelp.rpc_field(uint32)
    rtpref: int = rpchelp.rpc_field(uint32)
    rtmult: int = rpchelp.rpc_field(uint32)
    wtmax: int = rpchelp.rpc_field(uint32)
    wtpref: int = rpchelp.rpc_field(uint32)
    wtmult: int = rpchelp.rpc_field(uint32)
    dtpref: int = rpchelp.rpc_field(uint32)
    maxfilesize: int = rpchelp.rpc_field(size3)
    time_delta: nfstime3 = rpchelp.rpc_field(nfstime3)
    properties: int = rpchelp.rpc_field(uint32)


@dataclass
class FSINFO3resfail(rpchelp.struct):
    obj_attributes: typing.Optional[fattr3] = rpchelp.rpc_field(post_op_attr)


@dataclass
class FSINFO3res(rpchelp.union):
    SWITCH_OPTIONS = {NFS3_OK: 'resok', None: 'resfail'}
    status: nfsstat3 = rpchelp.rpc_field(nfsstat3)
    resok: typing.Optional[FSINFO3resok] = rpchelp.rpc_field(FSINFO3resok, default=None)
    resfail: typing.Optional[FSINFO3resfail] = rpchelp.rpc_field(FSINFO3resfail, default=None)


@dataclass
class PATHCONF3args(rpchelp.struct):
    obj_handle: bytes = rpchelp.rpc_field(nfs_fh3)


@dataclass
class PATHCONF3resok(rpchelp.struct):
    obj_attributes: typing.Optional[fattr3] = rpchelp.rpc_field(post_op_attr)
    linkmax: int = rpchelp.rpc_field(uint32)
    name_max: int = rpchelp.rpc_field(uint32)
    no_trunc: bool = rpchelp.rpc_field(rpchelp.r_bool)
    chown_restricted: bool = rpchelp.rpc_field(rpchelp.r_bool)
    case_insensitive: bool = rpchelp.rpc_field(rpchelp.r_bool)
    case_preserving: bool = rpchelp.rpc_field(rpchelp.r_bool)


@dataclass
class PATHCONF3resfail(rpchelp.struct):
    obj_attributes: typing.Optional[fattr3] = rpchelp.rpc_field(post_op_attr)


@dataclass
class PATHCONF3res(rpchelp.union):
    SWITCH_OPTIONS = {NFS3_OK: 'resok', None: 'resfail'}
    status: nfsstat3 = rpchelp.rpc_field(nfsstat3)
    resok: typing.Optional[PATHCONF3resok] = rpchelp.rpc_field(PATHCONF3resok, default=None)
    resfail: typing.Optional[PATHCONF3resfail] = rpchelp.rpc_field(PATHCONF3resfail, default=None)


@dataclass
class COMMIT3args(rpchelp.struct):
    file_handle: bytes = rpchelp.rpc_field(nfs_fh3)
    offset: int = rpchelp.rpc_field(offset3)
    count: int = rpchelp.rpc_field(count3)


@dataclass
class COMMIT3resok(rpchelp.struct):
    file_wcc: wcc_data = rpchelp.rpc_field(wcc_data)
    verf: bytes = rpchelp.rpc_field(writeverf3)


@dataclass
class COMMIT3resfail(rpchelp.struct):
    file_wcc: wcc_data = rpchelp.rpc_field(wcc_data)


@dataclass
class COMMIT3res(rpchelp.union):
    SWITCH_OPTIONS = {NFS3_OK: 'resok', None: 'resfail'}
    status: nfsstat3 = rpchelp.rpc_field(nfsstat3)
    resok: typing.Optional[COMMIT3resok] = rpchelp.rpc_field(COMMIT3resok, default=None)
    resfail: typing.Optional[COMMIT3resfail] = rpchelp.rpc_field(COMMIT3resfail, default=None)


MNTPATHLEN = 1024
MNTNAMLEN = 255
FHSIZE3 = 64
fhandle3 = rpchelp.opaque(rpchelp.LengthType.VAR, FHSIZE3)
dirpath = rpchelp.string(rpchelp.LengthType.VAR, MNTPATHLEN)
name = rpchelp.string(rpchelp.LengthType.VAR, MNTNAMLEN)


class mountstat3(rpchelp.enum):
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
class mountres3_ok(rpchelp.struct):
    fhandle: bytes = rpchelp.rpc_field(fhandle3)
    auth_flavors: typing.List[int] = rpchelp.rpc_field(rpchelp.arr(rpchelp.r_int, rpchelp.LengthType.VAR, None))


@dataclass
class mountres3(rpchelp.union):
    SWITCH_OPTIONS = {MNT3_OK: 'mountinfo', None: None}
    fhs_status: mountstat3 = rpchelp.rpc_field(mountstat3)
    mountinfo: typing.Optional[mountres3_ok] = rpchelp.rpc_field(mountres3_ok, default=None)


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


class NFS_PROGRAM_3_SERVER(rpchelp.Prog):
    prog = 100003
    vers = 3
    procs = {
        0: rpchelp.Proc('NULL', rpchelp.r_void, []),
        1: rpchelp.Proc('GETATTR', GETATTR3res, [GETATTR3args]),
        2: rpchelp.Proc('SETATTR', SETATTR3res, [SETATTR3args]),
        3: rpchelp.Proc('LOOKUP', LOOKUP3res, [LOOKUP3args]),
        4: rpchelp.Proc('ACCESS', ACCESS3res, [ACCESS3args]),
        5: rpchelp.Proc('READLINK', READLINK3res, [READLINK3args]),
        6: rpchelp.Proc('READ', READ3res, [READ3args]),
        7: rpchelp.Proc('WRITE', WRITE3res, [WRITE3args]),
        8: rpchelp.Proc('CREATE', CREATE3res, [CREATE3args]),
        9: rpchelp.Proc('MKDIR', MKDIR3res, [MKDIR3args]),
        10: rpchelp.Proc('SYMLINK', SYMLINK3res, [SYMLINK3args]),
        11: rpchelp.Proc('MKNOD', MKNOD3res, [MKNOD3args]),
        12: rpchelp.Proc('REMOVE', REMOVE3res, [REMOVE3args]),
        13: rpchelp.Proc('RMDIR', RMDIR3res, [RMDIR3args]),
        14: rpchelp.Proc('RENAME', RENAME3res, [RENAME3args]),
        15: rpchelp.Proc('LINK', LINK3res, [LINK3args]),
        16: rpchelp.Proc('READDIR', READDIR3res, [READDIR3args]),
        17: rpchelp.Proc('READDIRPLUS', READDIRPLUS3res, [READDIRPLUS3args]),
        18: rpchelp.Proc('FSSTAT', FSSTAT3res, [FSSTAT3args]),
        19: rpchelp.Proc('FSINFO', FSINFO3res, [FSINFO3args]),
        20: rpchelp.Proc('PATHCONF', PATHCONF3res, [PATHCONF3args]),
        21: rpchelp.Proc('COMMIT', COMMIT3res, [COMMIT3args]),
    }

    @abc.abstractmethod
    def NULL(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def GETATTR(self, arg_0: GETATTR3args) -> GETATTR3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def SETATTR(self, arg_0: SETATTR3args) -> SETATTR3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def LOOKUP(self, arg_0: LOOKUP3args) -> LOOKUP3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def ACCESS(self, arg_0: ACCESS3args) -> ACCESS3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def READLINK(self, arg_0: READLINK3args) -> READLINK3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def READ(self, arg_0: READ3args) -> READ3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def WRITE(self, arg_0: WRITE3args) -> WRITE3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def CREATE(self, arg_0: CREATE3args) -> CREATE3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def MKDIR(self, arg_0: MKDIR3args) -> MKDIR3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def SYMLINK(self, arg_0: SYMLINK3args) -> SYMLINK3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def MKNOD(self, arg_0: MKNOD3args) -> MKNOD3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def REMOVE(self, arg_0: REMOVE3args) -> REMOVE3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def RMDIR(self, arg_0: RMDIR3args) -> RMDIR3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def RENAME(self, arg_0: RENAME3args) -> RENAME3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def LINK(self, arg_0: LINK3args) -> LINK3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def READDIR(self, arg_0: READDIR3args) -> READDIR3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def READDIRPLUS(self, arg_0: READDIRPLUS3args) -> READDIRPLUS3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def FSSTAT(self, arg_0: FSSTAT3args) -> FSSTAT3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def FSINFO(self, arg_0: FSINFO3args) -> FSINFO3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def PATHCONF(self, arg_0: PATHCONF3args) -> PATHCONF3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def COMMIT(self, arg_0: COMMIT3args) -> COMMIT3res:
        raise NotImplementedError()


class NFS_PROGRAM_3_CLIENT(client.BaseClient):
    prog = 100003
    vers = 3
    procs = {
        0: rpchelp.Proc('NULL', rpchelp.r_void, []),
        1: rpchelp.Proc('GETATTR', GETATTR3res, [GETATTR3args]),
        2: rpchelp.Proc('SETATTR', SETATTR3res, [SETATTR3args]),
        3: rpchelp.Proc('LOOKUP', LOOKUP3res, [LOOKUP3args]),
        4: rpchelp.Proc('ACCESS', ACCESS3res, [ACCESS3args]),
        5: rpchelp.Proc('READLINK', READLINK3res, [READLINK3args]),
        6: rpchelp.Proc('READ', READ3res, [READ3args]),
        7: rpchelp.Proc('WRITE', WRITE3res, [WRITE3args]),
        8: rpchelp.Proc('CREATE', CREATE3res, [CREATE3args]),
        9: rpchelp.Proc('MKDIR', MKDIR3res, [MKDIR3args]),
        10: rpchelp.Proc('SYMLINK', SYMLINK3res, [SYMLINK3args]),
        11: rpchelp.Proc('MKNOD', MKNOD3res, [MKNOD3args]),
        12: rpchelp.Proc('REMOVE', REMOVE3res, [REMOVE3args]),
        13: rpchelp.Proc('RMDIR', RMDIR3res, [RMDIR3args]),
        14: rpchelp.Proc('RENAME', RENAME3res, [RENAME3args]),
        15: rpchelp.Proc('LINK', LINK3res, [LINK3args]),
        16: rpchelp.Proc('READDIR', READDIR3res, [READDIR3args]),
        17: rpchelp.Proc('READDIRPLUS', READDIRPLUS3res, [READDIRPLUS3args]),
        18: rpchelp.Proc('FSSTAT', FSSTAT3res, [FSSTAT3args]),
        19: rpchelp.Proc('FSINFO', FSINFO3res, [FSINFO3args]),
        20: rpchelp.Proc('PATHCONF', PATHCONF3res, [PATHCONF3args]),
        21: rpchelp.Proc('COMMIT', COMMIT3res, [COMMIT3args]),
    }

    async def NULL(self) -> client.UnpackedRPCMsg[None]:
        return await self.send_call(0, )

    async def GETATTR(self, arg_0: GETATTR3args) -> client.UnpackedRPCMsg[GETATTR3res]:
        return await self.send_call(1, arg_0)

    async def SETATTR(self, arg_0: SETATTR3args) -> client.UnpackedRPCMsg[SETATTR3res]:
        return await self.send_call(2, arg_0)

    async def LOOKUP(self, arg_0: LOOKUP3args) -> client.UnpackedRPCMsg[LOOKUP3res]:
        return await self.send_call(3, arg_0)

    async def ACCESS(self, arg_0: ACCESS3args) -> client.UnpackedRPCMsg[ACCESS3res]:
        return await self.send_call(4, arg_0)

    async def READLINK(self, arg_0: READLINK3args) -> client.UnpackedRPCMsg[READLINK3res]:
        return await self.send_call(5, arg_0)

    async def READ(self, arg_0: READ3args) -> client.UnpackedRPCMsg[READ3res]:
        return await self.send_call(6, arg_0)

    async def WRITE(self, arg_0: WRITE3args) -> client.UnpackedRPCMsg[WRITE3res]:
        return await self.send_call(7, arg_0)

    async def CREATE(self, arg_0: CREATE3args) -> client.UnpackedRPCMsg[CREATE3res]:
        return await self.send_call(8, arg_0)

    async def MKDIR(self, arg_0: MKDIR3args) -> client.UnpackedRPCMsg[MKDIR3res]:
        return await self.send_call(9, arg_0)

    async def SYMLINK(self, arg_0: SYMLINK3args) -> client.UnpackedRPCMsg[SYMLINK3res]:
        return await self.send_call(10, arg_0)

    async def MKNOD(self, arg_0: MKNOD3args) -> client.UnpackedRPCMsg[MKNOD3res]:
        return await self.send_call(11, arg_0)

    async def REMOVE(self, arg_0: REMOVE3args) -> client.UnpackedRPCMsg[REMOVE3res]:
        return await self.send_call(12, arg_0)

    async def RMDIR(self, arg_0: RMDIR3args) -> client.UnpackedRPCMsg[RMDIR3res]:
        return await self.send_call(13, arg_0)

    async def RENAME(self, arg_0: RENAME3args) -> client.UnpackedRPCMsg[RENAME3res]:
        return await self.send_call(14, arg_0)

    async def LINK(self, arg_0: LINK3args) -> client.UnpackedRPCMsg[LINK3res]:
        return await self.send_call(15, arg_0)

    async def READDIR(self, arg_0: READDIR3args) -> client.UnpackedRPCMsg[READDIR3res]:
        return await self.send_call(16, arg_0)

    async def READDIRPLUS(self, arg_0: READDIRPLUS3args) -> client.UnpackedRPCMsg[READDIRPLUS3res]:
        return await self.send_call(17, arg_0)

    async def FSSTAT(self, arg_0: FSSTAT3args) -> client.UnpackedRPCMsg[FSSTAT3res]:
        return await self.send_call(18, arg_0)

    async def FSINFO(self, arg_0: FSINFO3args) -> client.UnpackedRPCMsg[FSINFO3res]:
        return await self.send_call(19, arg_0)

    async def PATHCONF(self, arg_0: PATHCONF3args) -> client.UnpackedRPCMsg[PATHCONF3res]:
        return await self.send_call(20, arg_0)

    async def COMMIT(self, arg_0: COMMIT3args) -> client.UnpackedRPCMsg[COMMIT3res]:
        return await self.send_call(21, arg_0)


class MOUNT_PROGRAM_3_SERVER(rpchelp.Prog):
    prog = 100005
    vers = 3
    procs = {
        0: rpchelp.Proc('NULL', rpchelp.r_void, []),
        1: rpchelp.Proc('MNT', mountres3, [dirpath]),
        2: rpchelp.Proc('DUMP', mountlist, []),
        3: rpchelp.Proc('UMNT', rpchelp.r_void, [dirpath]),
        4: rpchelp.Proc('UMNTALL', rpchelp.r_void, []),
        5: rpchelp.Proc('EXPORT', exportlist, []),
    }

    @abc.abstractmethod
    def NULL(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def MNT(self, arg_0: bytes) -> mountres3:
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


class MOUNT_PROGRAM_3_CLIENT(client.BaseClient):
    prog = 100005
    vers = 3
    procs = {
        0: rpchelp.Proc('NULL', rpchelp.r_void, []),
        1: rpchelp.Proc('MNT', mountres3, [dirpath]),
        2: rpchelp.Proc('DUMP', mountlist, []),
        3: rpchelp.Proc('UMNT', rpchelp.r_void, [dirpath]),
        4: rpchelp.Proc('UMNTALL', rpchelp.r_void, []),
        5: rpchelp.Proc('EXPORT', exportlist, []),
    }

    async def NULL(self) -> client.UnpackedRPCMsg[None]:
        return await self.send_call(0, )

    async def MNT(self, arg_0: bytes) -> client.UnpackedRPCMsg[mountres3]:
        return await self.send_call(1, arg_0)

    async def DUMP(self) -> client.UnpackedRPCMsg[typing.List[mountlist]]:
        return await self.send_call(2, )

    async def UMNT(self, arg_0: bytes) -> client.UnpackedRPCMsg[None]:
        return await self.send_call(3, arg_0)

    async def UMNTALL(self) -> client.UnpackedRPCMsg[None]:
        return await self.send_call(4, )

    async def EXPORT(self) -> client.UnpackedRPCMsg[typing.List[exportlist]]:
        return await self.send_call(5, )


__all__ = ['NFS_PROGRAM_3_SERVER', 'NFS_PROGRAM_3_CLIENT', 'MOUNT_PROGRAM_3_SERVER', 'MOUNT_PROGRAM_3_CLIENT', 'TRUE', 'FALSE', 'NFS3_FHSIZE', 'NFS3_COOKIEVERFSIZE', 'NFS3_CREATEVERFSIZE', 'NFS3_WRITEVERFSIZE', 'NFS3_OK', 'NFS3ERR_PERM', 'NFS3ERR_NOENT', 'NFS3ERR_IO', 'NFS3ERR_NXIO', 'NFS3ERR_ACCES', 'NFS3ERR_EXIST', 'NFS3ERR_XDEV', 'NFS3ERR_NODEV', 'NFS3ERR_NOTDIR', 'NFS3ERR_ISDIR', 'NFS3ERR_INVAL', 'NFS3ERR_FBIG', 'NFS3ERR_NOSPC', 'NFS3ERR_ROFS', 'NFS3ERR_MLINK', 'NFS3ERR_NAMETOOLONG', 'NFS3ERR_NOTEMPTY', 'NFS3ERR_DQUOT', 'NFS3ERR_STALE', 'NFS3ERR_REMOTE', 'NFS3ERR_BADHANDLE', 'NFS3ERR_NOT_SYNC', 'NFS3ERR_BAD_COOKIE', 'NFS3ERR_NOTSUPP', 'NFS3ERR_TOOSMALL', 'NFS3ERR_SERVERFAULT', 'NFS3ERR_BADTYPE', 'NFS3ERR_JUKEBOX', 'NF3REG', 'NF3DIR', 'NF3BLK', 'NF3CHR', 'NF3LNK', 'NF3SOCK', 'NF3FIFO', 'DONT_CHANGE', 'SET_TO_SERVER_TIME', 'SET_TO_CLIENT_TIME', 'ACCESS3_READ', 'ACCESS3_LOOKUP', 'ACCESS3_MODIFY', 'ACCESS3_EXTEND', 'ACCESS3_DELETE', 'ACCESS3_EXECUTE', 'UNSTABLE', 'DATA_SYNC', 'FILE_SYNC', 'UNCHECKED', 'GUARDED', 'EXCLUSIVE', 'FSF3_LINK', 'FSF3_SYMLINK', 'FSF3_HOMOGENEOUS', 'FSF3_CANSETTIME', 'MNTPATHLEN', 'MNTNAMLEN', 'FHSIZE3', 'MNT3_OK', 'MNT3ERR_PERM', 'MNT3ERR_NOENT', 'MNT3ERR_IO', 'MNT3ERR_ACCES', 'MNT3ERR_NOTDIR', 'MNT3ERR_INVAL', 'MNT3ERR_NAMETOOLONG', 'MNT3ERR_NOTSUPP', 'MNT3ERR_SERVERFAULT', 'uint64', 'int64', 'uint32', 'int32', 'filename3', 'nfspath3', 'fileid3', 'cookie3', 'cookieverf3', 'createverf3', 'writeverf3', 'uid3', 'gid3', 'size3', 'offset3', 'mode3', 'count3', 'nfsstat3', 'ftype3', 'specdata3', 'nfs_fh3', 'nfstime3', 'fattr3', 'wcc_attr', 'post_op_attr', 'pre_op_attr', 'wcc_data', 'post_op_fh3', 'time_how', 'set_mode3', 'set_uid3', 'set_gid3', 'set_size3', 'set_atime', 'set_mtime', 'sattr3', 'diropargs3', 'GETATTR3args', 'GETATTR3resok', 'GETATTR3res', 'sattrguard3', 'SETATTR3args', 'SETATTR3resok', 'SETATTR3resfail', 'SETATTR3res', 'LOOKUP3args', 'LOOKUP3resok', 'LOOKUP3resfail', 'LOOKUP3res', 'ACCESS3args', 'ACCESS3resok', 'ACCESS3resfail', 'ACCESS3res', 'READLINK3args', 'READLINK3resok', 'READLINK3resfail', 'READLINK3res', 'READ3args', 'READ3resok', 'READ3resfail', 'READ3res', 'stable_how', 'WRITE3args', 'WRITE3resok', 'WRITE3resfail', 'WRITE3res', 'createmode3', 'createhow3', 'CREATE3args', 'CREATE3resok', 'CREATE3resfail', 'CREATE3res', 'MKDIR3args', 'MKDIR3resok', 'MKDIR3resfail', 'MKDIR3res', 'symlinkdata3', 'SYMLINK3args', 'SYMLINK3resok', 'SYMLINK3resfail', 'SYMLINK3res', 'devicedata3', 'mknoddata3', 'MKNOD3args', 'MKNOD3resok', 'MKNOD3resfail', 'MKNOD3res', 'REMOVE3args', 'REMOVE3resok', 'REMOVE3resfail', 'REMOVE3res', 'RMDIR3args', 'RMDIR3resok', 'RMDIR3resfail', 'RMDIR3res', 'RENAME3args', 'RENAME3resok', 'RENAME3resfail', 'RENAME3res', 'LINK3args', 'LINK3resok', 'LINK3resfail', 'LINK3res', 'READDIR3args', 'entry3', 'dirlist3', 'READDIR3resok', 'READDIR3resfail', 'READDIR3res', 'READDIRPLUS3args', 'entryplus3', 'dirlistplus3', 'READDIRPLUS3resok', 'READDIRPLUS3resfail', 'READDIRPLUS3res', 'FSSTAT3args', 'FSSTAT3resok', 'FSSTAT3resfail', 'FSSTAT3res', 'FSINFO3args', 'FSINFO3resok', 'FSINFO3resfail', 'FSINFO3res', 'PATHCONF3args', 'PATHCONF3resok', 'PATHCONF3resfail', 'PATHCONF3res', 'COMMIT3args', 'COMMIT3resok', 'COMMIT3resfail', 'COMMIT3res', 'fhandle3', 'dirpath', 'name', 'mountstat3', 'mountres3_ok', 'mountres3', 'mountlist', 'grouplist', 'exportlist']
