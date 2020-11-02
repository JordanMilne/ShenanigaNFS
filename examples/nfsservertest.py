import asyncio
import os

from shenaniganfs.nfs_utils import serve_nfs
from shenaniganfs.fs import SimpleFS, SimpleDirectory, SimpleFile, VerifyingFileHandleEncoder
from shenaniganfs.fs_manager import EvictingFileSystemManager, create_fs


class ExampleFS(SimpleFS):
    def __init__(self, read_only=True, size_quota=None, entries_quota=None):
        super().__init__(size_quota=size_quota, entries_quota=entries_quota)
        self.read_only = read_only
        self.num_blocks = 1
        self.free_blocks = 0
        self.avail_blocks = 0

        self.track_entry(SimpleDirectory(
            mode=0o0755,
            name=b"",
            root_dir=True,
        ))

        self.root_dir.link_child(SimpleFile(
            name=b"testfile.txt",
            mode=0o444 if read_only else 0o777,
            contents=bytearray(b"test\n"),
        ))


async def main():
    fs_manager = EvictingFileSystemManager(
        VerifyingFileHandleEncoder(os.urandom(32)),
        factories={
            b"/tmp/nfs2": lambda call_ctx: create_fs(
                ExampleFS,
                call_ctx,
                read_only=False,
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
