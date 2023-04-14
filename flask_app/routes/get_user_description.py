from flask_jwt_extended import get_jwt

from core.errors import UserIdException
from database.models import User


def user_description(body_json):
    user_jwt = get_jwt()['userid']
    user = User.query.filter_by(id=user_jwt).first()
    if 'admin' in user.roles or 'superUser' in user.roles:
        user_id = body_json.get('id')
    else:
        user_id = get_jwt()['userid']

    user = User.query.filter_by(id=user_id).first()

    if not user:
        raise UserIdException('invalid ID')
    else:
        return {
            'id': user.id,
            'first_name': user.first_name,
            'login': user.login,
            'roles': user.roles,
        }