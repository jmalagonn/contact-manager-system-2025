from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """Database model for application users."""

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    contacts = db.relationship("Contact", backref="user", lazy=True)

    def set_password(self, password: str) -> None:
        """Hash and store a new password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify a password against the stored hash."""
        return check_password_hash(self.password_hash, password)


class Contact(db.Model):
    """Database model for storing contacts."""

    __tablename__ = "contact"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    middle_name = db.Column(db.String(20))
    country_code = db.Column(db.String(10))
    city_code = db.Column(db.Integer)
    phone_num = db.Column(db.BigInteger, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "middle_name": self.middle_name,
            "country_code": self.country_code,
            "city_code": self.city_code,
            "phone_num": self.phone_num,
            "email": self.email,
        }

