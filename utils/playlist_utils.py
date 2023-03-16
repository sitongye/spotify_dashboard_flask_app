import pandas as pd


def get_playlistdetails(spotify_client, playlist_id):
    result = spotify_client.playlist(playlist_id)
    filtered = {i: result[i] for i in ["id", "uri", "name"]}
    filtered["images"] = result.get("images")[0].get("url")
    filtered["external_urls"] = result.get("external_urls").get("spotify")
    tracks = result.get("tracks").get("items")
    trackids = [i.get("track").get("id") for i in tracks]# gets a list of track objects
    usr_tracks = {"tracks":";".join(trackids)}
    filtered.update(usr_tracks)
    owner = result.get("owner")
    owner = {"user_id": owner.get("id")}
    filtered.update(owner)
    return filtered