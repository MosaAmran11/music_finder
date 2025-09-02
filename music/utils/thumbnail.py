import os

import requests
from PIL import Image
from mutagen.id3 import ID3, APIC, error
from mutagen.mp3 import MP3

from music.utils.files import create_temp_file
from music.utils.logger import get_logger


def download_thumbnail(url: str) -> str:
    log = get_logger()
    log.info(f"Downloading thumbnail from {url}")

    thumbnail_data = requests.get(url).content
    thumbnail_path = create_temp_file(thumbnail_data, suffix='.png')

    log.info(f"Thumbnail downloaded")
    return thumbnail_path


def embed_thumbnail(audio_filename: str, thumbnail_path: str):
    print("Embedding thumbnail into audio file...")

    # Ensure thumbnail is JPEG
    jpeg_thumb_path = thumbnail_path
    try:
        with Image.open(thumbnail_path) as img:
            if img.format != 'JPEG':
                jpeg_thumb_path = thumbnail_path.rsplit('.', 1)[0] + '.jpg'
                img.convert('RGB').save(jpeg_thumb_path, 'JPEG')
    except Exception:
        jpeg_thumb_path = thumbnail_path  # fallback

    # Embed the thumbnail image into the audio file (replace old cover art if present)
    audio = MP3(audio_filename, ID3=ID3)
    if audio.tags is None:
        audio.add_tags()
    else:
        # Remove any existing embedded images
        audio.tags.delall('APIC')

    audio.tags.add(APIC(
        encoding=3,  # 3 = utf-8
        mime='image/jpeg',  # MIME type of the image
        type=3,  # 3 = cover image
        desc='Cover',
        data=open(jpeg_thumb_path, 'rb').read()
    ))
    audio.save(v2_version=3)

    # Clean up the downloaded/converted thumbnail image(s)
    if jpeg_thumb_path != thumbnail_path and os.path.exists(jpeg_thumb_path):
        os.remove(jpeg_thumb_path)
    if os.path.exists(thumbnail_path):
        os.remove(thumbnail_path)
