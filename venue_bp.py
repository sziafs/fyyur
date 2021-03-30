from flask import Blueprint

from venue import venues, search_venues, show_venue, create_venue_form, create_venue_submission, edit_venue, edit_venue_submission, delete_venue

venue_bp = Blueprint("venue_bp", __name__)

venue_bp.route("/", methods=["GET"])(venues)
venue_bp.route("/search", methods=["POST"])(search_venues)
venue_bp.route("/<int:venue_id>", methods=["GET"])(show_venue)
venue_bp.route("/create", methods=["GET"])(create_venue_form)
venue_bp.route("/create", methods=["POST"])(create_venue_submission)
venue_bp.route("/<int:venue_id>/edit", methods=["GET"])(edit_venue)
venue_bp.route("/<int:venue_id>/edit", methods=["POST"])(edit_venue_submission)
venue_bp.route("/<venue_id>", methods=["DELETE"])(delete_venue)
