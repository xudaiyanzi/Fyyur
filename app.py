#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
# from flask_wtf import Form
from flask_wtf import FlaskForm

from forms import *
from models import db, Venue, Artist, Shows
from datetime import datetime
import sys

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

# TODO: connect to a local postgresql database
# DONE!!! 
### what I have done is go to the config and build the connection


app = Flask(__name__)
app.config.from_object('config')
moment = Moment(app)
db.init_app(app)

#### enable migrate
from flask_migrate import Migrate
migrate = Migrate(app, db)

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
# DONE!!!


## the "with" stattment can used to solve the "No application found" problem
with app.app_context():
  db.session.commit()

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  # DONE!!!

  wasNow = datetime.now()
  num_upcoming_shows = 0
  data = []

  locations = db.session.query(Venue.city, Venue.state).distinct()
  for location in locations:
    location_city = location.city
    location_state = location.state
    venue_data = []

    venue_filters = Venue.query.filter_by(city=location_city,state=location_state).all()

    for venue_filter in venue_filters:
      venue_id = venue_filter.id
      venue_name = venue_filter.name
      num_upcoming_shows = len(Shows.query.filter_by(venue_id=venue_id).filter(Shows.start_time>wasNow).all())
      venue_data.append({
        'id':venue_id,
        'name':venue_name,
        'num_upcoming_shows':num_upcoming_shows
      })
    
    data.append({
      'city':location_city,
      'state':location_state,
      'venues':venue_data
    })

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  # DONE!!!
    
    search_term=request.form.get('search_term', '')
    venue_searches = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
    data = []

    for venue_search in venue_searches:
      data.append({
          'id': venue_search.id,
          'name': venue_search.name,
          'num_upcoming_shows': len(Shows.query.filter_by(venue_id=venue_search.id).filter(Shows.start_time>datetime.now()).all())
      })
      
    response = {
        'count':len(venue_searches),
        'data':data
      }

    return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

#Done!!!

  data_get = Venue.query.get(venue_id)

  past_shows = []
  upcoming_shows = []

  for show in Shows.query.filter_by(venue_id=venue_id).all():

    artist_id = show.artist_id
    artist_name = Artist.query.filter_by(id=artist_id).first().name
    artist_image_link = Artist.query.filter_by(id=artist_id).first().image_link
    start_time = show.start_time.strftime("%m/%d/%Y, %H:%M")
    show_item = {
      "artist_id" : artist_id,
      "artist_name" : artist_name,
      "artist_image_link" : artist_image_link,
      "start_time" : start_time
    }

    if show.start_time > datetime.now():
      upcoming_shows.append(show_item)
    else:
      past_shows.append(show_item)

  data = {
    "id": data_get.id,
    "name": data_get.name,
    "city": data_get.city,
    "state": data_get.state,
    "address": data_get.address,
    "phone": data_get.phone,
    "website": data_get.website,
    "genres": data_get.genres,
    "website": data_get.website,
    "facebook_link": data_get.facebook_link,
    "seeking_talent": data_get.seeking_talent,
    "seeking_description": data_get.seeking_description,
    "image_link": data_get.image_link,
    "past_shows": past_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows": upcoming_shows,
    "upcoming_shows_count": len(upcoming_shows)
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

# @app.route('/venues/create', methods=['GET', 'POST'])

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

# DONE!!!
  # # start with no error
  error = False

  # use try-except-close to control the session controller
  ## this could help handle errors
      
  try:
      # use the request to get the data from html
  # if request.method == 'POST': 

      name = request.form['name']
      city = request.form['city']
      state = request.form['state']
      address = request.form['address']
      phone = request.form['phone']
      genres = request.form['genres']
      facebook_link = request.form['facebook_link']
      image_link = request.form['image_link']
      website = request.form['website_link']
      
      #### for the seeking_talent field, we want to check if the checkbox is checked
      #### if it is, then we want to set seeking_talent to true
      if 'seeking_talent' in request.form:
            seeking_talent = True
      else:
            seeking_talent = False

      #### here, we should not just get the request.form['seeking_talent']
      #### becasue it returns a string, not a boolean
      #### we need to convert it to boolean

      # seeking_talent = request.form['seeking_talent']
      # seeking_talent = request.form.get('seeking_talent')

      #### we also do not use the checkbox syntex as the todo_app project
      #### because we used the wtforms library. it is much easier
      #### one can revise the code in todo_app with wtforms and see how it is different


      seeking_description= request.form['seeking_description']
      
      venue_item = Venue(name=name, city=city, state=state, address=address, 
                          phone=phone, genres=genres, facebook_link=facebook_link,
                          image_link=image_link, website=website,
                          seeking_talent=seeking_talent, seeking_description=seeking_description)

      db.session.add(venue_item)
      db.session.commit()
      
  except:
      db.session.rollback()
      error=True
      print(sys.exc_info())
  finally:
      db.session.close()

  # TODO: on unsuccessful db insert, flash an error instead.

  if error:
    flash('Oops, an error occurred in Venue! ' + 'The ' + request.form['name'] + ' could not be listed.' )

  else:
      # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')


  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')
  

# @app.route('/venues/<venue_id>', methods=['DELETE'])
@app.route('/venues/<int:venue_id>/delete', methods=['DELETE'])

def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # DONE!!!
  
  # # start with no error
  error = False
  
  try:

      Shows.query.filter_by(venue_id=venue_id).delete()
      Venue.query.filter_by(id=venue_id).delete()
      
      db.session.commit()

  except:
      db.session.rollback()

  finally:
      db.session.close()
  
  if error:
    flash('Oops, an error occurred in Venue! The venue could not be delete.' )

  else:
    flash('The venue was successfully deleted!')

  #### can not use redirect(url) here, because it gives a 405 error
  #### redirect is not allowed in a DELETE request
  return jsonify({'success':True})

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  # DONE!!!

  data = []
  artist_info = {}

  artist_filters = Artist.query.all()

  for artist_filter in artist_filters:
      artist_id = artist_filter.id
      artist_name = artist_filter.name
      artist_info = {
        "id": artist_id,
        "name": artist_name
      }
    
      data.append(artist_info)

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  # Done!!!
  search_term=request.form.get('search_term', '')
  artist_searches = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
  data = []

  for artist_search in artist_searches:
      data.append({
          'id': artist_search.id,
          'name': artist_search.name,
          'num_upcoming_shows': len(Shows.query.filter_by(artist_id=artist_search.id).filter(Shows.start_time>datetime.now()).all())
      })
      
  response = {
        'count':len(artist_searches),
        'data':data
      }

  return render_template('pages/search_artists.html', results=response, search_term=search_term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  # DONE!!!

  data_get = Artist.query.get(artist_id)
  past_shows = []
  upcoming_shows = []

  for show in Shows.query.filter_by(artist_id=artist_id).all():

    venue_id = show.venue_id
    venue_name = Venue.query.filter_by(id=venue_id).first().name
    venue_image_link = Venue.query.filter_by(id=venue_id).first().image_link
    start_time = show.start_time.strftime("%m/%d/%Y, %H:%M")
    
    show_item = {
      "venue_id" : venue_id,
      "venue_name" : venue_name,
      "venue_image_link" : venue_image_link,
      "start_time" : start_time
    }

    if show.start_time < datetime.now():
      past_shows.append(show_item)

    if show.start_time > datetime.now():
      upcoming_shows.append(show_item)

  data = {
    "id": data_get.id,
    "name": data_get.name,
    "city": data_get.city,
    "state": data_get.state,
    "phone": data_get.phone,
    "website": data_get.website,
    "genres": data_get.genres,
    "website": data_get.website,
    "facebook_link": data_get.facebook_link,
    "seeking_venue": data_get.seeking_venue,
    "seeking_description": data_get.seeking_description,
    "image_link": data_get.image_link,
    "past_shows": past_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows": upcoming_shows,
    "upcoming_shows_count": len(upcoming_shows)
  }

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

# TODO: populate form with fields from artist with ID <artist_id>
# DONE!!!
  artist = Artist.query.filter_by(id=artist_id).first()
  form = ArtistForm(obj=artist)
  
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attribute values.

  error = False

  artist = Artist.query.filter_by(id=artist_id).first_or_404()
  form = ArtistForm(request.form)

  try:
      artist.name = request.form['name']
      artist.city = request.form['city']
      artist.state = request.form['state']
      artist.phone = request.form['phone']
      artist.genres = request.form['genres']
      artist.facebook_link = request.form['facebook_link']
      artist.image_link = request.form['image_link']
      artist.website = request.form['website_link']

      if 'seeking_venue' in request.form:
            artist.seeking_venue = True
      else:
            artist.seeking_venue = False


      artist.seeking_description= request.form['seeking_description']
      db.session.commit()
      
  except:
      db.session.rollback()
      error=True
      print(sys.exc_info())
  finally:
      db.session.close()

  # TODO: on unsuccessful db insert, flash an error instead.
  if error:
    flash('Oops, an error occurred in Artist! ' + 'The ' + request.form['name'] + ' could not be updated.' )

  else:
      # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully updated!')

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):

  # TODO: populate form with values from venue with ID <venue_id>
  # DONE!!!
  venue = Venue.query.filter_by(id=venue_id).first()
  form = VenueForm(obj=venue)

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  # DONE!!!
  error = False

  venue = Venue.query.filter_by(id=venue_id).first_or_404()
  form = VenueForm(request.form)

  try:
      venue.name = request.form['name']
      venue.city = request.form['city']
      venue.state = request.form['state']
      venue.address = request.form['address']
      venue.phone = request.form['phone']
      venue.genres = request.form['genres']
      venue.facebook_link = request.form['facebook_link']
      venue.image_link = request.form['image_link']
      venue.website = request.form['website_link']

      if 'seeking_talent' in request.form:
            venue.seeking_talent = True
      else:
            venue.seeking_talent = False


      venue.seeking_description= request.form['seeking_description']
      db.session.commit()
      
  except:
      db.session.rollback()
      error=True
      print(sys.exc_info())
  finally:
      db.session.close()

  # TODO: on unsuccessful db insert, flash an error instead.
  if error:
    flash('Oops, an error occurred in Venue! ' + 'The ' + request.form['name'] + ' could not be updated.' )

  else:
      # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully updated!')
  
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: modify data to be the data object returned from db insertion
 # Done!!!

  error = False
  try:
      name = request.form['name']
      city = request.form['city']
      state = request.form['state']
      phone = request.form['phone']
      genres = request.form['genres']
      facebook_link = request.form['facebook_link']
      image_link = request.form['image_link']
      website = request.form['website_link']

      if 'seeking_venue' in request.form:
            seeking_venue = True
      else:
            seeking_venue = False


      seeking_description= request.form['seeking_description']
      
      artist_item = Artist(name=name, city=city, state=state,
                          phone=phone, genres=genres, facebook_link=facebook_link,
                          image_link=image_link, website=website,
                          seeking_venue=seeking_venue, seeking_description=seeking_description)

      db.session.add(artist_item)
      db.session.commit()
      
  except:
      db.session.rollback()
      error=True
      print(sys.exc_info())
  finally:
      db.session.close()

  # TODO: on unsuccessful db insert, flash an error instead.
  if error:
    flash('Oops, an error occurred in Artist! ' + 'The ' + request.form['name'] + ' could not be listed.' )

  else:
      # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')

  return render_template('pages/home.html')



#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  # DONE!!!

  data = []
  show_item = {}
  
  for show in Shows.query.all():
      venue_id = Venue.query.filter_by(id=Shows.venue_id).first().id
      venue_name = Venue.query.filter_by(id=Shows.venue_id).first().name

      artist_id = Artist.query.filter_by(id=Shows.artist_id).first().id
      artist_name = Artist.query.filter_by(id=Shows.artist_id).first().name
      artist_image_link = Artist.query.filter_by(id=Shows.artist_id).first().image_link

      start_time = Shows.query.filter_by(id=Shows.id).first().start_time.strftime("%m/%d/%Y, %H:%M")

      show_item = {
        "id": show.id,
        "venue_id": venue_id,
        "venue_name": venue_name,
        "artist_id": artist_id,
        "artist_name": artist_name,
        "artist_image_link": artist_image_link,
        "start_time": start_time
      }
      data.append(show_item)

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  # Done!!!

  error = False
  try:
      venue_id = request.form['venue_id']
      artist_id = request.form['artist_id']
      start_time = request.form['start_time']
      show_item = Shows(venue_id=venue_id, 
                        artist_id=artist_id, 
                        start_time=start_time)
      db.session.add(show_item)
      db.session.commit()  
  except:
      db.session.rollback()
      error=True
      print(sys.exc_info())
  finally:
      db.session.close()
  if error:
    flash('Oops, an error occurred in Show! ' + 'The Venue (id: ' + venue_id + ') and the Artist (id:' + artist_id +') could not be listed.' )
  else:
    flash('Show was successfully listed!')
  return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
