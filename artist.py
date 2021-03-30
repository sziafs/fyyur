import sys
from flask import render_template, redirect, url_for, request, flash

from models import Artist, Venue, Show
from forms import ArtistForm, datetime

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def artists():
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)

def search_artists():
    search_term = request.form.get('search_term', '')
    response = Artist.query.filter(Artist.name.ilike('%' + search_term + '%'))
    results = {
        'count': response.count(),
        'data': response
    }

    return render_template('pages/search_artists.html', results=results, search_term=search_term)

def get_shows(shows):
    data = []
    for show in shows:
        venue = Venue.query.get(show.artist_id)
        data.append({
            "venue_id": venue.id,
            "venue_name": venue.name,
            "venue_image_link": venue.image_link,
            "start_time": show.start_time.strftime('%m/%d/%Y')
        })
    return data

def show_artist(artist_id):
    artist = Artist.query.get(artist_id)
    current_time = datetime.now().strftime('%m/%d/%Y')

    past_shows= Show.query.filter_by(artist_id=artist_id).filter(Show.start_time <= current_time)
    past_shows_data = get_shows(past_shows)

    upcoming_shows= Show.query.filter_by(artist_id=artist_id).filter(Show.start_time > current_time)
    upcoming_shows_data = get_shows(upcoming_shows)

    data = {
        'id': artist.id,
        'name': artist.name,
        'genres': artist.genres,
        'city': artist.city,
        'state': artist.state,
        'phone': artist.phone,
        'website': artist.website,
        'facebook_link': artist.facebook_link,
        'image_link': artist.image_link,
        'seeking_venue': artist.seeking_venue,
        'seeking_description': artist.seeking_description,
        'past_shows': past_shows_data,
        'upcoming_shows': upcoming_shows_data,
        'past_shows_count': past_shows.count(),
        'upcoming_shows_count': upcoming_shows.count(),
    }
    
    return render_template('pages/show_artist.html', artist=data)

def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

def create_artist_submission():
    if request.form.get('seeking_venue') == 'y':
        seeking_venue = True
    else:
        seeking_venue = False

    artist = Artist(
        name=request.form.get('name'),
        city=request.form.get('city'),
        state=request.form.get('state'),
        phone=request.form.get('phone'),
        genres=request.form.getlist('genres'),
        facebook_link=request.form.get('facebook_link'),
        image_link=request.form.get('image_link'),
        website=request.form.get('website'),
        seeking_venue=seeking_venue,
        seeking_description=request.form.get('seeking_description'),
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
    form.genres.default = artist.genres
    form.facebook_link.default = artist.facebook_link
    form.image_link.default = artist.image_link
    form.website_link.default = artist.website
    form.seeking_venue.default = artist.seeking_venue
    form.seeking_description.default = artist.seeking_description
    form.process()

    return render_template('forms/edit_artist.html', form=form, artist=artist)

def edit_artist_submission(artist_id):
    if request.form.get('seeking_venue') == 'y':
        seeking_venue = True
    else:
        seeking_venue = False

    artist = Artist.query.get(artist_id)

    try:
        artist.name = request.form.get('name')
        artist.city = request.form.get('city')
        artist.state = request.form.get('state')
        artist.phone = request.form.get('phone')
        artist.genres = request.form.getlist('genres')
        artist.facebook_link = request.form.get('facebook_link')
        artist.image_link = request.form.get('image_link')
        artist.website_link = request.form.get('website_link')
        artist.seeking_venue = seeking_venue
        artist.seeking_description = request.form.get('seeking_description')
        
        db.session.merge(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully updated!')
    except:
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
    finally:
        db.session.close()

    return redirect(url_for('artist_bp.show_artist', artist_id=artist_id))

def delete_artist(artist_id):
    try:
        artist = Artist.query.filter_by(id=artist_id).first_or_404()
        current_session = db.object_session(artist)
        current_session.delete(artist)
        current_session.commit()
        db.session.delete(artist)
        db.session.commit()
        flash('This artist was successfully deleted!')
        return render_template('pages/home.html')
    except:
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. This artist could not be deleted.')
    finally:
        db.session.close()
    
    return redirect(url_for('artist_bp.artists'))
