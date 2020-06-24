import datetime as dt
import secrets
import weakref

from pynefs.fs import BaseFS, Directory, File


class NullFS(BaseFS):
    def __init__(self, root_path):
        super().__init__()
        self.fsid = secrets.token_bytes(8)
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
            fileid=secrets.randbits(32),
            atime=dt.datetime.utcnow(),
            mtime=dt.datetime.utcnow(),
            ctime=dt.datetime.utcnow(),
            name=b"",
            child_ids=[],
            root_dir=True,
            parent_id=None,
        )

        self.entries = [
            root_dir,
        ]

        root_dir.add_child(File(
            fs=weakref.ref(self),
            # Will be filled in later
            parent_id=None,
            fileid=secrets.randbits(32),
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
