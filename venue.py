import sys
from flask import render_template, redirect, url_for, request, flash, abort, jsonify
from flask_sqlalchemy_session import current_session

from models import Venue
from forms import VenueForm

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def venues():
    venues = Venue.query.all()
    data =[]
    for venue in venues:
        data.append({
        'city': venue.city,
        'state': venue.state,
        'venues': [{
            'id': venue.id,
            'name': venue.name,
            'num_upcoming_shows': '',
        }]
    })

    return render_template('pages/venues.html', areas=data);

def search_venues():
    search_term = request.form.get('search_term', '')
    response = Venue.query.filter(Venue.name.ilike('%' + search_term + '%'))
    results = {
        'count': response.count(),
        'data': response
    }

    return render_template('pages/search_venues.html', results=results, search_term=search_term)

def show_venue(venue_id):
    venue = Venue.query.get(venue_id)
    data = {
        'id': venue.id,
        'name': venue.name,
        'genres': venue.genres,
        'address': venue.address,
        'city': venue.city, 
        'state': venue.state,
        'phone': venue.phone,
        'website': venue.website,
        'facebook_link': venue.facebook_link,
        'image_link': venue.image_link,
        'seeking_talent': venue.seeking_talent,
        'seeking_description': venue.seeking_description,
        'past_shows': [{
            'artist_id': 4,
            'artist_name': 'Guns N Petals',
            'artist_image_link': 'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80',
            'start_time': '2019-05-21T21:30:00.000Z'
        }],
        'upcoming_shows': [],
        'past_shows_count': 1,
        'upcoming_shows_count': 0,
    }

    return render_template('pages/show_venue.html', venue=data)

def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

def create_venue_submission():
    if request.form.get('seeking_talent') == 'y':
        seeking_talent = True
    else:
        seeking_talent = False

    venue = Venue(
        name=request.form.get('name'),
        city=request.form.get('city'),
        state=request.form.get('state'),
        address=request.form.get('address'),
        phone=request.form.get('phone'),
        genres=request.form.getlist('genres'),
        facebook_link=request.form.get('facebook_link'),
        image_link=request.form.get('image_link'),
        website=request.form.get('website'),
        seeking_talent=seeking_talent,
        seeking_description=request.form.get('seeking_description'),
    )

    try:
        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully added!')
    except:
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be added.')
    finally:
        db.session.close()
        
    return render_template('pages/home.html')

def edit_venue(venue_id):
    venue =Venue.query.get(venue_id)

    form = VenueForm()
    form.name.default = venue.name
    form.city.default = venue.city
    form.state.default = venue.state
    form.address.default = venue.address
    form.phone.default = venue.phone
    form.genres.default = venue.genres
    form.facebook_link.default = venue.facebook_link
    form.image_link.default = venue.image_link
    form.website_link.default = venue.website
    form.seeking_talent.default = venue.seeking_talent
    form.seeking_description.default = venue.seeking_description
    form.process()

    return render_template('forms/edit_venue.html', form=form, venue=venue)

def edit_venue_submission(venue_id):
    if request.form.get('seeking_talent') == 'y':
        seeking_talent = True
    else:
        seeking_talent = False

    venue = Venue.query.get(venue_id)

    try:
        venue.name = request.form.get('name', venue.name)
        venue.city = request.form.get('city')
        venue.state = request.form.get('state')
        venue.address = request.form.get('address')
        venue.phone = request.form.get('phone')
        venue.genres = request.form.getlist('genres')
        venue.facebook_link = request.form.get('facebook_link')
        venue.image_link = request.form.get('image_link')
        venue.website_link = request.form.get('website_link')
        venue.seeking_talent = seeking_talent
        venue.seeking_description = request.form.get('seeking_description')

        db.session.merge(venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully updated!')
    except:
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
    finally:
        db.session.close()

    return redirect(url_for('venue_bp.show_venue', venue_id=venue_id))

def delete_venue(venue_id):
    try:
        venue = Venue.query.filter_by(id=venue_id).first_or_404()
        current_session = db.object_session(venue)
        current_session.delete(venue)
        current_session.commit()
        db.session.delete(venue)
        db.session.commit()
        flash('This venue was successfully deleted!')
        return render_template('pages/home.html')
    except:
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. This venue could not be deleted.')
    finally:
        db.session.close()
    
    return redirect(url_for('venue_bp.venues'))
