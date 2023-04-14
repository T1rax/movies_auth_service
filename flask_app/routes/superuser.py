from core.errors import RegistrationException
from sqlalchemy.exc import IntegrityError
from database.db import db
from database.models import User


def create_superuser(login, password):
    user = User(login=login,
                roles=['superUser'])

    user.set_password(password)

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        raise RegistrationException('User already exists')

    return user