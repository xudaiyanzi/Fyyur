#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# from app import db

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref

db = SQLAlchemy()

# from the datetime in the python to import datetime
# not need import it from sqlalchemy
from datetime import datetime

### set up a many-to-many relationship "shows" to link venue and artists
### build the association object


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    # DONE! 

    ## 1) by comparing the class model and pre-input data in /venues/<int:venue_id>,
    ####  Below are the missing fields

    genres = db.Column(db.String(120))
    website = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean, default=False, server_default="false")
    seeking_description = db.Column(db.String(1000))
    
    ### 2) build the relationship with model "Artist"
    # shows = relationship("Shows", backref=backref("Venue", lazy=True))
    artist = db.relationship("Artist", backref=backref("Venue"), secondary="Shows")

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    # DONE!!
    website = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean)

    venue = relationship("Venue", secondary="Shows")

class Shows(db.Model):
    __tablename__ = 'Shows'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
    artist_id = db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    venue = relationship(Venue, backref=backref("Shows", cascade="all, delete-orphan"))
    artist = relationship(Artist, backref=backref("Shows", cascade="all, delete-orphan"))