from dash import html
from dash import dcc

# Define the layout of the Dash app

def render_dashplaylistlayout(playlist_name, tracks):
    layout = html.Div(
        children=[
            html.H2(children=playlist_name),
            html.Div(
                children=[
                    html.Div(
                        className="track",
                        children=[
                            html.Div(
                                className="track-image-container",
                                children=[
                                    html.Img(
                                        src=track["album_image"],
                                        alt=track["name"],
                                        className="track-image",
                                    )
                                ],
                            ),
                            html.Div(
                                className="track-details",
                                children=[
                                    html.P(
                                        children=track["name"], className="track-name"
                                    ),
                                    html.P(
                                        children=track["artist_ids"],
                                        className="track-artist",
                                    ),
                                    html.Audio(src=track["preview_url"], controls=True),
                                ],
                            ),
                        ],
                    )
                    for track in tracks
                ],
                className="playlist-tracks",
            ),
        ],
        className="container playlist-container",
    )
    return layout
