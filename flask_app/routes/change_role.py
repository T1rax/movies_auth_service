from core.errors import UserIdException
from app import User, db


def user_change_role(body_json):
    try:
        user = User.query.filter_by(id=body_json.get('id')).first()
    except Exception as e:
        print(e)
    if not user:
        raise UserIdException('invalid ID')
    else:
        try:
            roles = user.roles
            roles.append(body_json.get('role'))
            print(roles)

            user.roles = roles
            db.session.commit()
            return user.login
        except Exception as e:
            print(e)