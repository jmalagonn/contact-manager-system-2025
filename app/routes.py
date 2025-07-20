"""Application routes for the contact manager."""

from flask import Blueprint, request, jsonify, abort
import bleach

from . import db
from .models import Contact


main = Blueprint("main", __name__)


def _clean(value):
    """Sanitize incoming strings."""
    if value is None:
        return None
    return bleach.clean(str(value), strip=True)


@main.route("/contacts", methods=["POST"])
def create_contact():
    """Create a new contact."""
    payload = request.get_json(force=True, silent=True) or {}

    first_name = _clean(payload.get("first_name"))
    last_name = _clean(payload.get("last_name"))
    middle_name = _clean(payload.get("middle_name"))
    country_code = _clean(payload.get("country_code"))
    city_code = payload.get("city_code")
    phone_num = payload.get("phone_num")
    email = _clean(payload.get("email"))

    if not all([first_name, last_name, phone_num, email]):
        abort(400, "Missing required fields")

    contact = Contact(
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        country_code=country_code,
        city_code=city_code,
        phone_num=phone_num,
        email=email,
    )

    db.session.add(contact)
    db.session.commit()

    return jsonify(contact.to_dict()), 201


@main.route("/contacts", methods=["GET"])
def list_contacts():
    """Return all stored contacts."""
    contacts = Contact.query.all()
    return jsonify([c.to_dict() for c in contacts])

