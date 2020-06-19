import abc
import secrets
import weakref
from binascii import crc32
from dataclasses import dataclass
from typing import *

from pynefs.generated.rfc1094 import *


INODE = Union["File", "Directory"]


@dataclass
class File(v_fattr):
    fs: weakref.ReferenceType
    fsid: int
    fh: bytes
    name: bytes

    @staticmethod
    def _type_to_mode_mask(f_type: ftype):
        return {
            ftype.NFCHR: 0o0020000,
            ftype.NFDIR: 0o0040000,
            ftype.NFBLK: 0o0060000,
            ftype.NFREG: 0o0100000,
            ftype.NFLNK: 0o0120000,
            ftype.NFNON: 0o0140000,
        }[f_type]

    def to_fattr(self) -> v_fattr:
        return v_fattr(
            type=self.type,
            # https://tools.ietf.org/html/rfc1094#section-2.3.5
            # NFSv2 specific protocol weirdness
            mode=self.mode | self._type_to_mode_mask(self.type),
            nlink=self.nlink,
            uid=self.uid,
            gid=self.gid,
            size=self.size,
            blocksize=self.blocksize,
            rdev=self.rdev,
            blocks=self.blocks,
            fsid=self.fsid,
            fileid=self.fileid,
            atime=self.atime,
            mtime=self.mtime,
            ctime=self.ctime,
        )


@dataclass
class Directory(File):
    child_fhs: List[bytes]

    def get_child_by_name(self, name: bytes) -> Optional[INODE]:
        fs: BaseFS = self.fs()
        for fh in self.child_fhs:
            inode = fs.get_inode_by_fh(fh)
            if inode.name == name:
                return inode
        return None

    @property
    def children(self) -> List[INODE]:
        fs: BaseFS = self.fs()
        files = [fs.get_inode_by_fh(fh) for fh in self.child_fhs]
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
    inodes: List[File]

    def get_inode_by_fh(self, fh) -> Optional[INODE]:
        for inode in self.inodes:
            if inode.fh == fh:
                return inode
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
        self.inodes = [
            Directory(
                fs=weakref.ref(self),
                type=ftype.NFDIR,
                mode=0o0755,
                # . and ..
                nlink=2,
                uid=1000,
                gid=1000,
                size=4096,
                blocksize=self.block_size,
                rdev=0,
                blocks=1,
                fsid=self.fsid,
                fileid=crc32(self.fh),
                atime=v_timeval(0, 1),
                mtime=v_timeval(0, 1),
                ctime=v_timeval(0, 1),
                fh=self.fh,
                name=b"",
                child_fhs=[],
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

    def get_inode_by_fh(self, fh: bytes) -> Optional[INODE]:
        for fs in self.filesystems:
            inode = fs.get_inode_by_fh(fh)
            if inode is not None:
                return inode
        return None
