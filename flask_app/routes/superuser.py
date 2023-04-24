from core.errors import RegistrationException
from sqlalchemy.exc import IntegrityError
from database.db import db
from database.models import User
from flask import current_app
from performance.tracing.tracer import trace_it


@trace_it
def create_superuser(login, password):
    current_app.logger.info('Creating user instance')

    user = User(login=login,
                roles=['superUser'])

    user.set_password(password)

    try:
        db.session.add(user)
        db.session.commit()
        current_app.logger.info('User created')
    except IntegrityError:
        raise RegistrationException('User already exists')