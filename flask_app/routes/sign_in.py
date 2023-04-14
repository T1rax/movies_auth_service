from core.errors import LoginException
from database.models import User
from routes.sign_in_history import add_history


def login_user(request):
    body_json = request.get_json()
    user = User.query.filter_by(login=body_json.get('login')).first()
    if not user:
        raise LoginException('invalid login')
    else:
        pswd = user.check_password(body_json.get('password'))

    if not pswd:
        raise LoginException('invalid password')
    else:
        add_history(request, user.id, 'login')
        return user




