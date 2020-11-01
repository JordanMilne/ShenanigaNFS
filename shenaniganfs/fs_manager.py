import datetime as dt
from typing import *

from shenaniganfs.fs import BaseFS, FileHandleEncoder, FSENTRY
from shenaniganfs.server import CallContext


def create_fs(fs_type: Type[BaseFS], call_ctx: CallContext, **kwargs):
    new_fs = fs_type(**kwargs)
    new_fs.owner_addr = call_ctx.transport.client_addr[0]
    return new_fs


class FileSystemManager:
    def __init__(self, handle_encoder, factories: Dict[bytes, Callable]):
        self.handle_encoder: FileHandleEncoder = handle_encoder
        self.filesystems: Dict[int, BaseFS] = {}
        self.fs_factories: Dict[bytes, Callable] = factories

    def mount_fs_by_root(self, root_path, call_ctx: CallContext) -> BaseFS:
        new_fs: BaseFS = self.fs_factories[root_path](call_ctx)
        if new_fs.fsid in self.filesystems:
            raise ValueError("Unexpected FSID collision!")
        self.filesystems[new_fs.fsid] = new_fs
        return new_fs

    def get_fs_by_fh(self, fh: bytes, nfs_v2=False) -> Optional[BaseFS]:
        decoded = self.handle_encoder.decode(fh, nfs_v2)
        fs = self.filesystems.get(decoded.fsid)
        if not fs:
            return None
        if decoded.fileid != fs.root_dir.fileid:
            return None
        fs.last_referenced = dt.datetime.utcnow()
        return fs

    def get_entry_by_fh(self, fh: bytes, nfs_v2=False) -> Optional[FSENTRY]:
        decoded = self.handle_encoder.decode(fh, nfs_v2)
        fs = self.filesystems.get(decoded.fsid)
        if not fs:
            return None
        fs.last_referenced = dt.datetime.utcnow()
        return fs.get_entry_by_id(decoded.fileid)

    def entry_to_fh(self, entry: FSENTRY, nfs_v2=False):
        return self.handle_encoder.encode(entry, nfs_v2)


class EvictingFileSystemManager(FileSystemManager):
    """
    Filesystem manager that automatically evicts unused filesystems

    Implements basic DoS prevention by having a separate per-IP limit alongside
    a larger global limit so it's more difficult to force others' mounts to be
    evicted.
    """

    @staticmethod
    def _get_oldest_fs(filesystems: Iterable[BaseFS]) -> BaseFS:
        return sorted(filesystems, key=lambda x: x.last_referenced)[0]

    def __init__(self, handle_encoder, factories, total_allowed=100, client_allowed=2):
        super().__init__(handle_encoder, factories)
        self.client_allowed = client_allowed
        self.total_allowed = total_allowed

    def mount_fs_by_root(self, root_path, call_ctx: CallContext) -> BaseFS:
        new_fs = super().mount_fs_by_root(root_path, call_ctx)
        owned = [fs for fs in self.filesystems.values() if fs.owner_addr == new_fs.owner_addr]
        if len(owned) > self.client_allowed:
            old_fs = self._get_oldest_fs(owned)
            print(f"Evicting due to client limit {old_fs!r}")
            self.filesystems.pop(old_fs.fsid)
        if len(self.filesystems) > self.total_allowed:
            old_fs = self._get_oldest_fs(self.filesystems.values())
            print(f"Evicting due to global limit {old_fs!r}")
            self.filesystems.pop(old_fs.fsid)
        return new_fs
