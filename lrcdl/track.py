import os
import mutagen
from lrcdl import provider
from lrcdl.utils import get_metadata
from lrcdl.exceptions import (
    LyricsAlreadyExists,
    UnsupportedExtension,
    LyricsNotAvailable,
    NotEnoughMetadata
)

SUPPORTED_EXTENSIONS = [".mp3", ".flac", ".m4a", ".ogg"]  # Added .ogg

class Track:
    def __init__(self, path):
        self.path = path
        self.split_path = os.path.splitext(self.path)

        if not os.path.exists(self.path):
            raise FileNotFoundError()
        if not os.path.isfile(self.path):
            raise IsADirectoryError()
        if self.split_path[1].lower() not in SUPPORTED_EXTENSIONS:
            raise UnsupportedExtension()
        
        self.file = mutagen.File(self.path)

    def download_lyrics(self, options):
        metadata = get_metadata(self.file)
        title = options.title or metadata["title"]
        album = options.album or metadata["album"]
        artist = options.artist or metadata["artist"]
        download_path = options.download_path or self.split_path[0] + ".lrc"

        if os.path.exists(download_path):
            raise LyricsAlreadyExists()
        if not (title and album and artist):
            missing = []

            if not title:
                missing.append("title")
            if not album:
                missing.append("album")
            if not artist:
                missing.append("artist")

            raise NotEnoughMetadata(missing)

        # Ensure duration is correctly fetched
        duration = round(self.file.info.length)  # This should work for Ogg too

        lyrics = provider.get_lyrics(title, artist, album, duration)

        lyrics_text = None

        if lyrics.get("syncedLyrics"):
            lyrics_text = lyrics["syncedLyrics"]
        elif lyrics.get("plainLyrics") and options.include_plain:
            lyrics_text = lyrics["plainLyrics"]
        else:
            raise LyricsNotAvailable()
        
        with open(download_path, "w") as f:
            f.write(lyrics_text)
