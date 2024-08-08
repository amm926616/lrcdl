import requests
from importlib.metadata import version
from lrcdl.exceptions import TrackNotFound

DEFAULT_HOST = "https://lrclib.net"
DEFAULT_HEADERS = {
    "User-Agent": f"lrcdl v{version('lrcdl')} (https://github.com/viown/lrcdl)"
}

def get_lyrics(track_name, artist_name, album_name, duration):
    params = {
        "track_name": track_name.strip(),
        "artist_name": artist_name.strip(),
        "album_name": album_name.strip(),
        "duration": duration
    }
    r = requests.get(f"{DEFAULT_HOST}/api/get", params=params, headers=DEFAULT_HEADERS)

    if r.ok:
        return r.json()
    elif r.status_code == 404:
        raise TrackNotFound()