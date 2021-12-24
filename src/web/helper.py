from collections import abc


class Container(abc.Mapping):
    def __init__(self, **kwargs):
        self._names = {n for n in dir(self) if not n.startswith("_")}
        for name, value in kwargs.items():
            setattr(self, name, value)

    def __getitem__(self, name):
        return getattr(self, name)

    def __iter__(self):
        return iter(self._names)

    def __len__(self):
        return len(self._names)

    def __setattr__(self, name, value):
        if not name.startswith("_"):
            self._names.add(name)
        object.__setattr__(self, name, value)

    def update(self, data):
        for name, value in data.items():
            setattr(self, name, value)
