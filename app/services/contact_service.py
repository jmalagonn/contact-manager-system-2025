"""Business logic for contact operations."""

from .. import db
from ..models import Contact


def create_contact(data):
    """Create and persist a new contact.

    Parameters
    ----------
    data: dict
        Dictionary with keys matching ``Contact`` fields. Required keys are
        ``first_name``, ``last_name``, ``phone_num`` and ``email``.

    Returns
    -------
    Contact
        The newly created ``Contact`` instance.
    """
    contact = Contact(
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        middle_name=data.get("middle_name"),
        country_code=data.get("country_code"),
        city_code=data.get("city_code"),
        phone_num=data.get("phone_num"),
        email=data.get("email"),
    )

    db.session.add(contact)
    db.session.commit()

    return contact


def get_all_contacts():
    """Return all contacts from the database."""
    return Contact.query.all()
