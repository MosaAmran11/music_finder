from typing import Any
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from music.utils.datetime import format_time
import datetime


class AudioTags:
    def __init__(self, filepath: str = None):
        self.filepath = filepath
        self.title = None
        self.artist = None
        self.album = None
        self.genre = None
        self.tracknumber = None
        self.discnumber = None
        self.albumartist = None
        self.composer = None
        self._date = None
        self.bitrate = None
        self.duration = None
        self._extract_metadata()

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value: datetime.datetime | str | Any):
        if isinstance(value, datetime.datetime):
            self._date = value.strftime('%Y')
        elif value is not None:
            self._date = str(value)[:4]
        else:
            self._date = ''

    @property
    def str_bitrate(self):
        return f"{self.bitrate} kbps"

    @property
    def str_duration(self):
        return format_time(self.duration)

    def _extract_metadata(self):
        if not self.filepath:
            return
        try:
            audio = EasyID3(self.filepath)
            self.title = audio.get("title", [None])[0]
            self.artist = audio.get("artist", [None])[0]
            self.album = audio.get("album", [None])[0]
            self.genre = audio.get("genre", [None])[0]
            self.tracknumber = audio.get("tracknumber", [None])[0]
            self.discnumber = audio.get("discnumber", [None])[0]
            self.albumartist = audio.get("albumartist", [None])[0]
            self.composer = audio.get("composer", [None])[0]
            self.date = audio.get("date", [None])[0]  # Use 'date' tag for year

            # Get bitrate and duration using MP3
            audio_mp3 = MP3(self.filepath)
            self.bitrate = int(
                audio_mp3.info.bitrate / 1000) if audio_mp3.info.bitrate else 0
            self.duration = audio_mp3.info.length or 0

        except Exception as e:
            print(f"Error reading metadata: {e}")

    def parse(self, data: dict):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                print(
                    f"Warning: {key} is not a valid attribute of AudioTags. Skipping.")

    def itunes_parse(self, data: dict):
        """
        Parse metadata from a dictionary, typically from an iTunes API response.
        """
        self.title = data.get("trackName", None)
        self.artist = data.get("artistName", None)
        self.albumartist = data.get("artistName", None)
        self.album = data.get("collectionName", None)
        self.genre = data.get("primaryGenreName", None)
        self.tracknumber = data.get("trackNumber", None)
        self.discnumber = data.get("discNumber", None)
        self.date = datetime.datetime.fromisoformat(
            data.get("releaseDate").replace("Z", "+00:00"))

    def to_dict(self):
        """
        Convert the metadata attributes to a dictionary.
        """
        # Handle date serialization properly
        date_value = self.date
        if isinstance(date_value, (datetime.date, datetime.datetime)):
            date_value = date_value.isoformat()[:4]
        elif date_value is not None:
            date_value = str(date_value)

        return {
            "filepath": self.filepath,
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "genre": self.genre,
            "tracknumber": self.tracknumber,
            "discnumber": self.discnumber,
            "albumartist": self.albumartist,
            "composer": self.composer,
            "date": date_value,
            "bitrate": self.bitrate,
            "str_bitrate": self.str_bitrate,
            "duration": self.duration,
            "str_duration": self.str_duration,
        }

    def get(self, key, default=None):
        """
        Get the value of a metadata attribute by key.
        If the key does not exist, return the default value.
        """
        return getattr(self, key, default)

    def __getitem__(self, item):
        return getattr(self, item, None)

    def __getstate__(self):
        return self.to_dict()

    def __json__(self):
        return self.to_dict()

    def __repr__(self):
        return f"Audio({self.to_dict()})"

    def __str__(self):
        return f"Audio: {self.to_dict()}"


class ExtendedAudioTags(AudioTags):
    def __init__(self):
        super().__init__()
        self.thumbnailUrl = None

    def itunes_parse(self, data: dict):
        """
        Parse metadata from a dictionary, typically from an iTunes API response.
        """
        super().itunes_parse(data)
        self.thumbnailUrl = data.get("artworkUrl1000",
                                     data.get("artworkUrl100", '')
                                     .replace("100x100", "1000x1000"))

    def to_dict(self):
        d = super().to_dict()
        d["thumbnailUrl"] = self.thumbnailUrl
        return d

    def __getstate__(self):
        return self.to_dict()

    def __json__(self):
        return self.to_dict()
