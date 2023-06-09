import os
import dash
import spotipy
from dotenv import load_dotenv
from flask import Flask, redirect, request, session, render_template, url_for
from flask_session import Session
from utils.playlist_utils import get_playlistdetails
from utils.track_utils import get_trackdetails, get_audio_features_df
from utils.user_utils import get_userdetails, get_currentusrplaylists
from models import db, User, Playlist, Track
from dash_playlistdashboard.playlist import render_dashplaylistlayout, gen_card
from flask.blueprints import Blueprint
from dash import html, dcc, Output, Input
from dash.dependencies import Input, Output
import pandas as pd
import dash_mantine_components as dmc

load_dotenv()


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(64)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "./.flask_session/"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///spotify_app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
Session(app)
db.init_app(app)

metadata = {}
for table in db.metadata.tables.values():
    metadata[table.name] = [column.name for column in table.columns]


def insert_user(userprofile_dict):
    user_data = userprofile_dict
    # Check if user exists in database
    user = User.query.filter_by(id=user_data.get("id")).first()
    new_user = User(user_data)
    if user:
        # User already exists in database, update the existing record
        db.session.merge(new_user)
    else:

        db.session.add(new_user)
    db.session.commit()


def insert_playlist(playlistdetailsdict):
    # Check if playlist exists in database
    playlist = Playlist.query.filter_by(id=playlistdetailsdict.get("id")).first()
    new_plt = Playlist(playlistdetailsdict)
    if playlist:
        # User already exists in database, update the existing record
        db.session.merge(new_plt)
    else:
        db.session.add(new_plt)
    db.session.commit()

def insert_or_update_tracks(tracks_data):
    for track_data in tracks_data:
        track_id = track_data['id']
        track = Track.query.filter_by(id=track_id).first()
        new_track = Track(track_data)
        if track:
            db.session.merge(new_track)
        else:
            db.session.add(new_track)
    db.session.commit()

@app.route("/")
def index():

    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope="user-read-currently-playing playlist-read-private playlist-modify-private user-read-private",
        cache_handler=cache_handler,
        show_dialog=True,
    )

    if request.args.get("code"):
        # Step 2. Being redirected from Spotify auth page
        token = auth_manager.get_access_token(request.args.get("code"), as_dict=False)
        return redirect("/")

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 1. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return render_template("sign_in.html", authlink=auth_url)

    # Step 3. Signed in, display data
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    usr_dict = get_userdetails(spotify)
    usr_id = usr_dict.get("id")
    insert_user(usr_dict)
    return render_template(
        "greeting.html",
        username=spotify.me()["display_name"],
        redirectlink="/playlists",
    )


@app.route("/logout")
def logout():
    session.pop("token_info", None)
    return redirect("/")


@app.route("/playlists")
def playlists():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect("/")
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    userplaylists = spotify.current_user_playlists().get("items")
    return render_template("playlists.html", playlists=userplaylists)


@app.route("/currently_playing")
def currently_playing():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect("/")
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    track = spotify.current_user_playing_track()
    if not track is None:
        return track
    return "No track currently playing."


@app.route("/current_user")
def current_user():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect("/")
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify.current_user()



################dash################
EXTERNAL_STYLESHEET = ["/static/css/bootstrap.min.css", "/static/css/styles.css"]
dash_bp = Blueprint("dashplaylist", __name__, url_prefix="/dashboard/playlist")
dash_app = dash.Dash(
    __name__,
    server=app,
    url_base_pathname="/dashboard/playlist/",
    external_stylesheets=EXTERNAL_STYLESHEET,
    assets_folder="/static/css/", suppress_callback_exceptions = True
)
dash_app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

def render_playlist_layout(playlist_id):
    # Define your playlist layout here
    layout = html.Div([
        html.H1(f"Playlist {playlist_id}"),
        # Add other components here
    ])
    return layout
 

@dash_bp.route("/<playlist_id>/")

def dash_playlist(playlist_id):
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect(url_for("index"))
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    playlist_details = get_playlistdetails(spotify, playlist_id)
    playlist_name = playlist_details.get("name")
    trackids = playlist_details.get("track_ids")
    tracks = [
        get_trackdetails(
            spotify,
            i,
            playlist_id=playlist_id
        )
        for i in trackids
    ]
    tracks_audio_feature = get_audio_features_df(spotify, trackids)
    merged = pd.DataFrame(tracks).merge(tracks_audio_feature, on="id")
    insert_or_update_tracks(merged.to_dict("records"))
    tracks = Track.query.filter_by(playlist_id=playlist_id).all()
    dash_app.layout = render_dashplaylistlayout(tracks, playlist_name)

    @dash_app.callback(Output("card_content", "children"),
                       Input("playlist-accordion", "value"))
    def gen_card_widget(track_id, prevent_inital_call=True):
        if track_id:
            track = Track.query.get(track_id)
            return gen_card(track)

    # Return the rendered playlist dashboard
    return dash_app.index()


app.register_blueprint(dash_bp)
"""
Following lines allow application to be run more conveniently with
`python app.py` (Make sure you're using python3)
(Also includes directive to leverage pythons threading capacity.)
"""
if __name__ == "__main__":
    with app.app_context():
        #db.drop_all()
        db.create_all()
    app.run(threaded=True, port=5000, debug=True)
