from core.errors import UserIdException
from app import User, db
from core.config import configs


def user_change_role(body_json):
    try:
        user = User.query.filter_by(id=body_json.get('id')).first()
    except Exception as e:
        print(e)
    if not user:
        raise UserIdException('invalid ID')
    else:
        try:
            roles = list(user.roles)
            new_role = body_json.get('role')

            if new_role not in configs.main.existing_roles:
                return 'Not allowed Role', None, None

            if new_role in roles:
                return 'Role already exists', user.login, user.roles

            roles.append(new_role)
            user.roles = roles
            db.session.commit()
            return 'User roles updated', user.login, user.roles
        except Exception as e:
            print(e)