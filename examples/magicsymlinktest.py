"""
NFS service demoing symlink ToCToU attacks

Magically creates a symlink whenever lookup() is called with a
non-existent filename. "_"s in the filename are replaced with "/"s
when determining where the symlink points. It will flip between
a "trusted" value and the arbitrary value every time readlink() is
called.

for ex:

$ ls -a mnt
.  ..
$ readlink mnt/_etc_passwd
/tmp/foobar
$ readlink mnt/_etc_passwd
/etc/passwd
$ readlink mnt/_etc_passwd
/tmp/foobar
$ readlink mnt/.._foo_bar
/tmp/foobar
$ readlink mnt/.._foo_bar
../foo/bar
$ ls -a mnt
.  ..  _etc_passwd  .._foo_bar
"""

import asyncio
import dataclasses
import os

from typing import *

from shenaniganfs.fs import (
    FileType,
    FSENTRY,
    SimpleFS,
    SimpleDirectory,
    SimpleFSEntry,
    Symlink,
    utcnow,
    VerifyingFileHandleEncoder,
)
from shenaniganfs.fs_manager import EvictingFileSystemManager, create_fs
from shenaniganfs.nfs_utils import serve_nfs


@dataclasses.dataclass
class MagicSymLink(SimpleFSEntry, Symlink):
    read_count: int = dataclasses.field(default=0)
    symlink_options: List[bytes] = dataclasses.field(default_factory=list)
    type: FileType = dataclasses.field(default=FileType.LNK, init=False)

    @property
    def contents(self) -> bytearray:
        return bytearray(self.symlink_options[self.read_count % len(self.symlink_options)])

    @property
    def size(self) -> int:
        return len(self.contents)


class MagicSwitchingSymlinkFS(SimpleFS):
    def __init__(self, orig_link: bytes, size_quota=None, entries_quota=None):
        super().__init__(size_quota=size_quota, entries_quota=entries_quota)
        self.read_only = False
        self.trusted_target = orig_link
        self.num_blocks = 1
        self.free_blocks = 0
        self.avail_blocks = 0

        self.track_entry(SimpleDirectory(
            mode=0o0777,
            name=b"",
            root_dir=True,
        ))

    def lookup(self, directory: FSENTRY, name: bytes) -> Optional[FSENTRY]:
        entry = super().lookup(directory, name)
        if not entry:
            attrs = dict(
                mode=0o0777,
                symlink_options=[self.trusted_target, name.replace(b"_", b"/")],
            )
            self._verify_size_quota(len(name) * 2)
            entry = self._base_create(directory, name, attrs, MagicSymLink)
        return entry

    def readlink(self, entry: FSENTRY) -> bytes:
        val = super().readlink(entry)
        if isinstance(entry, MagicSymLink):
            entry.read_count += 1
            entry.ctime = utcnow()
            entry.mtime = utcnow()
        return val


async def main():
    fs_manager = EvictingFileSystemManager(
        VerifyingFileHandleEncoder(os.urandom(32)),
        factories={
            b"/symlinkfs": lambda call_ctx: create_fs(
                MagicSwitchingSymlinkFS,
                call_ctx,
                trusted_target=b"/tmp/foobar",
                # Only 100 entries total allowed in the FS
                entries_quota=100,
                # names + contents not allowed to exceed this in bytes
                size_quota=100 * 1024
            ),
        },
    )
    await serve_nfs(fs_manager, use_internal_rpcbind=True)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
