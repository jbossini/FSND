#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import datetime
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# DONE: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


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
    genres= db.Column(ARRAY(db.String()), nullable=False)
    website=db.Column(db.String(1000),nullable=True)
    seeking_talent=db.Column(db.Boolean, default=False)
    seeking_description=db.Column(db.String(500), nullable=True)
    shows = db.relationship('Show', backref='Venue', lazy=True)
    #genres = db.relationship('Venue_Genres', backref='Venue', lazy=True)
    def __repr__(self):
        return f'<VENUE [ ID :{self.id} \n  NAME :{self.name} \n CITY : {self.city} \n state :{self.state} \n ADDRESS: {self.address} \n PHONE :{self.phone} \n IMAGE : {self.image_link} \n FACEBOOK : {self.facebook_link} \n SHOWS : {self.shows} \n GENRES : {self.genres}] >'

    # DONE: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres= db.Column(ARRAY(db.String()), nullable=False)
    website=db.Column(db.String(1000),nullable=True)
    seeking_venue=db.Column(db.Boolean, default=False)
    seeking_description=db.Column(db.String(500), nullable=True)
    shows = db.relationship('Show', backref='Artist', lazy=True)
    #genres = db.relationship('Artist_Genres', backref='Artist', lazy=True)
    # DONE: implement any missing fields, as a database migration using Flask-Migrate

# DONE Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
    def __repr__(self):
        return f'<ARTIST [ ID :{self.id} \n  NAME :{self.name} \n CITY : {self.city} \n state :{self.state} \n PHONE :{self.phone} \n IMAGE : {self.image_link} \n FACEBOOK : {self.facebook_link} \n SHOWS : {self.shows} \n GENRES : {self.genres}] >'


class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    id_venue = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    id_artist = db.Column(db.Integer, db.ForeignKey(
        'Artist.id'), nullable=False)
    show_date = db.Column(db.DateTime, nullable=False)
    def __repr__(self):
      return f'<SHOW [ id: {self.id} \n id_venue: {self.id_venue} \n id_artist {self.id_artist} \n date: {self.show_date}'

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


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
    # DONE: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    venues_distinct_cities = db.session.query(Venue).distinct(Venue.city).all()
    data=[]
    for venue_city in venues_distinct_cities:
        venues = db.session.query(Venue).filter_by(city=venue_city.city).all()
        list_venue=[]
        for venue in venues:
            upcoming_shows=[show for show in venue.shows if show.show_date>=datetime.now() ]
            list_venue.append({'id': venue.id, 'name':venue.name,'num_upcoming_shows':len(upcoming_shows)})
        data.append({'city':venue_city.city,'state':venue_city.state,'venues':list_venue})
    return render_template('pages/venues.html', areas=data)
    


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')
    venues = Venue.query.filter(Venue.name.ilike('%'+search_term+'%')).all()
    # DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    data=[]
    for venue in venues:
        upcoming_shows = [show for show in venue.shows if show.show_date>=datetime.now() ]
        data.append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": len(upcoming_shows)
        })
    response={"count":len(venues),"data":data}
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))
#  --------------------------------------------------------------------------------------
#  Util for formatting past and upcoming shows
#  ---------------------------------------------------------------------------------------
def format_show_artist(show):
    return {"artist_id":show.id_artist,"artist_name":show.Artist.name,"artist_image_link":show.Artist.image_link,"start_time":show.show_date.strftime("%m/%d/%Y, %H:%M")}
def format_artist_venue(show):
    return {"venue_id":show.id_venue,"venue_name":show.Venue.name,"venue_image_link":show.Venue.image_link,"start_time":show.show_date.strftime("%m/%d/%Y, %H:%M")}
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # DONE: replace with real venue data from the venues table, using venue_id
    venue = Venue.query.filter_by(id=venue_id).one_or_none()
    error=False
    if venue!=None:
        past_shows = [format_show_artist(show) for show in venue.shows if show.show_date< datetime.now() ]
        upcoming_shows=[format_show_artist(show) for show in venue.shows if show.show_date>=datetime.now() ]
        data = {
            "id": venue.id,
            "name": venue.name,
            "genres": venue.genres,
            "address": venue.address,
            "city": venue.city,
            "state": venue.state,
            "phone": venue.phone,
            "website": venue.website,
            "facebook_link": venue.facebook_link,
            "seeking_talent": venue.seeking_talent,
            "seeking_description": venue.seeking_description,
            "image_link": venue.image_link,
            "past_shows": past_shows,
            "upcoming_shows": upcoming_shows,
            "past_shows_count": len(past_shows),
            "upcoming_shows_count": len(upcoming_shows),
        }
        return render_template('pages/show_venue.html', venue=data)
    else: 
        error=True
        flash('An error ocurred.Venue does not exists!','error')
        return redirect(url_for('venues'))
    

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    
    form = VenueForm(request.form)
    # DONE: insert form data as a new Venue record in the db, instead
    venue = Venue(
        name = form.name.data, 
        city = form.city.data,
        state = form.state.data,
        address= form.address.data,
        phone= form.phone.data,
        genres= form.genres.data,
        facebook_link= form.facebook_link.data
    )
    try:
        db.session.add(venue)
        db.session.commit()
        # on successful db insert, flash success
        flash('Venue ' + venue.name + ' was successfully listed!')
    except:
        # DONE: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        # DONE: modify data to be the data object returned from db insertion
        flash('An error ocurred.Venue ' + venue.name+ 'could not be listed!','error')
    finally:
        db.session.close()
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # DONE: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    error = False
    body={}
    try:
        venue = Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
    except:
        db.session.rollback()
        error=True
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return redirect(url_for('index'))
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # DONE: replace with real data returned from querying the database
    list_artist=Artist.query.all()
    data=[]
    for artist in list_artist:
        data.append({"id": artist.id, "name": artist.name})
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    search_term = request.form.get('search_term', '')
    artists = Artist.query.filter(Artist.name.ilike('%'+search_term+'%')).all()
    data=[]
    for artist in artists:
        upcoming_shows = len([show for show in artist.shows if show.show_date>=datetime.now() ])
        data.append({"id":artist.id,"name":artist.name,"num_upcoming_shows":upcoming_shows})
    response = {
        "count": len(artists),
        "data": data
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # DONE: replace with real venue data from the venues table, using venue_id

    artist=Artist.query.filter_by(id=artist_id).one_or_none()
    error=False
    if artist!=None:
        past_shows = [format_artist_venue(show) for show in artist.shows if show.show_date< datetime.now() ]
        upcoming_shows=[format_artist_venue(show) for show in artist.shows if show.show_date>=datetime.now() ]
        data = {
            "id": artist.id,
            "name": artist.name,
            "genres": artist.genres,
            "city": artist.city,
            "state": artist.state,
            "phone": artist.phone,
            "website": artist.website,
            "facebook_link": artist.facebook_link,
            "seeking_venue": artist.seeking_venue,
            "seeking_description": artist.seeking_description,
            "image_link": artist.image_link,
            "past_shows": past_shows,
            "upcoming_shows": upcoming_shows,
            "past_shows_count": len(past_shows),
            "upcoming_shows_count": len(upcoming_shows)
        }
        return render_template('pages/show_artist.html', artist=data)
    else:
        error=True
        flash('An error ocurred.Artist does not exists!','error')
        return redirect(url_for('artists'))

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    # DONE: populate form with fields from artist with ID <artist_id>
    artist=Artist.query.get(artist_id)
    error=False
    if (artist==None):
        error=True
        flash("The artist id does not exists","error")
        return redirect(url_for('venues'))
    else:
        form = ArtistForm(obj=artist)
        return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    form=ArtistForm(request.form)
    artist=Artist.query.get(artist_id)
    try:
        form.populate_obj(artist)
        db.session.commit()
    except:
        flash("An error has occurred, Imposible to update the artist information","error")
    finally:
        db.session.close()
    # DONE: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue=Venue.query.get(venue_id)
    form = VenueForm(obj=venue)
    if venue!=None:
        return render_template('forms/edit_venue.html', form=form, venue=venue)
    else:
        flash("An Error has occurred. Impossible to update Venue at the moment")
        return redirect(url_for('venues'))
    
    # DONE: populate form with values from venue with ID <venue_id>
    


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # DONE: take values from the form submitted, and update existing
    form=VenueForm(request.form)
    try:
        venue=Venue.query.get(venue_id)
        form.populate_obj(venue)
        db.session.commit()
        return redirect(url_for('show_venue', venue_id=venue_id))
    except:
        flash("An error has occurred while updating the venue, please try again later","error")
        return redirect(url_for('venues'))
    finally:
        db.session.close()

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # DONE: insert form data as a new Venue record in the db, instead
    # DONE: modify data to be the data object returned from db insertion
    form = ArtistForm(request.form)
    artist = Artist(
        name = form.name.data, 
        city = form.city.data,
        state = form.state.data,
        phone= form.phone.data,
        genres= form.genres.data,
        facebook_link= form.facebook_link.data
    )
    try:
        db.session.add(artist)
        db.session.commit()
        # on successful db insert, flash success
        flash('Artist ' + artist.name + ' was successfully listed!')
    except:
        # DONE: on unsuccessful db insert, flash an error instead.
         flash('An error ocurred.Artist ' + artist.name+ 'could not be listed!','error')
    finally:
        db.session.close()
    
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # DONE: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    shows = Show.query.all()
    data = []
    for show in shows:
        data.append({
            "venue_id": show.id_venue,
            "venue_name":show.Venue.name,
            "artist_id":show.id_artist,
            "artist_name":show.Artist.name,
            "artist_image_link":show.Artist.image_link,
            "start_time":show.show_date.strftime("%m/%d/%Y, %H:%M")})
    
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # DONE: insert form data as a new Show record in the db, instead
    form = ShowForm(request.form)
    show = Show(
        id_venue = form.venue_id.data,
        id_artist = form.artist_id.data,
        show_date = form.start_time.data
    )
    print("La fecha es {}".format(show.show_date))
    try:
        db.session.add(show)
        db.session.commit()
        # on successful db insert, flash success
        flash('Show was successfully listed!')
    except:
        # DONE: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Show could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        flash('An error occurred. Show could not be listed.','error')
    finally:
        db.session.close()
    
    
    
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
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
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
