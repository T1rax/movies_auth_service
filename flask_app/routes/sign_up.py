from core.errors import RegistrationException
from sqlalchemy.exc import IntegrityError
from database.db import db
from database.models import User
from performance.tracing.tracer import trace_it
from routes.sign_in_history import add_history
from flask import current_app


@trace_it
def register_user(request):
    body_json = request.get_json()
    current_app.logger.info('Creating user instance')
    user = User(login=body_json.get('login'),
                first_name=body_json.get('first_name'),
                last_name=body_json.get('last_name'), 
                roles=['basicRole'])

    current_app.logger.info('Encoding password')
    user.set_password(body_json.get('password'))

    current_app.logger.info('Checking if age provided')
    if body_json.get('age_group') is not None:
        user.age_group = body_json.get('age_group')

    try:
        db.session.add(user)
        db.session.commit()
        current_app.logger.info('User registered in DB')
    except IntegrityError:
        current_app.logger.error('User already exists')
        raise RegistrationException('User already exists')
    finally:
        current_app.logger.info('Adding login to user history')
        add_history(request, user.id, 'login')

    return user