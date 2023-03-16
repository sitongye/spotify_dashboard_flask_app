import pandas as pd

def get_userdetails(spotify_client):
    details = spotify_client.me()
    usrdetails = {k:details[k] for k in details if k not in ["email", "options", "explicit_content", "followers", "images", "product", "type"]}
    img = {"images": details.get("images")[0].get("url")}
    external_url = {"external_urls": details.get("external_urls").get("spotify")}
    usrdetails.update(external_url)
    usrdetails.update(img)
    return usrdetails


def get_currentusrplaylists(spotify_client):
    usr_plylsts_results = spotify_client.current_user_playlists()
    plysts = usr_plylsts_results.get("items")
    while usr_plylsts_results['next']:
        usr_plylsts_results = spotify_client.next(usr_plylsts_results)
        plysts.extend(usr_plylsts_results['items'])
    
    #return [i.get("id") for i in plysts]
    return plysts

def get_usrplaylist_tracks(spotify_client, username, playlist_id, limit=100):
    results = spotify_client.user_playlist_tracks(username,playlist_id, limit=limit)
    tracks = results['items']
    while results['next']:
        results = spotify_client.next(results)
        tracks.extend(results['items'])
    return [i.get("track").get("id") for i in tracks]

def get_currentusr_recentplay(spotify_client):
    return [i.get("track").get("id") for i in spotify_client.current_user_recently_played(50).get("items")]
