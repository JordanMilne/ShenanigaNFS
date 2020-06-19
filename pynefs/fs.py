import abc
import datetime as dt
import dataclasses
import enum
import math
import secrets
import weakref
from binascii import crc32
from typing import *

from pynefs.generated import rfc1094 as nfs2
from pynefs.generated.rfc1094 import ftype as ftype2  # to appease busted typecheck


FSENTRY = Union["File", "Directory", "SymLink", "BaseFSEntry"]


# Portable-ish between NFS2/3/4
class FileType(enum.IntEnum):
    REG = 1
    DIR = 2
    BLCK = 3
    CHAR = 4
    # Specifically a symbolic link, no way to differentiate hardlinks?
    LINK = 5
    SOCK = 6
    FIFO = 7

    # https://tools.ietf.org/html/rfc1094#section-2.3.5
    # NFSv2 specific protocol weirdness
    def _nfs2_mode_mask(self):
        return {
            self.CHAR: 0o0020000,
            self.DIR: 0o0040000,
            self.BLCK: 0o0060000,
            self.REG: 0o0100000,
            self.LINK: 0o0120000,
            self.SOCK: 0o0140000,
            # XXX: Not clear how FIFOs should be represented.
            # Same as sockets I guess?
            self.FIFO: 0o0140000,
        }[self]

    def to_nfs2(self, mode) -> Tuple[int, nfs2.ftype]:
        if self in (self.SOCK, self.FIFO):
            f_type = nfs2.ftype.NFNON
        else:
            f_type = ftype2(self)
        return mode | self._nfs2_mode_mask(), f_type


def date_to_nfs2(date: dt.datetime) -> nfs2.v_timeval:
    ts = date.timestamp()
    frac, whole = math.modf(ts)
    return nfs2.v_timeval(math.floor(whole), math.floor(frac * 1_000_000))


@dataclasses.dataclass
class BaseFSEntry:
    fs: weakref.ReferenceType
    fh: bytes
    parent_fh: Optional[bytes]
    fileid: int
    name: bytes
    type: FileType
    mode: int
    nlink: int
    uid: int
    gid: int
    size: int
    rdev: int
    blocks: int
    atime: dt.datetime
    mtime: dt.datetime
    ctime: dt.datetime

    def to_fattr(self) -> nfs2.v_fattr:
        mode, f_type = self.type.to_nfs2(self.mode)
        return nfs2.v_fattr(
            type=f_type,
            mode=mode,
            nlink=self.nlink,
            uid=self.uid,
            gid=self.gid,
            size=self.size,
            blocksize=self.fs().block_size,
            rdev=self.rdev,
            blocks=self.blocks,
            fsid=self.fs().fsid,
            fileid=self.fileid,
            atime=date_to_nfs2(self.atime),
            mtime=date_to_nfs2(self.mtime),
            ctime=date_to_nfs2(self.ctime),
        )


@dataclasses.dataclass
class File(BaseFSEntry):
    contents: bytes


@dataclasses.dataclass
class SymLink(File):
    pass


@dataclasses.dataclass
class Directory(BaseFSEntry):
    child_fhs: List[bytes]
    root_dir: bool = False

    def get_child_by_name(self, name: bytes) -> Optional[FSENTRY]:
        for entry in self.dir_listing:
            if entry.name == name:
                return entry
        return None

    def _make_upper_dir_link(self):
        if self.parent_fh:
            return dataclasses.replace(
                self.fs().get_entry_by_fh(self.parent_fh),
                name=b"..",
                child_fhs=[self.fh],
            )

        assert self.root_dir

        # Need to make a fake entry for `..` since it's actually above
        # the root directory. Ironically none of the info other than the
        # name seems to be used in the dir listing.
        return Directory(
            fs=weakref.ref(self),
            type=FileType.DIR,
            mode=0o0755,
            # . and ..
            nlink=0,
            uid=1000,
            gid=1000,
            size=4096,
            rdev=0,
            blocks=1,
            # Not a real file so should be fine?
            fileid=0,
            atime=dt.datetime.utcnow(),
            mtime=dt.datetime.utcnow(),
            ctime=dt.datetime.utcnow(),
            fh=b"\xff" * 32,
            name=b"..",
            child_fhs=[self.fh],
            root_dir=False,
            parent_fh=None,
        )

    @property
    def dir_listing(self) -> List[FSENTRY]:
        fs: BaseFS = self.fs()
        files = [
            dataclasses.replace(self, name=b"."),
            self._make_upper_dir_link(),
            *[fs.get_entry_by_fh(fh) for fh in self.child_fhs]
        ]
        assert(all(files))
        return files


class BaseFS(abc.ABC):
    fsid: int
    fh: bytes
    block_size: int
    num_blocks: int
    free_blocks: int
    avail_blocks: int
    root_path: bytes
    entries: List[FSENTRY]

    def get_entry_by_fh(self, fh) -> Optional[FSENTRY]:
        for entry in self.entries:
            if entry.fh == fh:
                return entry
        return None


class NullFS(BaseFS):
    def __init__(self, root_path):
        super().__init__()
        self.fh = secrets.token_bytes(32)
        self.fsid = 0
        self.block_size = 4096
        self.num_blocks = 1
        self.free_blocks = 0
        self.avail_blocks = 0
        self.root_path = root_path
        self.entries = [
            Directory(
                fs=weakref.ref(self),
                type=FileType.DIR,
                mode=0o0755,
                # . and ..
                nlink=2,
                uid=1000,
                gid=1000,
                size=4096,
                rdev=0,
                blocks=1,
                fileid=crc32(self.fh),
                atime=dt.datetime.utcnow(),
                mtime=dt.datetime.utcnow(),
                ctime=dt.datetime.utcnow(),
                fh=self.fh,
                name=b"",
                child_fhs=[],
                root_dir=True,
                parent_fh=None,
            )
        ]


class FileSystemManager:
    def __init__(self, filesystems):
        self.filesystems: List[BaseFS] = filesystems

    def get_fs_by_root(self, root_path) -> Optional[BaseFS]:
        for fs in self.filesystems:
            if fs.root_path == root_path:
                return fs
        return None

    def get_fs_by_fh(self, fh: bytes) -> Optional[BaseFS]:
        for fs in self.filesystems:
            if fs.fh == fh:
                return fs
        return None

    def get_entry_by_fh(self, fh: bytes) -> Optional[FSENTRY]:
        for fs in self.filesystems:
            entry = fs.get_entry_by_fh(fh)
            if entry is not None:
                return entry
        return None
