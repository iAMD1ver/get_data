# Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию через curl, Postman, Python.

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

cid = "353b61ac74144326ab6bcd987f57d8c5"
secret = "925feeedfb26413d8753c4de734b86ac"

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

birdy_uri = 'spotify:artist:5eAWCfyUhZtHHtBdNk56l1'

results = sp.artist_albums(birdy_uri, album_type='album')

artist = results['items'][0]['artists'][0]

with open('artist.json', 'w', encoding='utf-8') as f:
    json.dump(artist, f)