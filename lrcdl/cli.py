import os
import click
from mutagen import MutagenError
from lrcdl.track import Track, SUPPORTED_EXTENSIONS
from lrcdl.options import Options
from lrcdl.exceptions import (
    UnsupportedExtension,
    LyricsAlreadyExists,
    LyricsNotAvailable,
    TrackNotFound,
    NotEnoughMetadata,
    RequestFailed
)

def error(message):
    click.echo(f"{click.style('Error:', fg='red')} {message}")

@click.command()
@click.option('--download-path', '-p', help="Optionally specify a custom download path to place the LRC file")
@click.option('--cache', '-c', help='An optional cache file to skip already-checked files on next run (used with --recursive only)')
@click.option('--recursive', '-r', is_flag=True, help='Recursively search for tracks and download lyrics for them')
@click.option('--include-plain', is_flag=True, help='Download plain, non-timed lyrics when timed lyrics are not available')
@click.option('--title', help='Override file metadata and specify a manual title')
@click.option('--album', help='Override file metadata and specify a manual album')
@click.option('--artist', help='Override file metadata and specify a manual artist')
@click.argument('path', type=click.Path())
def lrcdl(path, title, album, artist, cache, recursive, include_plain, download_path):
    options = Options(
        cache=cache,
        recursive=recursive,
        title=title,
        album=album,
        artist=artist,
        include_plain=include_plain,
        download_path=download_path
    )

    tracks = []
    skip = []

    if recursive:
        if cache and os.path.isdir(cache):
            error("Invalid cache, must be a file")
            return
        elif cache and os.path.exists(cache):
            with open(cache, 'r') as cachefile:
                skip = cachefile.read().split('\n')

        if not os.path.isdir(path):
            error("You must specify a directory when --recursive is on")
            return
        if title or album or artist:
            error("You cannot specify --title, --album or --artist when --recursive is on")
            return
        
        click.echo("Scanning directory...")
        for subdir, _, files in os.walk(path):
            for file in files:
                full_path = os.path.join(subdir, file)
                name, ext = os.path.splitext(full_path)
                if ext.lower() in SUPPORTED_EXTENSIONS and not os.path.exists(name + ".lrc") and full_path not in skip:
                    tracks.append(full_path)
    else:
        tracks.append(path)

    for i, track_path in enumerate(tracks):
        progress = f"({i+1}/{len(tracks)})"
        click.echo(f"Downloading lyrics for {click.style(track_path, bold=True)} {progress}")
        
        try:
            track = Track(track_path)
            track.download_lyrics(options)
            click.echo(f"Lyrics successfully downloaded for {click.style(track_path, bold=True)}")
        except IsADirectoryError:
            error("A directory was specified when a file path was expected")
        except FileNotFoundError:
            error("Specified path could not be found")
        except UnsupportedExtension:
            error(f"Invalid format, supported extensions are: {', '.join(SUPPORTED_EXTENSIONS)}")
        except LyricsAlreadyExists:
            click.echo(f"Lyrics already exist for {click.style(track_path, bold=True)}. Skipping")
        except NotEnoughMetadata as e:
            click.echo(f"Not enough metadata for {click.style(track_path, bold=True)}. Missing: ({', '.join(e.args[0])}). Specify them manually using --title, --album, and --artist")
        except (LyricsNotAvailable, TrackNotFound):
            skip.append(track_path)
            click.echo(f"Could not find suitable lyrics for {click.style(track_path, bold=True)}")
        except RequestFailed as e:
            click.echo(f"Request failed while fetching lyrics: {e.args[0]}")
        except MutagenError:
            error(f"Failed to open file {track_path}, possibly invalid data.")

    if cache:
        with open(cache, 'w') as cachefile:
            cachefile.write('\n'.join(skip))