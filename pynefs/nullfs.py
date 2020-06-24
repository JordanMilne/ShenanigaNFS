import secrets
import weakref

from pynefs.fs import BaseFS, SimpleDirectory, SimpleFile


class NullFS(BaseFS):
    def __init__(self, root_path):
        super().__init__()
        self.num_blocks = 1
        self.free_blocks = 0
        self.avail_blocks = 0
        self.root_path = root_path

        root_dir = SimpleDirectory(
            fs=weakref.ref(self),
            mode=0o0755,
            fileid=secrets.randbits(32),
            name=b"",
            child_ids=[],
            root_dir=True,
            parent_id=None,
        )

        self.entries = [
            root_dir,
        ]

        root_dir.add_child(SimpleFile(
            fs=weakref.ref(self),
            # Will be filled in later
            parent_id=None,
            fileid=secrets.randbits(32),
            name=b"testfile.txt",
            mode=0o444,
            contents=b"test\n",
        ))
