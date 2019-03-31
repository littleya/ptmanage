class Torrent(object):
    def __init__(self, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs.get(k))

    @classmethod
    def from_dict(cls, **kwargs):
        for k in kwargs:
            setattr(cls, k, kwargs.get(k))
        return cls
