from core.errors import UserIdException
from database.db import db
from database.models import User
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
            target_role = body_json.get('role')
            action = body_json.get('action_type')

            if action == 'add':
                if target_role not in configs.main.existing_roles or target_role == 'superUser':
                    return {"msg":'Not allowed Role'}

                if target_role in roles:
                    return {"msg":'Role already exists'}

                roles.append(target_role)

            elif action == 'delete':
                if target_role in roles and target_role != 'superUser' and target_role != 'baseRole':
                    roles.remove(target_role)
                else:
                    return {"msg": 'Delete is not allowed'}

            user.roles = roles
            db.session.commit()
            return {"msg":'User roles updated', "user":user.login, "roles":user.roles}
        except Exception as e:
            print(e)