import abc
import dataclasses
import datetime as dt
import enum
import hmac
import math
import secrets
import struct
import weakref
from typing import *

from pynefs.generated import rfc1094 as nfs2


FSENTRY = Union["File", "Directory", "SymLink", "BaseFSEntry", "FSEntryProxy"]


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


def fsid_to_nfs2(fsid: int) -> int:
    return fsid & 0xFFffFFff


class BaseFSEntry(abc.ABC):
    fs: weakref.ReferenceType
    parent_id: Optional[int]
    fileid: Optional[int]
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

    @property
    def fsid(self):
        return self.fs().fsid

    @property
    def nfs2_cookie(self) -> bytes:
        return struct.pack("!L", self.fileid & 0xFFffFFff)

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
            fsid=fsid_to_nfs2(self.fs().fsid),
            fileid=self.fileid,
            atime=date_to_nfs2(self.atime),
            mtime=date_to_nfs2(self.mtime),
            ctime=date_to_nfs2(self.ctime),
        )


class FSEntryProxy:
    def __init__(self, base: FSENTRY, replacements: Dict[str, Any]):
        self.base = base
        self.replacements = replacements

    def __getattr__(self, item):
        if item in self.replacements:
            return self.replacements[item]
        return getattr(self.base, item)


class File(BaseFSEntry, abc.ABC):
    contents: bytes
    type: Literal[FileType.REG]


class SymLink(BaseFSEntry, abc.ABC):
    contents: bytes
    type: Literal[FileType.LINK]


class Directory(BaseFSEntry, abc.ABC):
    child_ids: List[int]
    type: Literal[FileType.DIR]
    root_dir: bool = False

    def link_child(self, child: FSENTRY):
        assert (child.fs == self.fs)
        fs: BaseFS = self.fs()
        if child.fileid is None:
            fs.track_entry(child)
        elif child.fileid in self.child_ids:
            return

        child.parent_id = self.fileid
        self.child_ids.append(child.fileid)

    def unlink_child(self, child: FSENTRY):
        assert child.fileid in self.child_ids
        self.child_ids.remove(child.fileid)
        child.parent_id = None

    def get_child_by_name(self, name: bytes) -> Optional[FSENTRY]:
        for entry in self.children:
            if entry.name == name:
                return entry
        return None

    def _make_upper_dir_link(self):
        if self.parent_id is not None:
            parent: Directory = self.fs().get_entry_by_id(self.parent_id)
            return FSEntryProxy(
                base=parent,
                replacements={
                    "name": b"..",
                },
            )

        assert self.root_dir

        # Need to make a fake entry for `..` since it's actually above
        # the root directory. Ironically none of the info other than the
        # name seems to be used in the dir listing.
        return FSEntryProxy(
            base=self,
            replacements={
                # `1` will never be used by legitimate files and
                # is not actually tracked
                "fileid": 1,
                "name": b"..",
                "child_ids": [self.fileid],
                "root_dir": False,
            }
        )

    @property
    def children(self) -> List[FSENTRY]:
        fs: BaseFS = self.fs()
        files = [
            FSEntryProxy(self, {"name": b"."}),
            self._make_upper_dir_link(),
            *[fs.get_entry_by_id(fileid) for fileid in self.child_ids]
        ]
        assert(all(files))
        return files


@dataclasses.dataclass
class SimpleFSEntry(BaseFSEntry):
    fs: weakref.ReferenceType
    name: bytes
    mode: int
    size: int = dataclasses.field(init=False, default=0)
    fileid: Optional[int] = dataclasses.field(default=None)
    type: FileType = dataclasses.field(init=False)
    parent_id: Optional[int] = dataclasses.field(default=None)
    nlink: int = dataclasses.field(default=1)
    uid: int = dataclasses.field(default=65534)
    gid: int = dataclasses.field(default=65534)
    rdev: int = dataclasses.field(default=0)
    blocks: int = dataclasses.field(default=1)
    atime: dt.datetime = dataclasses.field(default_factory=dt.datetime.utcnow)
    mtime: dt.datetime = dataclasses.field(default_factory=dt.datetime.utcnow)
    ctime: dt.datetime = dataclasses.field(default_factory=dt.datetime.utcnow)


@dataclasses.dataclass
class SimpleFile(File, SimpleFSEntry):
    contents: bytearray = dataclasses.field(default_factory=bytearray)
    type: FileType = dataclasses.field(default=FileType.REG, init=False)

    @property
    def size(self) -> int:
        return len(self.contents)


@dataclasses.dataclass
class SimpleSymlink(SymLink, SimpleFSEntry):
    contents: bytearray = dataclasses.field(default_factory=bytearray)
    type: FileType = dataclasses.field(default=FileType.LINK, init=False)

    @property
    def size(self) -> int:
        return len(self.contents)


@dataclasses.dataclass
class SimpleDirectory(Directory, SimpleFSEntry):
    type: FileType = dataclasses.field(default=FileType.DIR, init=False)
    child_ids: List[int] = dataclasses.field(default_factory=list)
    root_dir: bool = dataclasses.field(default=False)


class BaseFS(abc.ABC):
    fsid: int
    block_size: int
    num_blocks: int
    free_blocks: int
    avail_blocks: int
    root_path: bytes
    root_dir: Optional[Directory]

    def __init__(self):
        self.fsid = secrets.randbits(64)
        self.block_size = 4096

    @abc.abstractmethod
    def get_entry_by_id(self, fileid: int) -> Optional[FSENTRY]:
        raise NotImplementedError()

    @abc.abstractmethod
    def track_entry(self, entry: FSENTRY):
        raise NotImplementedError()

    @abc.abstractmethod
    def remove_entry(self, entry: FSENTRY):
        """Completely remove an entry and its subtree from the FS"""
        raise NotImplementedError()

    def iter_descendants(self, entry: FSENTRY) -> Generator[FSENTRY, None, None]:
        if not isinstance(entry, Directory):
            return
        for fileid in entry.child_ids:
            child = self.get_entry_by_id(fileid)
            yield from self.iter_descendants(child)
            yield child


class DictTrackingFS(BaseFS, abc.ABC):
    def __init__(self):
        super().__init__()
        self.entries: Dict[int, FSENTRY] = {}
        self._fileid_base = 0
        self.root_dir = None

    def _gen_fileid(self):
        # keep generating until we find one that doesn't collide
        while True:
            # fileid 0 is invalid and 1 has a special meaning for us (fake dir above root)
            self._fileid_base = min(self._fileid_base + 1, 2) & ((2 ** 64) - 1)
            if self._fileid_base not in self.entries:
                return self._fileid_base

    def get_entry_by_id(self, fileid: int) -> Optional[FSENTRY]:
        return self.entries.get(fileid)

    def track_entry(self, entry: FSENTRY):
        assert entry.fileid is None
        entry.fileid = self._gen_fileid()
        self.entries[entry.fileid] = entry

        if isinstance(entry, Directory):
            if entry.root_dir:
                assert not self.root_dir
                self.root_dir = entry

    def remove_entry(self, entry: FSENTRY):
        if entry.parent_id is not None:
            parent: Directory = self.get_entry_by_id(entry.parent_id)
            parent.unlink_child(entry)
        for descendant in self.iter_descendants(entry):
            del self.entries[descendant.fileid]
        del self.entries[entry.fileid]

    def sanity_check(self):
        # Not multi-rooted
        entries = list(self.entries.values())
        assert sum(getattr(entry, 'root_dir', False) for entry in entries) == 1
        # Everything correctly rooted
        assert all(getattr(entry, 'root_dir', False) or entry.parent_id is not None for entry in entries)
        # Unique fileids
        assert len(set(e.fileid for e in entries)) == len(entries)
        for entry in entries:
            if entry.parent_id is not None:
                parent = self.get_entry_by_id(entry.parent_id)
                assert parent
                assert entry.fileid in parent.child_ids


class DecodedFileHandle(NamedTuple):
    fileid: int
    fsid: int


class FileHandleEncoder(abc.ABC):
    @abc.abstractmethod
    def encode(self, entry: Union[FSENTRY, DecodedFileHandle], nfs_v2=False) -> bytes:
        pass

    @abc.abstractmethod
    def decode(self, fh: bytes, nfs_v2=False) -> DecodedFileHandle:
        pass


class VerifyingFileHandleEncoder(FileHandleEncoder):
    """64bit FSID and FileID preceded by 128 or 256bit HMAC"""
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
        payload = struct.pack("!QQ", entry.fileid, entry.fsid)
        return self._calc_mac(payload, nfs_v2) + payload

    def decode(self, fh: bytes, nfs_v2=False) -> DecodedFileHandle:
        mac_len = self._mac_len(nfs_v2)
        expected_len = 16 + mac_len
        if len(fh) != expected_len:
            raise ValueError(f"FH {fh!r} is not {expected_len} bytes")
        mac, payload = fh[:mac_len], fh[mac_len:]
        if not secrets.compare_digest(mac, self._calc_mac(payload, nfs_v2)):
            raise ValueError(f"FH {fh!r} failed sig check")
        return DecodedFileHandle(*struct.unpack("!QQ", payload))


class FileSystemManager:
    def __init__(self, handle_encoder, filesystems):
        self.handle_encoder: FileHandleEncoder = handle_encoder
        self.filesystems: Dict[int, BaseFS] = {f.fsid: f for f in filesystems}

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
