from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4

metadata_mapping = {
    MP3: {
        "title": "TIT2",
        "album": "TALB",
        "artist": "TPE1"
    },
    FLAC: {
        "title": "title",
        "album": "album",
        "artist": "artist"
    },
    MP4: {
        "title": "©nam",
        "album": "©alb",
        "artist": "©ART"
    }
}

def get_metadata(file):
    metadata = {}
    
    for mapping in metadata_mapping:
        if isinstance(file, mapping):
            for item, val in metadata_mapping[mapping].items():
                metadata[item] = dict(file)[val][0] if val in file else None

    return metadata