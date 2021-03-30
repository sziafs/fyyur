from flask import Blueprint

from artist import artists, search_artists, show_artist, edit_artist, edit_artist_submission, create_artist_form, create_artist_submission, delete_artist

artist_bp = Blueprint('artist_bp', __name__)

artist_bp.route('/', methods=['GET'])(artists)
artist_bp.route('/search', methods=['POST'])(search_artists)
artist_bp.route('/<int:artist_id>', methods=['GET'])(show_artist)
artist_bp.route('/create', methods=['GET'])(create_artist_form) 
artist_bp.route('/create', methods=['POST'])(create_artist_submission)
artist_bp.route('/<int:artist_id>/edit', methods=['GET'])(edit_artist)
artist_bp.route('/<int:artist_id>/edit', methods=['POST'])(edit_artist_submission)
artist_bp.route('/<int:artist_id>', methods=['POST'])(delete_artist)
