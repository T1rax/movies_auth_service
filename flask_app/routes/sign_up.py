from core.errors import RegistrationException
from sqlalchemy.exc import IntegrityError
from database.db import db
from database.models import User


def register_user(body_json):
    user = User(login=body_json.get('login'),
                first_name=body_json.get('first_name'),
                last_name=body_json.get('last_name'), 
                roles=['basicRole'])

    user.set_password(body_json.get('password'))

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        raise RegistrationException('User already exists')

    return user