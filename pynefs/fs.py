import abc
import datetime as dt
import dataclasses
import enum
import hmac
import math
import secrets
import struct
import weakref
from typing import *

from pynefs.generated import rfc1094 as nfs2


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

    def to_nfs2(self, mode) -> Tuple[int, nfs2.Ftype]:
        if self in (self.SOCK, self.FIFO):
            f_type = nfs2.Ftype.NFNON
        else:
            f_type = nfs2.Ftype(self)
        return mode | self._nfs2_mode_mask(), f_type


def date_to_nfs2(date: dt.datetime) -> nfs2.Timeval:
    ts = date.timestamp()
    frac, whole = math.modf(ts)
    return nfs2.Timeval(math.floor(whole), math.floor(frac * 1_000_000))


def fsid_to_nfs2(fsid: bytes) -> int:
    return struct.unpack("!L", fsid[:4])[0]


@dataclasses.dataclass
class BaseFSEntry:
    fs: weakref.ReferenceType
    parent_id: Optional[int]
    fileid: int
    name: bytes
    type: FileType = dataclasses.field(init=False)
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

    @property
    def fsid(self) -> bytes:
        return self.fs().fsid

    @property
    def nfs2_cookie(self) -> bytes:
        return struct.pack("!L", self.fileid)

    def to_nfs2_fattr(self) -> nfs2.FAttr:
        mode, f_type = self.type.to_nfs2(self.mode)
        return nfs2.FAttr(
            type=f_type,
            mode=mode,
            nlink=self.nlink,
            uid=self.uid,
            gid=self.gid,
            size=self.size,
            blocksize=self.fs().block_size,
            rdev=self.rdev,
            blocks=self.blocks,
            fsid=fsid_to_nfs2(self.fsid),
            fileid=self.fileid,
            atime=date_to_nfs2(self.atime),
            mtime=date_to_nfs2(self.mtime),
            ctime=date_to_nfs2(self.ctime),
        )


@dataclasses.dataclass
class File(BaseFSEntry):
    contents: bytes

    def __post_init__(self):
        self.type = FileType.REG


@dataclasses.dataclass
class SymLink(BaseFSEntry):
    contents: bytes

    def __post_init__(self):
        self.type = FileType.LINK


@dataclasses.dataclass
class Directory(BaseFSEntry):
    child_ids: List[int]
    root_dir: bool = False

    def __post_init__(self):
        self.type = FileType.DIR

    def add_child(self, child: FSENTRY):
        if child.fileid in self.child_ids:
            return
        assert(child.fs == self.fs)
        child.parent_id = self.fileid
        self.child_ids.append(child.fileid)

        fs: BaseFS = self.fs()
        if child not in fs.entries:
            fs.entries.append(child)

    def get_child_by_name(self, name: bytes) -> Optional[FSENTRY]:
        for entry in self.children:
            if entry.name == name:
                return entry
        return None

    def _make_upper_dir_link(self):
        if self.parent_id is not None:
            parent: Directory = self.fs().get_entry_by_id(self.parent_id)
            return dataclasses.replace(
                parent,
                name=b"..",
                child_ids=[self.fileid],
            )

        assert self.root_dir

        # Need to make a fake entry for `..` since it's actually above
        # the root directory. Ironically none of the info other than the
        # name seems to be used in the dir listing.
        return Directory(
            fs=weakref.ref(self),
            mode=0o0555,
            nlink=2,
            uid=1000,
            gid=1000,
            size=4096,
            rdev=0,
            blocks=1,
            # Not a real file so should be fine?
            # fileid may NOT be 0 or clients will ignore it!
            fileid=(~self.fileid) & 0xFFffFFff,
            atime=dt.datetime.utcnow(),
            mtime=dt.datetime.utcnow(),
            ctime=dt.datetime.utcnow(),
            name=b"..",
            child_ids=[self.fileid],
            root_dir=False,
            parent_id=None,
        )

    @property
    def children(self) -> List[FSENTRY]:
        fs: BaseFS = self.fs()
        files = [
            dataclasses.replace(self, name=b"."),
            self._make_upper_dir_link(),
            *[fs.get_entry_by_id(fileid) for fileid in self.child_ids]
        ]
        assert(all(files))
        return files


class BaseFS(abc.ABC):
    fsid: bytes
    fh: bytes
    block_size: int
    num_blocks: int
    free_blocks: int
    avail_blocks: int
    root_path: bytes
    entries: List[FSENTRY]

    def get_entry_by_id(self, fileid: int) -> Optional[FSENTRY]:
        for entry in self.entries:
            if entry.fileid == fileid:
                return entry
        return None

    def get_descendants(self, entry: FSENTRY) -> Generator[FSENTRY, None, None]:
        if not isinstance(entry, Directory):
            return
        for fileid in entry.child_ids:
            child = self.get_entry_by_id(fileid)
            yield child
            yield from self.get_descendants(child)

    def remove_entry(self, entry: FSENTRY):
        """Completely remove an entry and its subtree from the FS"""
        if entry.parent_id is not None:
            parent: Directory = self.get_entry_by_id(entry.parent_id)
            parent.child_ids.remove(entry.fileid)
        for descendant in self.get_descendants(entry):
            self.entries.remove(descendant)
        self.entries.remove(entry)

    def sanity_check(self):
        # Not multi-rooted
        assert sum(getattr(entry, 'root_dir', False) for entry in self.entries) == 1
        # Everything correctly rooted
        assert all(getattr(entry, 'root_dir', False) or entry.parent_id is not None for entry in self.entries)
        # Unique fileids
        assert len(set(e.fileid for e in self.entries)) == len(self.entries)
        for entry in self.entries:
            if entry.parent_id is not None:
                parent = self.get_entry_by_id(entry.parent_id)
                assert parent
                assert entry.fileid in parent.child_ids


@dataclasses.dataclass
class DecodedFileHandle:
    fileid: int
    fsid: bytes


class FileHandleEncoder(abc.ABC):
    @abc.abstractmethod
    def encode(self, entry: Union[FSENTRY, DecodedFileHandle], nfs_v2=False) -> bytes:
        pass

    @abc.abstractmethod
    def decode(self, fh: bytes, nfs_v2=False) -> DecodedFileHandle:
        pass


class VerifyingFileHandleEncoder(FileHandleEncoder):
    def __init__(self, hmac_secret):
        self.hmac_secret = hmac_secret

    @staticmethod
    def _mac_len(nfs_v2=False):
        return 16 if nfs_v2 else 32

    def _calc_mac(self, data: bytes, nfs_v2=False):
        # Truncated sha256 isn't recommended, but fine for our purposes.
        # We're limited to 32 byte FHs if we want to support NFSv2 so
        # we don't really have a choice.
        digest = hmac.new(self.hmac_secret, data, 'sha256').digest()
        return digest[:self._mac_len(nfs_v2)]

    def encode(self, entry: Union[FSENTRY, DecodedFileHandle], nfs_v2=False) -> bytes:
        payload = struct.pack("!Q", entry.fileid) + entry.fsid
        return self._calc_mac(payload, nfs_v2) + payload

    def decode(self, fh: bytes, nfs_v2=False) -> DecodedFileHandle:
        mac_len = self._mac_len(nfs_v2)
        expected_len = 16 + mac_len
        if len(fh) != expected_len:
            raise ValueError(f"FH {fh!r} is not {expected_len} bytes")
        mac, payload = fh[:mac_len], fh[mac_len:]
        if not secrets.compare_digest(mac, self._calc_mac(payload, nfs_v2)):
            raise ValueError(f"FH {fh!r} failed sig check")
        return DecodedFileHandle(struct.unpack("!Q", payload[:8])[0], payload[8:])


class FileSystemManager:
    def __init__(self, handle_encoder, filesystems):
        self.handle_encoder: FileHandleEncoder = handle_encoder
        self.filesystems: Dict[bytes, BaseFS] = {f.fsid: f for f in filesystems}

    def get_fs_by_root(self, root_path) -> Optional[BaseFS]:
        for fs in self.filesystems.values():
            if fs.root_path == root_path:
                return fs
        return None

    def get_fs_by_fh(self, fh: bytes, nfs_v2=False) -> Optional[BaseFS]:
        decoded = self.handle_encoder.decode(fh, nfs_v2)
        # TODO: check that fileid matches root dir?
        return self.filesystems.get(decoded.fsid)

    def get_entry_by_fh(self, fh: bytes, nfs_v2=False) -> Optional[FSENTRY]:
        decoded = self.handle_encoder.decode(fh, nfs_v2)
        fs = self.filesystems.get(decoded.fsid)
        if not fs:
            return None
        return fs.get_entry_by_id(decoded.fileid)

    def entry_to_fh(self, entry: FSENTRY, nfs_v2=False):
        return self.handle_encoder.encode(entry, nfs_v2)
