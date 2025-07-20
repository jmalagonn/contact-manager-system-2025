"""Application routes for the contact manager."""

from flask import Blueprint, request, jsonify, abort, session, g
from functools import wraps
import bleach

from .services.contact_service import (
    create_contact as svc_create_contact,
    get_all_contacts_by_user,
    get_contact_by_id_for_user,
)
from .services.user_service import create_user, get_user_by_username


main = Blueprint("main", __name__)


def login_required(func):
    """Ensure a user is authenticated before accessing the route."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id")
        if not user_id:
            abort(401, "Login required")
        g.user_id = user_id
        return func(*args, **kwargs)

    return wrapper


def _clean(value):
    """Sanitize incoming strings."""
    if value is None:
        return None
    return bleach.clean(str(value), strip=True)


@main.route("/register", methods=["POST"])
def register():
    """Register a new user and start a session."""
    payload = request.get_json(force=True, silent=True) or {}
    username = _clean(payload.get("username"))
    password = payload.get("password")

    if not username or not password:
        abort(400, "Missing username or password")

    if get_user_by_username(username):
        abort(400, "Username already exists")

    user = create_user(username, password)
    session["user_id"] = user.id
    return jsonify({"message": "registered"}), 201


@main.route("/login", methods=["POST"])
def login():
    """Authenticate a user."""
    payload = request.get_json(force=True, silent=True) or {}
    username = _clean(payload.get("username"))
    password = payload.get("password")

    if not username or not password:
        abort(400, "Missing credentials")

    user = get_user_by_username(username)
    if not user or not user.check_password(password):
        abort(401, "Invalid credentials")

    session["user_id"] = user.id
    return jsonify({"message": "logged in"})


@main.route("/logout", methods=["POST"])
@login_required
def logout():
    """End the current user session."""
    session.pop("user_id", None)
    return jsonify({"message": "logged out"})


@main.route("/contacts", methods=["POST"])
@login_required
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

    contact = svc_create_contact(data, g.user_id)

    return jsonify(contact.to_dict()), 201





@main.route("/contacts/list", methods=["GET"])
@login_required
def get_contacts():
    """Retrieve contacts from the database."""
    contacts = get_all_contacts_by_user(g.user_id)
    return jsonify([c.to_dict() for c in contacts])


@main.route("/contacts/<int:contact_id>", methods=["GET"])
@login_required
def get_contact(contact_id: int):
    """Retrieve a single contact belonging to the logged in user."""
    contact = get_contact_by_id_for_user(contact_id, g.user_id)
    if not contact:
        abort(404, "Contact not found")
    return jsonify(contact.to_dict())
