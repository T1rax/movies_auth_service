from core.errors import UserIdException
from database.models import User


def user_description(body_json):
    user = User.query.filter_by(id=body_json.get('id')).first()

    if not user:
        raise UserIdException('invalid ID')
    else:
        return {
            'id': user.id,
            'first_name': user.first_name,
            'login': user.login,
            'roles': user.roles,
        }