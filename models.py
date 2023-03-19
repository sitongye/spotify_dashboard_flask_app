from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    country = db.Column(db.String(50))
    display_name = db.Column(db.String(120))
    href = db.Column(db.String(300), unique=True, nullable=False)
    id = db.Column(db.String(200), unique=True, primary_key=True)
    images =db.Column(db.String(120))
    uri = db.Column(db.String(120), unique=True)
    external_urls = db.Column(db.String(200))
    def __init__(self, data):
        self.id = data['id']
        self.country = data.get('country')
        self.display_name = data.get('display_name')
        self.href = data['href']
        self.images = data.get('images')
        self.uri = data.get('uri')
        self.external_urls = data.get('external_urls')

    def __repr__(self):
        return f"User('{self.id}', '{self.display_name}')"
    

class Playlist(db.Model):
    id = db.Column(db.String(255), unique=True, primary_key=True)
    images =db.Column(db.String(255))
    external_urls = db.Column(db.String(255), unique=True)
    uri = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))
    user_id = db.Column(db.String(255))
    track_ids = db.Column(db.JSON)

    def __init__(self, data):
        self.id = data['id']
        self.images = data['images']
        self.external_urls = data['external_urls']
        self.uri = data['uri']
        self.name = data['name']
        self.user_id = data['user_id']
        self.track_ids = data['track_ids']

    def __repr__(self):
        return f"Playlist('{self.id}', '{self.name}')"

class Track(db.Model):
    id = db.Column(db.String(255), primary_key=True, unique=True)
    playlist_id = db.Column(db.String(255), db.ForeignKey('playlist.id'))
    playlist = db.relationship('Playlist', backref=db.backref('tracks', lazy=True))
    name = db.Column(db.String(255))
    disc_number = db.Column(db.Integer)
    track_number = db.Column(db.Integer)
    preview_url = db.Column(db.String(255))
    album_id = db.Column(db.String(255))
    album_img = db.Column(db.String(255))
    artist_ids = db.Column(db.JSON)
    danceability = db.Column(db.Float)
    energy = db.Column(db.Float)
    key = db.Column(db.Integer)
    loudness = db.Column(db.Float)
    mode = db.Column(db.Integer)
    speechiness = db.Column(db.Float)
    acousticness = db.Column(db.Float)
    instrumentalness = db.Column(db.Float)
    liveness = db.Column(db.Float)
    valence = db.Column(db.Float)
    tempo = db.Column(db.Float)
    duration_ms = db.Column(db.Integer)
    time_signature = db.Column(db.Integer)

    def __init__(self, data):
        self.id = data.get('id')
        self.playlist_id = data.get("playlist_id") # can be None
        self.name = data.get('name')
        self.disc_number = data.get('disc_number')
        self.track_number = data.get('track_number')
        self.preview_url = data.get('preview_url')
        self.album_id = data.get('album_id')
        self.album_img = data.get("album_img")
        self.artist_ids = data.get('artist_ids')
        self.danceability = data.get('danceability')
        self.energy = data.get('energy')
        self.key = data.get('key')
        self.loudness = data.get('loudness')
        self.mode = data.get('mode')
        self.speechiness = data.get('speechiness')
        self.acousticness = data.get('acousticness')
        self.instrumentalness = data.get('instrumentalness')
        self.liveness = data.get('liveness')
        self.valence = data.get('valence')
        self.tempo = data.get('tempo')
        self.duration_ms = data.get('duration_ms')
        self.time_signature = data.get('time_signature')

