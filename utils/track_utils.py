import pandas as pd

def get_trackdetails(spotify_client, track_id, usr_filter=None, playlist_id=None):
    result = spotify_client.track(track_id)
    result["id"] = track_id
    filtered = {i: result[i] for i in ["id", "name", "disc_number", "track_number", "preview_url"]}
    album = result.get("album")
    filtered["album_img"] = album.get("images")[0].get("url")
    filtered["album_id"] = album.get("id")
    artists = result.get("artists")
    artists = [i.get("id") for i in artists]
    artists = {"artist_ids": artists}
    filtered.update(artists)
    if usr_filter:
        filtered = {k: filtered[k] for k in usr_filter}
    if playlist_id:
        filtered["playlist_id"] = playlist_id
    return filtered


def get_audio_features_df(spotify_client, list_of_tracksid):
    if isinstance(list_of_tracksid,str):
        list_of_tracksid = [list_of_tracksid]
    return pd.DataFrame([{k:i[k] for k in i.keys() if k not in ["type", "uri", "track_href", "analysis_url"]} for i in spotify_client.audio_features(list_of_tracksid)])

def get_tempo(spotify_client, track_id):
    aa_out = spotify_client.audio_analysis(track_id)
    return int(aa_out.get("track").get('tempo'))

def get_audio_analysis_df(spotify_client, list_of_tracksid):
    output = []
    if isinstance(list_of_tracksid,str):
        list_of_tracksid = [list_of_tracksid]
    for track_id in list_of_tracksid:
        track_analysis = spotify_client.audio_analysis(track_id).get("track")
        filtered = {"track_id": track_id}
        filtered.update({key:track_analysis[key] for key in ["loudness", "tempo", "time_signature", "key", "mode"]})
        output.append(filtered)
    return pd.DataFrame(output)

def get_allarists_from_tracklists(spotify_client, list_of_trackids):
    list_listartists = [get_trackdetails(spotify_client, i).get("artists_ids") for i in list_of_trackids]
    flattened = list(set([artist for artist_list in list_listartists for artist in artist_list]))
    return flattened
