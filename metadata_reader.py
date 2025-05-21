from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import os


def extract_metadata(file_path):
    metadata = {}
    try:
        audio = EasyID3(file_path)
        metadata["title"] = audio.get("title", [None])[0]
        metadata["artist"] = audio.get("artist", [None])[0]
        metadata["album"] = audio.get("album", [None])[0]
        metadata["genre"] = audio.get("genre", [None])[0]
        metadata["tracknumber"] = audio.get("tracknumber", [None])[0]
        metadata["discnumber"] = audio.get("discnumber", [None])[0]
        metadata["lyrics"] = audio.get("lyrics", [None])[0]
        metadata["comment"] = audio.get("comment", [None])[0]
        metadata["albumartist"] = audio.get("albumartist", [None])[0]
        metadata["composer"] = audio.get("composer", [None])[0]
        metadata["date"] = audio.get("date", [None])[
            0]  # Use 'date' tag for year

        # Get bitrate and duration using MP3
        audio_mp3 = MP3(file_path)
        metadata["bitrate"] = f"{int(audio_mp3.info.bitrate / 1000)} kbps" if audio_mp3.info.bitrate else None
        # Duration can be added if needed: metadata["duration"] = audio_mp3.info.length

    except Exception as e:
        print(f"Error reading metadata: {e}")

    # Add file path separately as it's not in ID3 tags
    # You might want to clean this path for display
    metadata["filepath"] = file_path

    return metadata
