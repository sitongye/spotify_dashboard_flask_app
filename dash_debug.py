import dash
from dash import html
from dash_playlistdashboard.playlist import render_dashplaylistlayout
from dash_playlistdashboard.dash_baselayout import BaseLayout
import dash_bootstrap_components as dbc

tracks = [
    {
        "name": "Track 1",
        "artist_ids": "Artist 1",
        "album_image": "https://via.placeholder.com/150",
        "preview_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    },
    {
        "name": "Track 2",
        "artist_ids": "Artist 2",
        "album_image": "https://via.placeholder.com/150",
        "preview_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
    },
    {
        "name": "Track 3",
        "artist_ids": "Artist 3",
        "album_image": "https://via.placeholder.com/150",
        "preview_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
    },
]

playlist_name = "My Playlist"

EXTERNAL_STYLESHEET = [dbc.themes.BOOTSTRAP, "/static/css/styles.css"]
dash_app = dash.Dash(
    __name__,
    external_stylesheets=EXTERNAL_STYLESHEET)



dash_app.layout = BaseLayout(render_dashplaylistlayout(playlist_name, tracks))

# run the app
if __name__ == "__main__":
    dash_app.run_server(debug=True)