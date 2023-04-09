from core.errors import RegistrationException
from sqlalchemy.exc import IntegrityError
from app import db
from app import User


def register_user(body_json):

    print(body_json)

    # with app.app_context():
    #     db.create_all()

    user = User(login=body_json.get('login'), 
                password=body_json.get('password'), 
                first_name=body_json.get('first_name'), 
                last_name=body_json.get('last_name'), 
                roles=['basicRole'])

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        raise RegistrationException('User already exists')

    return user

    # raise RegistrationException('User already exists')