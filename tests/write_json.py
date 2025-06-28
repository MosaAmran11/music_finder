from music.services.itunes_api import get_song_info
from json import JSONEncoder

with open("test.json", "w") as f:
    results = get_song_info('close your eyes', artist='KSHMR')
    if results:
        f.write(str(JSONEncoder.encode(JSONEncoder(), results)))
