from core.errors import LoginException
from database.models import User
from routes.sign_in_history import add_history
from flask import current_app


def login_user(request):
    body_json = request.get_json()

    current_app.logger.info('Looking for user in DB')
    user = User.query.filter_by(login=body_json.get('login')).first()
    if not user:
        current_app.logger.error('invalid login')
        raise LoginException('invalid login')
    else:
        current_app.logger.info('Checking password')
        pswd = user.check_password(body_json.get('password'))

    if not pswd:
        current_app.logger.error('invalid password')
        raise LoginException('invalid password')
    else:
        current_app.logger.info('Adding login to user history')
        add_history(request, user.id, 'login')
        return user




