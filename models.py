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

    def __repr__(self):
        return f"User('{self.id}', '{self.display_name}')"
    

class Playlist(db.Model):
    id = db.Column(db.String(200), unique=True, primary_key=True)
    images =db.Column(db.String(120))
    external_urls = db.Column(db.String(200), unique=True)
    uri = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(120))
    user_id = db.Column(db.String(200))
    tracks = db.Column(db.String(5000))

    def __repr__(self):
        return f"Playlist('{self.id}', '{self.name}')"
#class Track(db.Model):
