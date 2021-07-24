#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
from sqlalchemy.dialects.postgresql import JSON
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref

db = SQLAlchemy()


# from the datetime in the python to import datetime
# not need import it from sqlalchemy
from datetime import datetime

### set up a many-to-many relationship "shows" to link venue and artists
### build the association object


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(1000))
    facebook_link = db.Column(db.String(500))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    # DONE! 

    ## 1) by comparing the class model and pre-input data in /venues/<int:venue_id>,
    ####  Below are the missing fields

    genres = db.Column(JSON)
    website = db.Column(db.String(1000))
    seeking_talent = db.Column(db.Boolean, default=False, server_default="false", nullable=False)
    seeking_description = db.Column(db.String(1000))
    

    shows = relationship("shows", backref=backref("venues", lazy=True))
    ### 2) build the relationship with model "Artist"
    # # artist = db.relationship("Artist", backref=backref("Venue"), secondary="Shows")

    def __repr__(self):
        return "<venues>" % self.name

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(JSON)
    image_link = db.Column(db.String(1000))
    facebook_link = db.Column(db.String(500))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    # DONE!!
    website = db.Column(db.String(1000))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(1000))

    shows = relationship("shows", backref=backref("artists", lazy=True))
    # venue = relationship("Venue", secondary="Shows")

    def __repr__(self):
        return "<artists>" % self.name

class Shows(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    venue_id = db.Column('venue_id', db.Integer, db.ForeignKey('venues.id', ondelete='CASCADE'), nullable=False)
    artist_id = db.Column('artist_id', db.Integer, db.ForeignKey('artists.id', ondelete='CASCADE'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "<shows>" % self.id % self.venue_id % self.artist_id % self.start_time

