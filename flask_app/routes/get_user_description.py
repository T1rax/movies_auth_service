from core.errors import UserIdException
from app import User


def user_description(body_json):
    user = User.query.filter_by(id=body_json.get('id')).first()

    print(1111111111, user)

    if not user:
        raise UserIdException('invalid ID')
    else:
        return {
            'id': user.id,
            'first_name': user.first_name,
            'login': user.login,
            'roles': user.roles,
        }