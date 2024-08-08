from mutagen.flac import FLAC
from mutagen.mp3 import MP3

def get_metadata(file):
    metadata = {}
    
    if isinstance(file, MP3):
        metadata["title"] = file.get("TIT2")[0] if "TIT2" in file else None
        metadata["album"] = file.get("TALB")[0] if "TALB" in file else None
        metadata["artist"] = file.get("TPE1")[0] if "TPE1" in file else None
    elif isinstance(file, FLAC):
        metadata["title"] = file.get("title")[0] if "title" in file else None
        metadata["album"] = file.get("album")[0] if "album" in file else None
        metadata["artist"] = file.get("artist")[0] if "artist" in file else None

    return metadata