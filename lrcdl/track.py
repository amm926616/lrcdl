import mutagen
import os
from lrcdl import api
from lrcdl.utils import get_metadata
from lrcdl.exceptions import (
    LyricsAlreadyExists,
    UnsupportedExtension,
    LyricsNotAvailable,
    NotEnoughMetadata
)

SUPPORTED_EXTENSIONS = [".mp3", ".flac", ".m4a"]

class Track:
    def __init__(self, path, title=None, album=None, artist=None):
        self.path = path
        self.split_path = os.path.splitext(self.path)

        if not os.path.exists(self.path):
            raise FileNotFoundError()
        if not os.path.isfile(self.path):
            raise IsADirectoryError()
        if self.split_path[1].lower() not in SUPPORTED_EXTENSIONS:
            raise UnsupportedExtension()
        
        self.file = mutagen.File(self.path)
        
        metadata = get_metadata(self.file)
        self.title = title or metadata["title"]
        self.album = album or metadata["album"]
        self.artist = artist or metadata["artist"]

    def download_lyrics(self, include_plain=False):
        if os.path.exists(self.split_path[0] + ".lrc"):
            raise LyricsAlreadyExists()
        if not (self.title and self.album and self.artist):
            missing = []

            if not self.title:
                missing.append("title")
            if not self.album:
                missing.append("album")
            if not self.artist:
                missing.append("artist")

            raise NotEnoughMetadata(missing)

        lyrics = api.get_lyrics(self.title, self.artist, self.album, round(self.file.info.length))

        lyrics_text = None

        if lyrics["syncedLyrics"]:
            lyrics_text = lyrics["syncedLyrics"]
        elif lyrics["plainLyrics"] and include_plain:
            lyrics_text = lyrics["plainLyrics"]
        else:
            raise LyricsNotAvailable()
        
        with open(self.split_path[0] + ".lrc", "w") as f:
            f.write(lyrics_text)