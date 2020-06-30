import abc
import dataclasses
import datetime as dt
import enum
import hmac
import secrets
import struct
import weakref
from typing import *

FSENTRY = Union["File", "Directory", "SymLink", "BaseFSEntry", "FSEntryProxy"]


# Mostly a copy of NFS2's error codes that are supported in 3 as well.
class NFSError(enum.IntEnum):
    OK = 0
    ERR_PERM = 1
    ERR_NOENT = 2
    ERR_IO = 5
    ERR_NXIO = 6
    ERR_ACCES = 13
    ERR_EXIST = 17
    ERR_NODEV = 19
    ERR_NOTDIR = 20
    ERR_ISDIR = 21
    ERR_FBIG = 27
    ERR_NOSPC = 28
    ERR_ROFS = 30
    ERR_NAMETOOLONG = 63
    ERR_NOTEMPTY = 66
    ERR_DQUOT = 69
    ERR_STALE = 70
    ERR_WFLUSH = 99


class FSException(Exception):
    def __init__(self, nfs_error_code: int, message: str = ""):
        self.error_code = nfs_error_code
        self.message = message
        super().__init__(message)


# Portable-ish between NFS2/3/4
class FileType(enum.IntEnum):
    REG = 1
    DIR = 2
    BLK = 3
    CHR = 4
    LNK = 5
    SOCK = 6
    FIFO = 7


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
    rdev: Tuple[int, int]
    blocks: int
    atime: dt.datetime
    mtime: dt.datetime
    ctime: dt.datetime

    @property
    def fsid(self) -> int:
        return self.fs().fsid


class FSEntryProxy:
    """Quick way to make fake hardlinks with different names like `.` and `..`"""
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


class Symlink(BaseFSEntry, abc.ABC):
    contents: bytes
    type: Literal[FileType.LNK]


class Directory(BaseFSEntry, abc.ABC):
    child_ids: List[int]
    type: Literal[FileType.DIR]
    root_dir: bool = False


class NodeDirectory(Directory, abc.ABC):
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
    rdev: Tuple[int, int] = dataclasses.field(default=(0, 0))
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
class SimpleSymlink(Symlink, SimpleFSEntry):
    contents: bytearray = dataclasses.field(default_factory=bytearray)
    type: FileType = dataclasses.field(default=FileType.LNK, init=False)

    @property
    def size(self) -> int:
        return len(self.contents)


@dataclasses.dataclass
class SimpleDirectory(NodeDirectory, SimpleFSEntry):
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
    read_only: bool
    root_dir: Optional[Directory]

    def __init__(self):
        self.fsid = secrets.randbits(64)
        self.block_size = 4096

    def _verify_owned(self, entry: FSENTRY):
        if entry.fs() != self:
            raise FSException(NFSError.ERR_STALE, "Not owned by this FS")

    def _verify_writable(self):
        if self.read_only:
            raise FSException(NFSError.ERR_ROFS)

    @staticmethod
    def _is_valid_name(name: bytes):
        if any(x in name for x in (b"\x00", b"/")):
            return False
        if name in (b".", b".."):
            return False
        if len(name) > 250:
            return False
        return True

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

    def iter_descendants(self, entry: FSENTRY, inclusive=False, _depth=0) -> Generator[FSENTRY, None, None]:
        if _depth > 100:
            raise ValueError("Possible recursion in directory tree")
        if isinstance(entry, Directory):
            for fileid in entry.child_ids:
                child = self.get_entry_by_id(fileid)
                yield from self.iter_descendants(child, inclusive=False, _depth=_depth + 1)
                yield child
        if inclusive:
            yield entry

    def iter_ancestors(self, entry: FSENTRY, inclusive=False) -> Generator[FSENTRY, None, None]:
        seen_ids = set()
        if inclusive:
            yield entry
            seen_ids.add(entry.fileid)
        while entry.parent_id is not None:
            if entry.fileid in seen_ids:
                raise ValueError("Possible recursion in directory tree")
            entry = self.get_entry_by_id(entry.parent_id)
            seen_ids.add(entry.fileid)
            yield entry

    @abc.abstractmethod
    def lookup(self, directory: FSENTRY, name: bytes) -> Optional[FSENTRY]:
        raise NotImplementedError()

    @abc.abstractmethod
    def readdir(self, directory: FSENTRY) -> Sequence[FSENTRY]:
        raise NotImplementedError()

    @abc.abstractmethod
    def read(self, entry: FSENTRY, offset: int, count: int) -> bytes:
        raise NotImplementedError()

    @abc.abstractmethod
    def readlink(self, entry: FSENTRY) -> bytes:
        raise NotImplementedError()

    @abc.abstractmethod
    def write(self, entry: FSENTRY, offset: int, data: bytes) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    def setattrs(self, entry: FSENTRY, attrs: Dict[str, Any]):
        raise NotImplementedError()

    @abc.abstractmethod
    def rmdir(self, entry: Directory):
        raise NotImplementedError()

    @abc.abstractmethod
    def rm(self, entry: FSENTRY):
        raise NotImplementedError()

    @abc.abstractmethod
    def rename(self, source: FSENTRY, to_dir: Directory, new_name: bytes):
        raise NotImplementedError()

    @abc.abstractmethod
    def mkdir(self, dest: Directory, name: bytes, attrs: Dict[str, Any]) -> Directory:
        raise NotImplementedError()

    @abc.abstractmethod
    def symlink(self, dest: Directory, name: bytes, attrs: Dict[str, Any], val: bytes) -> Symlink:
        raise NotImplementedError()

    @abc.abstractmethod
    def create_file(self, dest: Directory, name: bytes, attrs: Dict[str, Any]) -> File:
        raise NotImplementedError()


class NodeTrackingFS(BaseFS, abc.ABC):
    NFS_V2_COMPAT: bool = True

    def __init__(self):
        super().__init__()
        self.entries: Dict[int, FSENTRY] = {}
        self._fileid_base = 0
        self.root_dir = None
        self._fileid_mask = (2 ** (32 if self.NFS_V2_COMPAT else 64)) - 1

    def _gen_fileid(self):
        # keep generating until we find one that doesn't collide
        while True:
            # fileid 0 is invalid and 1 has a special meaning for us (fake dir above root)
            self._fileid_base = max(self._fileid_base + 1, 2) & self._fileid_mask
            if self._fileid_base not in self.entries:
                return self._fileid_base

    def get_entry_by_id(self, fileid: int) -> Optional[FSENTRY]:
        return self.entries.get(fileid)

    def track_entry(self, entry: FSENTRY):
        self._verify_owned(entry)
        assert entry.fileid is None
        entry.fileid = self._gen_fileid()
        self.entries[entry.fileid] = entry

        if isinstance(entry, Directory):
            if entry.root_dir:
                assert not self.root_dir
                self.root_dir = entry

    def remove_entry(self, entry: FSENTRY):
        self._verify_owned(entry)
        if entry.parent_id is not None:
            parent: NodeDirectory = self.get_entry_by_id(entry.parent_id)
            parent.unlink_child(entry)
        for descendant in self.iter_descendants(entry, inclusive=True):
            del self.entries[descendant.fileid]

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


class SimpleFS(NodeTrackingFS):
    def _make_upper_dir_link(self, entry: FSENTRY) -> FSEntryProxy:
        if entry.parent_id is not None:
            parent: Directory = self.get_entry_by_id(entry.parent_id)
            return FSEntryProxy(
                base=parent,
                replacements={
                    "name": b"..",
                },
            )

        assert entry.root_dir

        # Need to make a fake entry for `..` since it's actually above
        # the root directory. Ironically none of the info other than the
        # name seems to be used in the dir listing.
        return FSEntryProxy(
            base=entry,
            replacements={
                # `1` will never be used by legitimate files and
                # is not actually tracked
                "fileid": 1,
                "name": b"..",
                "child_ids": [entry.fileid],
                "root_dir": False,
            }
        )

    @staticmethod
    def _hydrate_sattrs(attrs: Dict[str, Any], entry: Optional[FSENTRY] = None) -> Dict[str, Any]:
        new_attrs = {}
        for attr_name, attr_val in attrs.items():
            if attr_name == "size":
                if not entry:
                    if attrs["size"] != 0:
                        # TODO: is this actually the case?
                        raise FSException(NFSError.ERR_NXIO, "Can't set a size on a new file!")
                if entry.type not in (FileType.REG, FileType.LNK):
                    raise FSException(NFSError.ERR_IO, "Must be a file to change size!")
                # TODO: check new size within quota
            # This is a hint that the client wants to automatically fill in the server time
            elif "time" in attr_name and attr_val is None:
                attr_val = dt.datetime.utcnow()
            new_attrs[attr_name] = attr_val
        # Presumably this case is to allow the FS to choose the time rather than the NFS server,
        # but we're all mashed together.
        if "ctime" not in new_attrs:
            new_attrs["ctime"] = dt.datetime.utcnow()
        # Changing filesize means we have to update mtime, even if one wasn't specified
        if "size" in new_attrs and entry and entry.size != new_attrs["size"]:
            new_attrs["mtime"] = dt.datetime.utcnow()
        return new_attrs

    def readdir(self, directory: FSENTRY) -> Sequence[FSENTRY]:
        self._verify_owned(directory)
        if directory.type != FileType.DIR:
            raise FSException(NFSError.ERR_NOTDIR)
        files = [
            FSEntryProxy(directory, {"name": b"."}),
            self._make_upper_dir_link(directory),
            *[self.get_entry_by_id(fileid) for fileid in directory.child_ids]
        ]
        assert (all(files))
        return files

    def lookup(self, directory: FSENTRY, name: bytes) -> Optional[FSENTRY]:
        self._verify_owned(directory)
        if directory.type != FileType.DIR:
            raise FSException(NFSError.ERR_NOTDIR)
        for child in self.readdir(directory):
            if child.name == name:
                return child
        return None

    def read(self, entry: FSENTRY, offset: int, count: int) -> bytes:
        self._verify_owned(entry)
        if entry.type != FileType.REG:
            raise FSException(NFSError.ERR_IO)
        return entry.contents[offset:offset + count]

    def readlink(self, entry: FSENTRY) -> bytes:
        self._verify_owned(entry)
        if entry.type != FileType.LNK:
            raise FSException(NFSError.ERR_IO)
        return entry.contents

    def write(self, entry: FSENTRY, offset: int, data: bytes) -> int:
        self._verify_owned(entry)
        self._verify_writable()
        if entry.type != FileType.REG:
            raise FSException(NFSError.ERR_IO, "Not a regular file!")
        # Write chunks can be out of order, even when using TCP!
        # I've observed misordered writes in multi-fragment PSHs.
        size = entry.size
        if offset > size:
            # Filling gaps with NUL seems to align with POSIX fseek() semantics.
            # https://pubs.opengroup.org/onlinepubs/009695399/functions/fseek.html#tag_03_191_03
            entry.contents[size:offset] = b"\x00" * (offset - size)
        # TODO: update mtime
        entry.contents[offset:offset + len(data)] = data
        return len(data)

    def setattrs(self, entry: FSENTRY, attrs: Dict[str, Any]):
        self._verify_owned(entry)
        self._verify_writable()
        new_attrs = self._hydrate_sattrs(attrs, entry)
        new_size = new_attrs.pop("size", None)
        if new_size is not None:
            # TODO: changing file size must update mtime, how does that mesh with
            # client-specified mtime?
            if entry.type != FileType.REG:
                raise FSException(NFSError.Stat.ERR_PERM, "Can't set size on non-file")
            entry.contents = entry.contents[:new_size]

        for attr_name, attr_val in new_attrs.items():
            assert hasattr(entry, attr_name)
            setattr(entry, attr_name, attr_val)

    def rm(self, entry: FSENTRY):
        self._verify_owned(entry)
        self._verify_writable()
        if entry.type == FileType.DIR:
            raise FSException(NFSError.ERR_ISDIR)
        self.remove_entry(entry)

    def rmdir(self, entry: Directory):
        self._verify_owned(entry)
        self._verify_writable()
        if entry.type != FileType.DIR:
            raise FSException(NFSError.ERR_NOTDIR, "Not a directory")
        if entry.child_ids:
            raise FSException(NFSError.ERR_NOTEMPTY, "Not empty")
        if entry == self.root_dir:
            raise FSException(NFSError.ERR_NOTEMPTY, "Trying to remove root dir")
        self.remove_entry(entry)

    def rename(self, source: FSENTRY, to_dir: SimpleDirectory, new_name: bytes):
        self._verify_owned(source)
        self._verify_owned(to_dir)
        self._verify_writable()
        # TODO: needs to update ctime of file (due to hardlink changes) and
        # mtime of both src and dst dirs (since they normally own file name)
        if source == self.root_dir:
            raise FSException(NFSError.ERR_PERM, "Trying to move root!")
        if not self._is_valid_name(new_name):
            raise FSException(NFSError.ERR_PERM)
        # trying to move a directory inside itself????
        if source in self.iter_ancestors(to_dir):
            raise FSException(NFSError.ERR_ACCES, "Recursive parenting attempt")
        if self.lookup(to_dir, new_name):
            raise FSException(NFSError.ERR_EXIST)
        if source.parent_id != to_dir.fileid:
            self.get_entry_by_id(source.parent_id).unlink_child(source)
            to_dir.link_child(source)
        source.name = new_name

    def _base_create(self, dest: SimpleDirectory, name: bytes, attrs: Dict[str, Any], typ: Type) -> FSENTRY:
        self._verify_owned(dest)
        self._verify_writable()
        if self.lookup(dest, name):
            raise FSException(NFSError.ERR_EXIST)
        new_attrs = self._hydrate_sattrs(attrs, entry=None)
        new_entry = typ(
            fs=weakref.ref(self),
            name=name,
            **new_attrs,
        )
        dest.link_child(new_entry)
        return new_entry

    def mkdir(self, dest: SimpleDirectory, name: bytes, attrs: Dict[str, Any]) -> Directory:
        return self._base_create(dest, name, attrs, SimpleDirectory)

    def symlink(self, dest: SimpleDirectory, name: bytes, attrs: Dict[str, Any], val: bytes) -> Symlink:
        entry: SimpleSymlink = self._base_create(dest, name, attrs, SimpleSymlink)
        entry.contents = val
        return entry

    def create_file(self, dest: SimpleDirectory, name: bytes, attrs: Dict[str, Any]) -> File:
        return self._base_create(dest, name, attrs, SimpleFile)


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
            raise FSException(NFSError.ERR_IO, f"FH {fh!r} is not {expected_len} bytes")
        mac, payload = fh[:mac_len], fh[mac_len:]
        if not secrets.compare_digest(mac, self._calc_mac(payload, nfs_v2)):
            raise FSException(NFSError.ERR_IO, f"FH {fh!r} failed sig check")
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
        fs = self.filesystems.get(decoded.fsid)
        if not fs:
            return None
        if decoded.fileid != fs.root_dir.fileid:
            return None
        return fs

    def get_entry_by_fh(self, fh: bytes, nfs_v2=False) -> Optional[FSENTRY]:
        decoded = self.handle_encoder.decode(fh, nfs_v2)
        fs = self.filesystems.get(decoded.fsid)
        if not fs:
            return None
        return fs.get_entry_by_id(decoded.fileid)

    def entry_to_fh(self, entry: FSENTRY, nfs_v2=False):
        return self.handle_encoder.encode(entry, nfs_v2)
