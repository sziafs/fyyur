from flask import Blueprint

from show import shows, create_shows, create_show_submission

show_bp = Blueprint('show_bp', __name__)

show_bp.route('/', methods=['GET'])(shows)
show_bp.route('/create', methods=['GET'])(create_shows)
show_bp.route('/create', methods=['POST'])(create_show_submission)
