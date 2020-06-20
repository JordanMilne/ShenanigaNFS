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

post_op_attr = rpchelp.union('post_op_attr', rpchelp.r_bool, 'attributes_follow', {TRUE: ('attributes', fattr3), FALSE: (None, rpchelp.r_void)}, from_parser=True)
@dataclass
class v_post_op_attr:
    attributes_follow: bool
    attributes: typing.Optional[fattr3] = None


post_op_attr.val_base_class = v_post_op_attr



@dataclass
class wcc_attr(rpchelp.struct):
    size: int = rpchelp.rpc_field(size3)
    mtime: nfstime3 = rpchelp.rpc_field(nfstime3)
    ctime: nfstime3 = rpchelp.rpc_field(nfstime3)

pre_op_attr = rpchelp.union('pre_op_attr', rpchelp.r_bool, 'attributes_follow', {TRUE: ('attributes', wcc_attr), FALSE: (None, rpchelp.r_void)}, from_parser=True)
@dataclass
class v_pre_op_attr:
    attributes_follow: bool
    attributes: typing.Optional[wcc_attr] = None


pre_op_attr.val_base_class = v_pre_op_attr



@dataclass
class wcc_data(rpchelp.struct):
    before: typing.Optional[wcc_attr] = rpchelp.rpc_field(pre_op_attr)
    after: typing.Optional[fattr3] = rpchelp.rpc_field(post_op_attr)

post_op_fh3 = rpchelp.union('post_op_fh3', rpchelp.r_bool, 'handle_follows', {TRUE: ('obj_handle', nfs_fh3), FALSE: (None, rpchelp.r_void)}, from_parser=True)
@dataclass
class v_post_op_fh3:
    handle_follows: bool
    obj_handle: typing.Optional[bytes] = None


post_op_fh3.val_base_class = v_post_op_fh3



class time_how(rpchelp.enum):
    DONT_CHANGE = 0
    SET_TO_SERVER_TIME = 1
    SET_TO_CLIENT_TIME = 2
set_mode3 = rpchelp.union('set_mode3', rpchelp.r_bool, 'set_it', {TRUE: ('mode', mode3), None: (None, rpchelp.r_void)}, from_parser=True)
@dataclass
class v_set_mode3:
    set_it: bool
    mode: typing.Optional[int] = None


set_mode3.val_base_class = v_set_mode3



set_uid3 = rpchelp.union('set_uid3', rpchelp.r_bool, 'set_it', {TRUE: ('uid', uid3), None: (None, rpchelp.r_void)}, from_parser=True)
@dataclass
class v_set_uid3:
    set_it: bool
    uid: typing.Optional[int] = None


set_uid3.val_base_class = v_set_uid3



set_gid3 = rpchelp.union('set_gid3', rpchelp.r_bool, 'set_it', {TRUE: ('gid', gid3), None: (None, rpchelp.r_void)}, from_parser=True)
@dataclass
class v_set_gid3:
    set_it: bool
    gid: typing.Optional[int] = None


set_gid3.val_base_class = v_set_gid3



set_size3 = rpchelp.union('set_size3', rpchelp.r_bool, 'set_it', {TRUE: ('size', size3), None: (None, rpchelp.r_void)}, from_parser=True)
@dataclass
class v_set_size3:
    set_it: bool
    size: typing.Optional[int] = None


set_size3.val_base_class = v_set_size3



set_atime = rpchelp.union('set_atime', time_how, 'set_it', {SET_TO_CLIENT_TIME: ('atime', nfstime3), None: (None, rpchelp.r_void)}, from_parser=True)
@dataclass
class v_set_atime:
    set_it: time_how
    atime: typing.Optional[nfstime3] = None


set_atime.val_base_class = v_set_atime



set_mtime = rpchelp.union('set_mtime', time_how, 'set_it', {SET_TO_CLIENT_TIME: ('mtime', nfstime3), None: (None, rpchelp.r_void)}, from_parser=True)
@dataclass
class v_set_mtime:
    set_it: time_how
    mtime: typing.Optional[nfstime3] = None


set_mtime.val_base_class = v_set_mtime



@dataclass
class sattr3(rpchelp.struct):
    mode: v_set_mode3 = rpchelp.rpc_field(set_mode3)
    uid: v_set_uid3 = rpchelp.rpc_field(set_uid3)
    gid: v_set_gid3 = rpchelp.rpc_field(set_gid3)
    size: v_set_size3 = rpchelp.rpc_field(set_size3)
    atime: v_set_atime = rpchelp.rpc_field(set_atime)
    mtime: v_set_mtime = rpchelp.rpc_field(set_mtime)

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

GETATTR3res = rpchelp.union('GETATTR3res', nfsstat3, 'status', {NFS3_OK: ('resok', GETATTR3resok), None: (None, rpchelp.r_void)}, from_parser=True)
@dataclass
class v_GETATTR3res:
    status: nfsstat3
    resok: typing.Optional[GETATTR3resok] = None


GETATTR3res.val_base_class = v_GETATTR3res



sattrguard3 = rpchelp.union('sattrguard3', rpchelp.r_bool, 'check', {TRUE: ('obj_ctime', nfstime3), FALSE: (None, rpchelp.r_void)}, from_parser=True)
@dataclass
class v_sattrguard3:
    check: bool
    obj_ctime: typing.Optional[nfstime3] = None


sattrguard3.val_base_class = v_sattrguard3



@dataclass
class SETATTR3args(rpchelp.struct):
    obj_handle: bytes = rpchelp.rpc_field(nfs_fh3)
    new_attributes: sattr3 = rpchelp.rpc_field(sattr3)
    guard: typing.Optional[nfstime3] = rpchelp.rpc_field(sattrguard3)

@dataclass
class SETATTR3resok(rpchelp.struct):
    obj_wcc: wcc_data = rpchelp.rpc_field(wcc_data)

@dataclass
class SETATTR3resfail(rpchelp.struct):
    obj_wcc: wcc_data = rpchelp.rpc_field(wcc_data)

SETATTR3res = rpchelp.union('SETATTR3res', nfsstat3, 'status', {NFS3_OK: ('resok', SETATTR3resok), None: ('resfail', SETATTR3resfail)}, from_parser=True)
@dataclass
class v_SETATTR3res:
    status: nfsstat3
    resok: typing.Optional[SETATTR3resok] = None
    resfail: typing.Optional[SETATTR3resfail] = None


SETATTR3res.val_base_class = v_SETATTR3res



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

LOOKUP3res = rpchelp.union('LOOKUP3res', nfsstat3, 'status', {NFS3_OK: ('resok', LOOKUP3resok), None: ('resfail', LOOKUP3resfail)}, from_parser=True)
@dataclass
class v_LOOKUP3res:
    status: nfsstat3
    resok: typing.Optional[LOOKUP3resok] = None
    resfail: typing.Optional[LOOKUP3resfail] = None


LOOKUP3res.val_base_class = v_LOOKUP3res



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

ACCESS3res = rpchelp.union('ACCESS3res', nfsstat3, 'status', {NFS3_OK: ('resok', ACCESS3resok), None: ('resfail', ACCESS3resfail)}, from_parser=True)
@dataclass
class v_ACCESS3res:
    status: nfsstat3
    resok: typing.Optional[ACCESS3resok] = None
    resfail: typing.Optional[ACCESS3resfail] = None


ACCESS3res.val_base_class = v_ACCESS3res



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

READLINK3res = rpchelp.union('READLINK3res', nfsstat3, 'status', {NFS3_OK: ('resok', READLINK3resok), None: ('resfail', READLINK3resfail)}, from_parser=True)
@dataclass
class v_READLINK3res:
    status: nfsstat3
    resok: typing.Optional[READLINK3resok] = None
    resfail: typing.Optional[READLINK3resfail] = None


READLINK3res.val_base_class = v_READLINK3res



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

READ3res = rpchelp.union('READ3res', nfsstat3, 'status', {NFS3_OK: ('resok', READ3resok), None: ('resfail', READ3resfail)}, from_parser=True)
@dataclass
class v_READ3res:
    status: nfsstat3
    resok: typing.Optional[READ3resok] = None
    resfail: typing.Optional[READ3resfail] = None


READ3res.val_base_class = v_READ3res



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

WRITE3res = rpchelp.union('WRITE3res', nfsstat3, 'status', {NFS3_OK: ('resok', WRITE3resok), None: ('resfail', WRITE3resfail)}, from_parser=True)
@dataclass
class v_WRITE3res:
    status: nfsstat3
    resok: typing.Optional[WRITE3resok] = None
    resfail: typing.Optional[WRITE3resfail] = None


WRITE3res.val_base_class = v_WRITE3res



class createmode3(rpchelp.enum):
    UNCHECKED = 0
    GUARDED = 1
    EXCLUSIVE = 2
createhow3 = rpchelp.union('createhow3', createmode3, 'mode', {UNCHECKED: ('obj_attributes', sattr3), GUARDED: ('obj_attributes', sattr3), EXCLUSIVE: ('verf', createverf3)}, from_parser=True)
@dataclass
class v_createhow3:
    mode: createmode3
    obj_attributes: typing.Optional[sattr3] = None
    verf: typing.Optional[bytes] = None


createhow3.val_base_class = v_createhow3



@dataclass
class CREATE3args(rpchelp.struct):
    where: diropargs3 = rpchelp.rpc_field(diropargs3)
    how: v_createhow3 = rpchelp.rpc_field(createhow3)

@dataclass
class CREATE3resok(rpchelp.struct):
    obj_handle: typing.Optional[bytes] = rpchelp.rpc_field(post_op_fh3)
    obj_attributes: typing.Optional[fattr3] = rpchelp.rpc_field(post_op_attr)
    dir_wcc: wcc_data = rpchelp.rpc_field(wcc_data)

@dataclass
class CREATE3resfail(rpchelp.struct):
    dir_wcc: wcc_data = rpchelp.rpc_field(wcc_data)

CREATE3res = rpchelp.union('CREATE3res', nfsstat3, 'status', {NFS3_OK: ('resok', CREATE3resok), None: ('resfail', CREATE3resfail)}, from_parser=True)
@dataclass
class v_CREATE3res:
    status: nfsstat3
    resok: typing.Optional[CREATE3resok] = None
    resfail: typing.Optional[CREATE3resfail] = None


CREATE3res.val_base_class = v_CREATE3res



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

MKDIR3res = rpchelp.union('MKDIR3res', nfsstat3, 'status', {NFS3_OK: ('resok', MKDIR3resok), None: ('resfail', MKDIR3resfail)}, from_parser=True)
@dataclass
class v_MKDIR3res:
    status: nfsstat3
    resok: typing.Optional[MKDIR3resok] = None
    resfail: typing.Optional[MKDIR3resfail] = None


MKDIR3res.val_base_class = v_MKDIR3res



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

SYMLINK3res = rpchelp.union('SYMLINK3res', nfsstat3, 'status', {NFS3_OK: ('resok', SYMLINK3resok), None: ('resfail', SYMLINK3resfail)}, from_parser=True)
@dataclass
class v_SYMLINK3res:
    status: nfsstat3
    resok: typing.Optional[SYMLINK3resok] = None
    resfail: typing.Optional[SYMLINK3resfail] = None


SYMLINK3res.val_base_class = v_SYMLINK3res



@dataclass
class devicedata3(rpchelp.struct):
    dev_attributes: sattr3 = rpchelp.rpc_field(sattr3)
    spec: specdata3 = rpchelp.rpc_field(specdata3)

mknoddata3 = rpchelp.union('mknoddata3', ftype3, 'type', {NF3CHR: ('chr_device', devicedata3), NF3BLK: ('blk_device', devicedata3), NF3SOCK: ('sock_pipe_attributes', sattr3), NF3FIFO: ('fifo_pipe_attributes', sattr3), None: (None, rpchelp.r_void)}, from_parser=True)
@dataclass
class v_mknoddata3:
    type: ftype3
    chr_device: typing.Optional[devicedata3] = None
    blk_device: typing.Optional[devicedata3] = None
    sock_pipe_attributes: typing.Optional[sattr3] = None
    fifo_pipe_attributes: typing.Optional[sattr3] = None


mknoddata3.val_base_class = v_mknoddata3



@dataclass
class MKNOD3args(rpchelp.struct):
    where: diropargs3 = rpchelp.rpc_field(diropargs3)
    what: v_mknoddata3 = rpchelp.rpc_field(mknoddata3)

@dataclass
class MKNOD3resok(rpchelp.struct):
    obj_handle: typing.Optional[bytes] = rpchelp.rpc_field(post_op_fh3)
    obj_attributes: typing.Optional[fattr3] = rpchelp.rpc_field(post_op_attr)
    dir_wcc: wcc_data = rpchelp.rpc_field(wcc_data)

@dataclass
class MKNOD3resfail(rpchelp.struct):
    dir_wcc: wcc_data = rpchelp.rpc_field(wcc_data)

MKNOD3res = rpchelp.union('MKNOD3res', nfsstat3, 'status', {NFS3_OK: ('resok', MKNOD3resok), None: ('resfail', MKNOD3resfail)}, from_parser=True)
@dataclass
class v_MKNOD3res:
    status: nfsstat3
    resok: typing.Optional[MKNOD3resok] = None
    resfail: typing.Optional[MKNOD3resfail] = None


MKNOD3res.val_base_class = v_MKNOD3res



@dataclass
class REMOVE3args(rpchelp.struct):
    object: diropargs3 = rpchelp.rpc_field(diropargs3)

@dataclass
class REMOVE3resok(rpchelp.struct):
    dir_wcc: wcc_data = rpchelp.rpc_field(wcc_data)

@dataclass
class REMOVE3resfail(rpchelp.struct):
    dir_wcc: wcc_data = rpchelp.rpc_field(wcc_data)

REMOVE3res = rpchelp.union('REMOVE3res', nfsstat3, 'status', {NFS3_OK: ('resok', REMOVE3resok), None: ('resfail', REMOVE3resfail)}, from_parser=True)
@dataclass
class v_REMOVE3res:
    status: nfsstat3
    resok: typing.Optional[REMOVE3resok] = None
    resfail: typing.Optional[REMOVE3resfail] = None


REMOVE3res.val_base_class = v_REMOVE3res



@dataclass
class RMDIR3args(rpchelp.struct):
    object: diropargs3 = rpchelp.rpc_field(diropargs3)

@dataclass
class RMDIR3resok(rpchelp.struct):
    dir_wcc: wcc_data = rpchelp.rpc_field(wcc_data)

@dataclass
class RMDIR3resfail(rpchelp.struct):
    dir_wcc: wcc_data = rpchelp.rpc_field(wcc_data)

RMDIR3res = rpchelp.union('RMDIR3res', nfsstat3, 'status', {NFS3_OK: ('resok', RMDIR3resok), None: ('resfail', RMDIR3resfail)}, from_parser=True)
@dataclass
class v_RMDIR3res:
    status: nfsstat3
    resok: typing.Optional[RMDIR3resok] = None
    resfail: typing.Optional[RMDIR3resfail] = None


RMDIR3res.val_base_class = v_RMDIR3res



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

RENAME3res = rpchelp.union('RENAME3res', nfsstat3, 'status', {NFS3_OK: ('resok', RENAME3resok), None: ('resfail', RENAME3resfail)}, from_parser=True)
@dataclass
class v_RENAME3res:
    status: nfsstat3
    resok: typing.Optional[RENAME3resok] = None
    resfail: typing.Optional[RENAME3resfail] = None


RENAME3res.val_base_class = v_RENAME3res



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

LINK3res = rpchelp.union('LINK3res', nfsstat3, 'status', {NFS3_OK: ('resok', LINK3resok), None: ('resfail', LINK3resfail)}, from_parser=True)
@dataclass
class v_LINK3res:
    status: nfsstat3
    resok: typing.Optional[LINK3resok] = None
    resfail: typing.Optional[LINK3resfail] = None


LINK3res.val_base_class = v_LINK3res



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

READDIR3res = rpchelp.union('READDIR3res', nfsstat3, 'status', {NFS3_OK: ('resok', READDIR3resok), None: ('resfail', READDIR3resfail)}, from_parser=True)
@dataclass
class v_READDIR3res:
    status: nfsstat3
    resok: typing.Optional[READDIR3resok] = None
    resfail: typing.Optional[READDIR3resfail] = None


READDIR3res.val_base_class = v_READDIR3res



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

READDIRPLUS3res = rpchelp.union('READDIRPLUS3res', nfsstat3, 'status', {NFS3_OK: ('resok', READDIRPLUS3resok), None: ('resfail', READDIRPLUS3resfail)}, from_parser=True)
@dataclass
class v_READDIRPLUS3res:
    status: nfsstat3
    resok: typing.Optional[READDIRPLUS3resok] = None
    resfail: typing.Optional[READDIRPLUS3resfail] = None


READDIRPLUS3res.val_base_class = v_READDIRPLUS3res



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

FSSTAT3res = rpchelp.union('FSSTAT3res', nfsstat3, 'status', {NFS3_OK: ('resok', FSSTAT3resok), None: ('resfail', FSSTAT3resfail)}, from_parser=True)
@dataclass
class v_FSSTAT3res:
    status: nfsstat3
    resok: typing.Optional[FSSTAT3resok] = None
    resfail: typing.Optional[FSSTAT3resfail] = None


FSSTAT3res.val_base_class = v_FSSTAT3res



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

FSINFO3res = rpchelp.union('FSINFO3res', nfsstat3, 'status', {NFS3_OK: ('resok', FSINFO3resok), None: ('resfail', FSINFO3resfail)}, from_parser=True)
@dataclass
class v_FSINFO3res:
    status: nfsstat3
    resok: typing.Optional[FSINFO3resok] = None
    resfail: typing.Optional[FSINFO3resfail] = None


FSINFO3res.val_base_class = v_FSINFO3res



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

PATHCONF3res = rpchelp.union('PATHCONF3res', nfsstat3, 'status', {NFS3_OK: ('resok', PATHCONF3resok), None: ('resfail', PATHCONF3resfail)}, from_parser=True)
@dataclass
class v_PATHCONF3res:
    status: nfsstat3
    resok: typing.Optional[PATHCONF3resok] = None
    resfail: typing.Optional[PATHCONF3resfail] = None


PATHCONF3res.val_base_class = v_PATHCONF3res



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

COMMIT3res = rpchelp.union('COMMIT3res', nfsstat3, 'status', {NFS3_OK: ('resok', COMMIT3resok), None: ('resfail', COMMIT3resfail)}, from_parser=True)
@dataclass
class v_COMMIT3res:
    status: nfsstat3
    resok: typing.Optional[COMMIT3resok] = None
    resfail: typing.Optional[COMMIT3resfail] = None


COMMIT3res.val_base_class = v_COMMIT3res



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

mountres3 = rpchelp.union('mountres3', mountstat3, 'fhs_status', {MNT3_OK: ('mountinfo', mountres3_ok), None: (None, rpchelp.r_void)}, from_parser=True)
@dataclass
class v_mountres3:
    fhs_status: mountstat3
    mountinfo: typing.Optional[mountres3_ok] = None


mountres3.val_base_class = v_mountres3



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
    def GETATTR(self, arg_0: GETATTR3args) -> v_GETATTR3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def SETATTR(self, arg_0: SETATTR3args) -> v_SETATTR3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def LOOKUP(self, arg_0: LOOKUP3args) -> v_LOOKUP3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def ACCESS(self, arg_0: ACCESS3args) -> v_ACCESS3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def READLINK(self, arg_0: READLINK3args) -> v_READLINK3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def READ(self, arg_0: READ3args) -> v_READ3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def WRITE(self, arg_0: WRITE3args) -> v_WRITE3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def CREATE(self, arg_0: CREATE3args) -> v_CREATE3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def MKDIR(self, arg_0: MKDIR3args) -> v_MKDIR3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def SYMLINK(self, arg_0: SYMLINK3args) -> v_SYMLINK3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def MKNOD(self, arg_0: MKNOD3args) -> v_MKNOD3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def REMOVE(self, arg_0: REMOVE3args) -> v_REMOVE3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def RMDIR(self, arg_0: RMDIR3args) -> v_RMDIR3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def RENAME(self, arg_0: RENAME3args) -> v_RENAME3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def LINK(self, arg_0: LINK3args) -> v_LINK3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def READDIR(self, arg_0: READDIR3args) -> v_READDIR3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def READDIRPLUS(self, arg_0: READDIRPLUS3args) -> v_READDIRPLUS3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def FSSTAT(self, arg_0: FSSTAT3args) -> v_FSSTAT3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def FSINFO(self, arg_0: FSINFO3args) -> v_FSINFO3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def PATHCONF(self, arg_0: PATHCONF3args) -> v_PATHCONF3res:
        raise NotImplementedError()

    @abc.abstractmethod
    def COMMIT(self, arg_0: COMMIT3args) -> v_COMMIT3res:
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

    async def GETATTR(self, arg_0: GETATTR3args) -> client.UnpackedRPCMsg[v_GETATTR3res]:
        return await self.send_call(1, arg_0)

    async def SETATTR(self, arg_0: SETATTR3args) -> client.UnpackedRPCMsg[v_SETATTR3res]:
        return await self.send_call(2, arg_0)

    async def LOOKUP(self, arg_0: LOOKUP3args) -> client.UnpackedRPCMsg[v_LOOKUP3res]:
        return await self.send_call(3, arg_0)

    async def ACCESS(self, arg_0: ACCESS3args) -> client.UnpackedRPCMsg[v_ACCESS3res]:
        return await self.send_call(4, arg_0)

    async def READLINK(self, arg_0: READLINK3args) -> client.UnpackedRPCMsg[v_READLINK3res]:
        return await self.send_call(5, arg_0)

    async def READ(self, arg_0: READ3args) -> client.UnpackedRPCMsg[v_READ3res]:
        return await self.send_call(6, arg_0)

    async def WRITE(self, arg_0: WRITE3args) -> client.UnpackedRPCMsg[v_WRITE3res]:
        return await self.send_call(7, arg_0)

    async def CREATE(self, arg_0: CREATE3args) -> client.UnpackedRPCMsg[v_CREATE3res]:
        return await self.send_call(8, arg_0)

    async def MKDIR(self, arg_0: MKDIR3args) -> client.UnpackedRPCMsg[v_MKDIR3res]:
        return await self.send_call(9, arg_0)

    async def SYMLINK(self, arg_0: SYMLINK3args) -> client.UnpackedRPCMsg[v_SYMLINK3res]:
        return await self.send_call(10, arg_0)

    async def MKNOD(self, arg_0: MKNOD3args) -> client.UnpackedRPCMsg[v_MKNOD3res]:
        return await self.send_call(11, arg_0)

    async def REMOVE(self, arg_0: REMOVE3args) -> client.UnpackedRPCMsg[v_REMOVE3res]:
        return await self.send_call(12, arg_0)

    async def RMDIR(self, arg_0: RMDIR3args) -> client.UnpackedRPCMsg[v_RMDIR3res]:
        return await self.send_call(13, arg_0)

    async def RENAME(self, arg_0: RENAME3args) -> client.UnpackedRPCMsg[v_RENAME3res]:
        return await self.send_call(14, arg_0)

    async def LINK(self, arg_0: LINK3args) -> client.UnpackedRPCMsg[v_LINK3res]:
        return await self.send_call(15, arg_0)

    async def READDIR(self, arg_0: READDIR3args) -> client.UnpackedRPCMsg[v_READDIR3res]:
        return await self.send_call(16, arg_0)

    async def READDIRPLUS(self, arg_0: READDIRPLUS3args) -> client.UnpackedRPCMsg[v_READDIRPLUS3res]:
        return await self.send_call(17, arg_0)

    async def FSSTAT(self, arg_0: FSSTAT3args) -> client.UnpackedRPCMsg[v_FSSTAT3res]:
        return await self.send_call(18, arg_0)

    async def FSINFO(self, arg_0: FSINFO3args) -> client.UnpackedRPCMsg[v_FSINFO3res]:
        return await self.send_call(19, arg_0)

    async def PATHCONF(self, arg_0: PATHCONF3args) -> client.UnpackedRPCMsg[v_PATHCONF3res]:
        return await self.send_call(20, arg_0)

    async def COMMIT(self, arg_0: COMMIT3args) -> client.UnpackedRPCMsg[v_COMMIT3res]:
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
    def MNT(self, arg_0: bytes) -> v_mountres3:
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

    async def MNT(self, arg_0: bytes) -> client.UnpackedRPCMsg[v_mountres3]:
        return await self.send_call(1, arg_0)

    async def DUMP(self) -> client.UnpackedRPCMsg[typing.List[mountlist]]:
        return await self.send_call(2, )

    async def UMNT(self, arg_0: bytes) -> client.UnpackedRPCMsg[None]:
        return await self.send_call(3, arg_0)

    async def UMNTALL(self) -> client.UnpackedRPCMsg[None]:
        return await self.send_call(4, )

    async def EXPORT(self) -> client.UnpackedRPCMsg[typing.List[exportlist]]:
        return await self.send_call(5, )

__all__ = ['nfsstat3', 'ftype3', 'specdata3', 'nfstime3', 'fattr3', 'v_post_op_attr', 'wcc_attr', 'v_pre_op_attr', 'wcc_data', 'v_post_op_fh3', 'time_how', 'v_set_mode3', 'v_set_uid3', 'v_set_gid3', 'v_set_size3', 'v_set_atime', 'v_set_mtime', 'sattr3', 'diropargs3', 'GETATTR3args', 'GETATTR3resok', 'v_GETATTR3res', 'v_sattrguard3', 'SETATTR3args', 'SETATTR3resok', 'SETATTR3resfail', 'v_SETATTR3res', 'LOOKUP3args', 'LOOKUP3resok', 'LOOKUP3resfail', 'v_LOOKUP3res', 'ACCESS3args', 'ACCESS3resok', 'ACCESS3resfail', 'v_ACCESS3res', 'READLINK3args', 'READLINK3resok', 'READLINK3resfail', 'v_READLINK3res', 'READ3args', 'READ3resok', 'READ3resfail', 'v_READ3res', 'stable_how', 'WRITE3args', 'WRITE3resok', 'WRITE3resfail', 'v_WRITE3res', 'createmode3', 'v_createhow3', 'CREATE3args', 'CREATE3resok', 'CREATE3resfail', 'v_CREATE3res', 'MKDIR3args', 'MKDIR3resok', 'MKDIR3resfail', 'v_MKDIR3res', 'symlinkdata3', 'SYMLINK3args', 'SYMLINK3resok', 'SYMLINK3resfail', 'v_SYMLINK3res', 'devicedata3', 'v_mknoddata3', 'MKNOD3args', 'MKNOD3resok', 'MKNOD3resfail', 'v_MKNOD3res', 'REMOVE3args', 'REMOVE3resok', 'REMOVE3resfail', 'v_REMOVE3res', 'RMDIR3args', 'RMDIR3resok', 'RMDIR3resfail', 'v_RMDIR3res', 'RENAME3args', 'RENAME3resok', 'RENAME3resfail', 'v_RENAME3res', 'LINK3args', 'LINK3resok', 'LINK3resfail', 'v_LINK3res', 'READDIR3args', 'entry3', 'dirlist3', 'READDIR3resok', 'READDIR3resfail', 'v_READDIR3res', 'READDIRPLUS3args', 'entryplus3', 'dirlistplus3', 'READDIRPLUS3resok', 'READDIRPLUS3resfail', 'v_READDIRPLUS3res', 'FSSTAT3args', 'FSSTAT3resok', 'FSSTAT3resfail', 'v_FSSTAT3res', 'FSINFO3args', 'FSINFO3resok', 'FSINFO3resfail', 'v_FSINFO3res', 'PATHCONF3args', 'PATHCONF3resok', 'PATHCONF3resfail', 'v_PATHCONF3res', 'COMMIT3args', 'COMMIT3resok', 'COMMIT3resfail', 'v_COMMIT3res', 'mountstat3', 'mountres3_ok', 'v_mountres3', 'mountlist', 'grouplist', 'exportlist', 'NFS_PROGRAM_3_SERVER', 'MOUNT_PROGRAM_3_SERVER', 'TRUE', 'FALSE', 'NFS3_FHSIZE', 'NFS3_COOKIEVERFSIZE', 'NFS3_CREATEVERFSIZE', 'NFS3_WRITEVERFSIZE', 'NFS3_OK', 'NFS3ERR_PERM', 'NFS3ERR_NOENT', 'NFS3ERR_IO', 'NFS3ERR_NXIO', 'NFS3ERR_ACCES', 'NFS3ERR_EXIST', 'NFS3ERR_XDEV', 'NFS3ERR_NODEV', 'NFS3ERR_NOTDIR', 'NFS3ERR_ISDIR', 'NFS3ERR_INVAL', 'NFS3ERR_FBIG', 'NFS3ERR_NOSPC', 'NFS3ERR_ROFS', 'NFS3ERR_MLINK', 'NFS3ERR_NAMETOOLONG', 'NFS3ERR_NOTEMPTY', 'NFS3ERR_DQUOT', 'NFS3ERR_STALE', 'NFS3ERR_REMOTE', 'NFS3ERR_BADHANDLE', 'NFS3ERR_NOT_SYNC', 'NFS3ERR_BAD_COOKIE', 'NFS3ERR_NOTSUPP', 'NFS3ERR_TOOSMALL', 'NFS3ERR_SERVERFAULT', 'NFS3ERR_BADTYPE', 'NFS3ERR_JUKEBOX', 'NF3REG', 'NF3DIR', 'NF3BLK', 'NF3CHR', 'NF3LNK', 'NF3SOCK', 'NF3FIFO', 'DONT_CHANGE', 'SET_TO_SERVER_TIME', 'SET_TO_CLIENT_TIME', 'ACCESS3_READ', 'ACCESS3_LOOKUP', 'ACCESS3_MODIFY', 'ACCESS3_EXTEND', 'ACCESS3_DELETE', 'ACCESS3_EXECUTE', 'UNSTABLE', 'DATA_SYNC', 'FILE_SYNC', 'UNCHECKED', 'GUARDED', 'EXCLUSIVE', 'FSF3_LINK', 'FSF3_SYMLINK', 'FSF3_HOMOGENEOUS', 'FSF3_CANSETTIME', 'MNTPATHLEN', 'MNTNAMLEN', 'FHSIZE3', 'MNT3_OK', 'MNT3ERR_PERM', 'MNT3ERR_NOENT', 'MNT3ERR_IO', 'MNT3ERR_ACCES', 'MNT3ERR_NOTDIR', 'MNT3ERR_INVAL', 'MNT3ERR_NAMETOOLONG', 'MNT3ERR_NOTSUPP', 'MNT3ERR_SERVERFAULT']
