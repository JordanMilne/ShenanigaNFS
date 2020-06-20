import datetime as dt
import secrets
import weakref
from zlib import crc32

from pynefs.fs import BaseFS, Directory, File


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

        root_dir = Directory(
            fs=weakref.ref(self),
            mode=0o0755,
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

        self.entries = [
            root_dir,
        ]

        root_dir.add_child(File(
            fs=weakref.ref(self),
            fh=secrets.token_bytes(32),
            # Will be filled in later
            parent_fh=None,
            fileid=crc32(self.fh),
            name=b"testfile.txt",
            mode=0o555,
            nlink=0,
            uid=1000,
            gid=1000,
            size=4,
            rdev=0,
            blocks=1,
            atime=dt.datetime.utcnow(),
            mtime=dt.datetime.utcnow(),
            ctime=dt.datetime.utcnow(),
            contents=b"test",
        ))
