import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv
from user_utils import *
from playlist_utils import * 



def get_artistdetails(spotify_client, artist_id):
    return {i: spotify_client.artist(artist_id)[i] for i in ["id", "name", "genres"]}

def get_artistalbums(spotify_client, artist_id):
    return [i.get("id") for i in spotify_client.artist_albums(artist_id, album_type=None, country=None, limit=50, offset=0).get("items")]

def get_relevantartists(spotify_client, artist_id):
    relevanted = ["genres", "id", "name", "type"]
    output = []
    for i in spotify_client.artist_related_artists(artist_id).get("artists"):
        output.append(i["id"])
    return output

def get_artisttoptracks(spotify_client, artist_id, country_code="DE"):
    return [i.get("id") for i in spotify_client.artist_top_tracks(artist_id, country_code).get("tracks")]

