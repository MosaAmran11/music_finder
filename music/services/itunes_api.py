import requests

from music.services.http_service import HttpService
from music.utils.logger import get_logger

log = get_logger()
service = HttpService(base_url="https://itunes.apple.com")


def get_music_by_artist_id(artist_id: str) -> list:
    """
    Query itunes api to get all music by given artist.

    :param artist_id: itunes artist id
    :return: list of music by artist
    """
    music = []

    # get all songs by artist
    song_response = service.get(path=f"/lookup?id={artist_id}&entity=song")

    if song_response:
        music.extend(song_response.json().get("results"))

    # get all albums by artist
    album_response = service.get(path=f"/lookup?id={artist_id}&entity=album")

    if album_response:
        music.extend(album_response.json().get("results"))

    return music


def get_song_info(info: list, limit: int = 5) -> list:
    terms = [t.replace(' ', '+') for t in info if t]
    term = '+'.join(terms)
    url = f"https://itunes.apple.com/search?term={term}&entity=musicTrack&limit={limit}"
    response = requests.get(url)
    results = response.json().get("results")

    if not results:
        return []

    for r in results:
        r.update({"artworkUrl1000": r.get(
            "artworkUrl100").replace("100x100", "1000x1000")})

    return results
