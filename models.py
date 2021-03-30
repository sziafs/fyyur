from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.relationship('VenueGenre', backref='venue', lazy=True)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String)
    shows = db.relationship('Show', cascade='all, delete-orphan', backref='venue', lazy=True)

class VenueGenre(db.Model):
    __tablename__ = 'venue_genres'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.relationship('ArtistGenre', backref='artist', lazy=True)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String)
    shows = db.relationship('Show', cascade='all, delete-orphan', backref='artist', lazy=True)

class ArtistGenre(db.Model):
    __tablename__ = 'artist_genres'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))

class Show(db.Model):
    __tablename__='shows'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
    start_time  = db.Column(db.DateTime(), nullable=False)