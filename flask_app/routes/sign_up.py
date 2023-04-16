from core.errors import RegistrationException
from sqlalchemy.exc import IntegrityError
from database.db import db
from database.models import User
from flask import current_app


def register_user(body_json):
    current_app.logger.info('Creating user instance')
    user = User(login=body_json.get('login'),
                first_name=body_json.get('first_name'),
                last_name=body_json.get('last_name'), 
                roles=['basicRole'])

    current_app.logger.info('Encoding password')
    user.set_password(body_json.get('password'))

    try:
        db.session.add(user)
        db.session.commit()
        current_app.logger.info('User registered in DB')
    except IntegrityError:
        current_app.logger.error('User already exists')
        raise RegistrationException('User already exists')

    return user