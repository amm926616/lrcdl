class Options:
    def __init__(self,
                 cache=None,
                 recursive=False,
                 include_plain=False,
                 title=None,
                 album=None,
                 artist=None):
        self.cache = cache
        self.recursive = recursive
        self.include_plain = include_plain
        self.title = title
        self.album = album
        self.artist = artist