"""Business logic for contact operations."""

from .. import db
from ..models import Contact


def create_contact(data, user_id: int):
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
        user_id=user_id,
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


def get_all_contacts_by_user(user_id: int):
    """Return contacts belonging to a specific user."""
    return Contact.query.filter_by(user_id=user_id).all()


def get_contact_by_id_for_user(contact_id: int, user_id: int) -> Contact | None:
    """Fetch a contact by id ensuring it belongs to the given user."""
    return Contact.query.filter_by(id=contact_id, user_id=user_id).first()
