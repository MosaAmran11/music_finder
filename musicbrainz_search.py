import requests
from config import LASTFM_API_KEY, YOUTUBE_API_KEY
import urllib.parse


def get_youtube_thumbnail(artist, title, album=None):
    """Get thumbnail from YouTube Music search."""
    try:
        # Construct search query
        search_query = f"{artist} {title}"
        if album:
            search_query += f" {album}"
        search_query += " music"

        # Search YouTube
        encoded_query = urllib.parse.quote(search_query)
        search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={encoded_query}&type=video&videoCategoryId=10&key={YOUTUBE_API_KEY}"

        response = requests.get(search_url)
        if response.status_code == 200:
            data = response.json()
            if "items" in data and len(data["items"]) > 0:
                # Get the highest quality thumbnail available
                thumbnails = data["items"][0]["snippet"]["thumbnails"]
                if "maxres" in thumbnails:
                    return thumbnails["maxres"]["url"]
                elif "high" in thumbnails:
                    return thumbnails["high"]["url"]
                elif "medium" in thumbnails:
                    return thumbnails["medium"]["url"]
                elif "default" in thumbnails:
                    return thumbnails["default"]["url"]
    except Exception as e:
        print(f"Error getting YouTube thumbnail: {e}")
    return None


def search_musicbrainz(title, artist):
    query = f"recording:{title} AND artist:{artist}"
    url = f"https://musicbrainz.org/ws/2/recording/?query={query}&fmt=json"
    try:
        response = requests.get(
            url, headers={"User-Agent": "SongMetadataApp/1.0 ( email@example.com )"})
        if response.status_code == 200:
            data = response.json()
            recordings = data.get("recordings", [])

            # Add cover art information to each recording using Last.fm
            for recording in recordings:
                if recording.get("releases"):
                    release_title = recording["releases"][0].get("title")
                    artist_name = recording["artist-credit"][0].get("name")
                    track_title = recording.get("title")

                    if track_title and artist_name:
                        # Use Last.fm API to get track info first
                        encoded_artist = urllib.parse.quote(artist_name)
                        encoded_track = urllib.parse.quote(track_title)
                        lastfm_url = f"http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={LASTFM_API_KEY}&artist={encoded_artist}&track={encoded_track}&format=json"

                        try:
                            lastfm_response = requests.get(lastfm_url)
                            if lastfm_response.status_code == 200:
                                lastfm_data = lastfm_response.json()

                                # Try to get album art from track info first
                                if "track" in lastfm_data and "album" in lastfm_data["track"]:
                                    images = lastfm_data["track"]["album"].get(
                                        "image", [])
                                    # Try different image sizes in order of preference
                                    for size in ["extralarge", "large", "medium"]:
                                        for image in images:
                                            if image["size"] == size:
                                                recording["cover_art"] = image["#text"]
                                                break
                                        if recording.get("cover_art"):
                                            break

                                # If no cover art found from track, try album search
                                if not recording.get("cover_art") and release_title:
                                    encoded_album = urllib.parse.quote(
                                        release_title)
                                    album_url = f"http://ws.audioscrobbler.com/2.0/?method=album.getInfo&api_key={LASTFM_API_KEY}&artist={encoded_artist}&album={encoded_album}&format=json"
                                    album_response = requests.get(album_url)
                                    if album_response.status_code == 200:
                                        album_data = album_response.json()
                                        if "album" in album_data and "image" in album_data["album"]:
                                            images = album_data["album"]["image"]
                                            for size in ["extralarge", "large", "medium"]:
                                                for image in images:
                                                    if image["size"] == size:
                                                        recording["cover_art"] = image["#text"]
                                                        break
                                                if recording.get("cover_art"):
                                                    break

                            # If Last.fm didn't provide a cover, try YouTube Music
                            if not recording.get("cover_art"):
                                youtube_thumbnail = get_youtube_thumbnail(
                                    artist_name, track_title, release_title)
                                if youtube_thumbnail:
                                    recording["cover_art"] = youtube_thumbnail
                                    recording["cover_source"] = "youtube"
                                else:
                                    recording["cover_art"] = None
                        except:
                            recording["cover_art"] = None
                    else:
                        recording["cover_art"] = None
                else:
                    recording["cover_art"] = None

            return recordings
        else:
            return []
    except Exception as e:
        print(f"Error querying MusicBrainz: {e}")
        return []
