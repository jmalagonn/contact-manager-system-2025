from . import db


class Contact(db.Model):
    """Database model for storing contacts."""

    __tablename__ = "contact"

    id = db.Column(db.Integer, primary_key=True)
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
            "first_name": self.first_name,
            "last_name": self.last_name,
            "middle_name": self.middle_name,
            "country_code": self.country_code,
            "city_code": self.city_code,
            "phone_num": self.phone_num,
            "email": self.email,
        }

