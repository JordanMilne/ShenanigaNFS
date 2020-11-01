import weakref

from shenaniganfs.fs import SimpleFS, SimpleDirectory, SimpleFile


class NullFS(SimpleFS):
    def __init__(self, read_only=True):
        super().__init__()
        self.read_only = read_only
        self.num_blocks = 1
        self.free_blocks = 0
        self.avail_blocks = 0

        self.track_entry(SimpleDirectory(
            fs=weakref.ref(self),
            mode=0o0755,
            name=b"",
            root_dir=True,
        ))

        self.root_dir.link_child(SimpleFile(
            fs=weakref.ref(self),
            name=b"testfile.txt",
            mode=0o444 if read_only else 0o777,
            contents=bytearray(b"test\n"),
        ))
