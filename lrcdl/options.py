class Options:
    def __init__(self,
                 cache=None,
                 recursive=False,
                 include_plain=False,
                 title=None,
                 album=None,
                 artist=None,
                 download_path=None):
        self.cache = cache
        self.recursive = recursive
        self.include_plain = include_plain
        self.title = title
        self.album = album
        self.artist = artist
        self.download_path = download_path