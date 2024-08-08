import click
import os
import sys
from lrcdl.track import Track, SUPPORTED_EXTENSIONS
from lrcdl.exceptions import (
    UnsupportedExtension,
    LyricsAlreadyExists,
    LyricsNotAvailable,
    TrackNotFound,
    NotEnoughMetadata
)

def error(message, exit=False):
    click.echo(f"{click.style('Error:', fg='red')} {message}")
    if exit:
        sys.exit()

@click.command()
@click.option('--title')
@click.option('--album')
@click.option('--artist')
@click.option('--cache')
@click.option('--recursive', is_flag=True)
@click.option('--include-plain', is_flag=True)
@click.argument('path', type=click.Path())
def lrcdl(path, title, album, artist, cache, recursive, include_plain):
    tracks = []
    skip = []

    if recursive:
        
        if cache and os.path.isdir(cache):
            error("Invalid cache, must be a file", exit=True)
        elif cache and os.path.exists(cache):
            with open(cache, 'r') as cachefile:
                skip = cachefile.read().split('\n')

        if not os.path.isdir(path):
            error("You must specify a directory when --recursive is on", exit=True)
        if title or album or artist:
            error("You cannot specify --title, --album or --artist when --recursive is on", exit=True)
        
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
            track = Track(track_path, title, album, artist)
            track.download_lyrics(include_plain)
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

    if cache:
        with open(cache, 'w') as cachefile:
            cachefile.write('\n'.join(skip))