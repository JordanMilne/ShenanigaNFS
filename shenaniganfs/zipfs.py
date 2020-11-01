import datetime as dt
import math
import weakref
import zipfile

from shenaniganfs.fs import SimpleFS, SimpleDirectory, SimpleFile, NodeDirectory


def propagate_owner_perms(mode):
    owner_perms = (mode & 0o700)
    return mode | (owner_perms >> 3) | (owner_perms >> 6)


class ZipFS(SimpleFS):
    def __init__(self, zip_path, read_only=True, size_quota=None, entries_quota=None):
        super().__init__(size_quota=size_quota, entries_quota=entries_quota)
        self.read_only = read_only
        self.num_blocks = 1
        self.free_blocks = 0
        self.avail_blocks = 0

        self.track_entry(SimpleDirectory(
            fs=weakref.ref(self),
            mode=0o0555 if self.read_only else 0o0777,
            name=b"",
            root_dir=True,
        ))

        with zipfile.ZipFile(zip_path) as f:
            for path in zipfile.Path(f).iterdir():
                self._add_path(f, parent=self.root_dir, path=path)
        self.sanity_check()

    def _add_path(self, zip_file: zipfile.ZipFile, parent: NodeDirectory, path: zipfile.Path):
        info: zipfile.ZipInfo = zip_file.getinfo(path.at)

        common_kwargs = dict(
            fs=parent.fs,
            # specifically the file portion
            name=path.name.encode("utf8"),
            # Not writeable!
            mode=propagate_owner_perms((info.external_attr >> 16) & (~0o222 if self.read_only else ~0)),
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
                contents=bytearray(path.read_bytes()),
                **common_kwargs
            )

        parent.link_child(entry)

        if info.is_dir():
            for child_path in path.iterdir():
                self._add_path(zip_file, parent=entry, path=child_path)
