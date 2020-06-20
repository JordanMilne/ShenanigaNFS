import datetime as dt
import math
import secrets
import weakref
import zipfile
from zlib import crc32

from pynefs.fs import BaseFS, Directory, File


class ZipFS(BaseFS):
    def __init__(self, root_path, zip_path):
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
            mode=0o0555,
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

        with zipfile.ZipFile(zip_path) as f:
            for path in zipfile.Path(f).iterdir():
                self._add_path(f, parent=root_dir, path=path)
        self.sanity_check()

    def _add_path(self, zip_file: zipfile.ZipFile, parent: Directory, path: zipfile.Path):
        info: zipfile.ZipInfo = zip_file.getinfo(path.at)

        common_kwargs = dict(
            fs=parent.fs,
            fh=secrets.token_bytes(32),
            # Will get filled in when added
            parent_fh=None,
            # numeric ID based on the full path
            fileid=crc32(info.filename.encode("utf8")),
            # specifically the file portion
            name=path.name.encode("utf8"),
            # Not writeable!
            mode=(info.external_attr >> 16) & ~0o222,
            uid=1000,
            gid=1000,
            size=info.file_size,
            rdev=0,
            blocks=math.ceil(info.file_size / self.block_size),
            atime=dt.datetime.utcnow(),
            mtime=dt.datetime(*info.date_time),
            ctime=dt.datetime(*info.date_time),
        )

        if info.is_dir():
            entry = Directory(
                child_fhs=[],
                root_dir=False,
                # we always have the `.` hard link, so at least 2
                nlink=2,
                **common_kwargs,
            )
        else:
            entry = File(
                contents=path.read_bytes(),
                nlink=1,
                **common_kwargs
            )

        parent.add_child(entry)

        if info.is_dir():
            for child_path in path.iterdir():
                self._add_path(zip_file, parent=entry, path=child_path)
