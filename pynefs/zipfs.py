import datetime as dt
import math
import secrets
import weakref
import zipfile
from zlib import crc32

from pynefs.fs import BaseFS, Directory, SimpleDirectory, SimpleFile


class ZipFS(BaseFS):
    def __init__(self, root_path, zip_path):
        super().__init__()
        self.num_blocks = 1
        self.free_blocks = 0
        self.avail_blocks = 0
        self.root_path = root_path

        root_dir = SimpleDirectory(
            fs=weakref.ref(self),
            mode=0o0555,
            fileid=secrets.randbits(32),
            name=b"",
            child_ids=[],
            root_dir=True,
            parent_id=None,
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
            # Will get filled in when added
            parent_id=None,
            # numeric ID based on the full path
            fileid=crc32(info.filename.encode("utf8")),
            # specifically the file portion
            name=path.name.encode("utf8"),
            # Not writeable!
            mode=(info.external_attr >> 16) & ~0o222,
            # size=info.file_size,
            blocks=math.ceil(info.file_size / self.block_size),
            mtime=dt.datetime(*info.date_time),
            ctime=dt.datetime(*info.date_time),
        )

        if info.is_dir():
            entry = SimpleDirectory(
                child_ids=[],
                root_dir=False,
                # we always have the `.` hard link, so at least 2
                nlink=2,
                **common_kwargs,
            )
        else:
            entry = SimpleFile(
                contents=path.read_bytes(),
                nlink=1,
                **common_kwargs
            )

        parent.add_child(entry)

        if info.is_dir():
            for child_path in path.iterdir():
                self._add_path(zip_file, parent=entry, path=child_path)
