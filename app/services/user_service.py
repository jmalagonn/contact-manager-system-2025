from .. import db
from ..models import User


def create_user(username: str, password: str) -> User:
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def get_user_by_username(username: str) -> User | None:
    return User.query.filter_by(username=username).first()
