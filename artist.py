import sys
from flask import render_template, redirect, url_for, request, flash

from models import Artist
from forms import ArtistForm

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def artists():
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)

def search_artists():
    search_term = request.form.get('search_term', '')
    response = Artist.query.filter(Artist.name.ilike('%' + search_term + '%'))
    results = {
        "count": response.count(),
        "data": response
    }

    return render_template('pages/search_artists.html', results=results, search_term=search_term)

def show_artist(artist_id):
    artist = Artist.query.get(artist_id)
    data={
        "id": artist.id,
        "name": artist.name,
        "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": artist.facebook_link,
        "image_link": artist.image_link,
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "past_shows": [{
            "venue_id": 1,
            "venue_name": "The Musical Hop",
            "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
            "start_time": "2019-05-21T21:30:00.000Z"
        }],
        "upcoming_shows": [],
        "past_shows_count": 1,
        "upcoming_shows_count": 0,
    }
    
    return render_template('pages/show_artist.html', artist=data)

def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

def create_artist_submission():
    artist = Artist(
        name=request.form.get('name'),
        city=request.form.get('city'),
        state=request.form.get('state'),
        phone=request.form.get('phone'),
        image_link=request.form.get('image_link'),
        facebook_link=request.form.get('facebook_link'),
    )

    try:
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully added!')
    except:
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be added.')
    finally:
        db.session.close()

    return render_template('pages/home.html')

def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)
    
    form = ArtistForm()
    form.name.default = artist.name
    form.city.default = artist.city
    form.state.default = artist.state
    form.phone.default = artist.phone
    form.image_link.default = artist.image_link
    form.facebook_link.default = artist.facebook_link
    form.process()

    return render_template('forms/edit_artist.html', form=form, artist=artist)

def edit_artist_submission(artist_id):
    artist = Artist.query.get(artist_id)

    try:
        artist.name = request.form.get('name')
        artist.city = request.form.get('city')
        artist.state = request.form.get('state')
        artist.phone = request.form.get('phone')
        artist.image_link = request.form.get('image_link')
        artist.facebook_link = request.form.get('facebook_link')
        
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully updated!')
    except:
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
    finally:
        db.session.close()

    return redirect(url_for('artist_bp.show_artist', artist_id=artist_id))


