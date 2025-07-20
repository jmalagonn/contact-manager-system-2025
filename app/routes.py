"""Application routes for the contact manager."""

from flask import Blueprint, request, jsonify, abort
import bleach

from .services.contact_service import (
    create_contact as svc_create_contact,
    get_all_contacts,
)


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

    data = {
        "first_name": _clean(payload.get("first_name")),
        "last_name": _clean(payload.get("last_name")),
        "middle_name": _clean(payload.get("middle_name")),
        "country_code": _clean(payload.get("country_code")),
        "city_code": payload.get("city_code"),
        "phone_num": payload.get("phone_num"),
        "email": _clean(payload.get("email")),
    }

    if not all(
        [data["first_name"], data["last_name"], data["phone_num"], data["email"]]
    ):
        abort(400, "Missing required fields")

    contact = svc_create_contact(data)

    return jsonify(contact.to_dict()), 201


@main.route("/contacts", methods=["GET"])
def list_contacts():
    """Return all stored contacts."""
    contacts = get_all_contacts()
    return jsonify([c.to_dict() for c in contacts])


@main.route("/contacts/list", methods=["GET"])
def get_contacts():
    """Retrieve contacts from the database."""
    contacts = get_all_contacts()
    return jsonify([c.to_dict() for c in contacts])
