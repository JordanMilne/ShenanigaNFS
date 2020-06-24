import datetime as dt
import math
import secrets
import weakref
import zipfile
from zlib import crc32

from pynefs.fs import DictTrackingFS, Directory, SimpleDirectory, SimpleFile


class ZipFS(DictTrackingFS):
    def __init__(self, root_path, zip_path):
        super().__init__()
        self.num_blocks = 1
        self.free_blocks = 0
        self.avail_blocks = 0
        self.root_path = root_path

        self.track_entry(SimpleDirectory(
            fs=weakref.ref(self),
            mode=0o0555,
            name=b"",
            root_dir=True,
        ))

        with zipfile.ZipFile(zip_path) as f:
            for path in zipfile.Path(f).iterdir():
                self._add_path(f, parent=self.root_dir, path=path)
        self.sanity_check()

    def _add_path(self, zip_file: zipfile.ZipFile, parent: Directory, path: zipfile.Path):
        info: zipfile.ZipInfo = zip_file.getinfo(path.at)

        common_kwargs = dict(
            fs=parent.fs,
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
                **common_kwargs,
            )
        else:
            entry = SimpleFile(
                contents=path.read_bytes(),
                **common_kwargs
            )

        parent.add_child(entry)

        if info.is_dir():
            for child_path in path.iterdir():
                self._add_path(zip_file, parent=entry, path=child_path)
