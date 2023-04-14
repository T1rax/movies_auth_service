from core.errors import LoginException
from database.models import User


def login_user(body_json):
    user = User.query.filter_by(login=body_json.get('login')).first()
    if not user:
        raise LoginException('invalid login')
    else:
        pswd = user.check_password(body_json.get('password'))

    if not pswd:
        raise LoginException('invalid password')
    else:
        print(111111111111111, user.id)
        return user

