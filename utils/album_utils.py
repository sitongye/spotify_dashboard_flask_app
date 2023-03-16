import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv
from user_utils import *
from playlist_utils import * 


def get_albumdetails(spotify_client, album_id):
    result = spotify_client.album(album_id)
    filtered = {i: result[i] for i in ["id", "name", "genres", 'release_date','total_tracks']}
    tracks = result.get("tracks")
    tracks = {"tracks":[i.get("id") for i in tracks.get("items")]}
    filtered.update(tracks)
    return filtered