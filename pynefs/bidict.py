from collections import UserDict


class BiDict(UserDict):
    def __init__(self, *args, **kwargs):
        self.backward = {}
        super().__init__(*args, **kwargs)

    def __delitem__(self, key):
        del self.backward[self.data[key]]

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.backward[value] = key

    @property
    def forward(self):
        return self.data
