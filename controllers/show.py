import sys
from flask import render_template, request, flash

from models.models import Show, Venue, Artist
from forms import ShowForm, datetime

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def shows():
  shows = Show.query.all()
  data = []
  for show in shows:
    data.append({
      "venue_id": show.venue_id,
      "venue_name": Venue.query.get(show.venue_id).name,
      "artist_id": show.artist_id,
      "artist_name": Artist.query.get(show.artist_id).name,
      "artist_image_link": Artist.query.get(show.artist_id).image_link,
      "start_time": show.start_time.strftime('%m/%d/%Y')
    })

  return render_template('pages/shows.html', shows=data)

def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

def create_show_submission():
  show = Show(
    artist_id=request.form.get('artist_id'),
    venue_id=request.form.get('venue_id'),
    start_time=datetime.strptime(request.form.get('start_time'), '%Y-%m-%d %H:%M:%S')
  )

  try:  
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully added!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Show could not be added.')
  finally:
    db.session.close()

  return render_template('pages/home.html')