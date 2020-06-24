import weakref

from pynefs.fs import DictTrackingFS, SimpleDirectory, SimpleFile


class NullFS(DictTrackingFS):
    def __init__(self, root_path):
        super().__init__()
        self.num_blocks = 1
        self.free_blocks = 0
        self.avail_blocks = 0
        self.root_path = root_path

        self.track_entry(SimpleDirectory(
            fs=weakref.ref(self),
            mode=0o0755,
            name=b"",
            root_dir=True,
        ))

        self.root_dir.link_child(SimpleFile(
            fs=weakref.ref(self),
            name=b"testfile.txt",
            mode=0o444,
            contents=bytearray(b"test\n"),
        ))
