from flask_jwt_extended import get_jwt
from flask import current_app

from core.errors import UserIdException
from database.db import db
from database.models import User
from core.config import configs
from performance.tracing.tracer import trace_it


@trace_it
def user_change_role(body_json: dict) -> dict:
    """
    Updates user's role
    Accepts user, target role and what to do with it
    """
    current_app.logger.info("Reading JWT")
    user_jwt = get_jwt()["userid"]

    current_app.logger.info("Searching for user in DB")
    user = User.get_user_by_id(id=user_jwt)

    current_app.logger.info("Assessing roles")
    if "admin" in user.roles or "superUser" in user.roles:
        user_id = body_json.get("id")
    else:
        return {"msg": "Haven't got permission"}

    user = User.get_user_by_id(id=user_id)

    if not user:
        current_app.logger.error("Invalid ID")
        raise UserIdException("invalid ID")
    else:
        current_app.logger.info("Updating roles")
        roles = list(user.roles)
        target_role = body_json.get("role")
        action = body_json.get("action_type")

        if action == "add":
            if (
                target_role not in configs.main.existing_roles
                or target_role == "superUser"
            ):
                return {"msg": "Not allowed Role"}

            if target_role in roles:
                return {"msg": "Role already exists"}

            roles.append(target_role)

        elif action == "delete":
            if (
                target_role in roles
                and target_role != "superUser"
                and target_role != "baseRole"
            ):
                roles.remove(target_role)
            else:
                return {"msg": "Delete is not allowed"}

        user.roles = roles
        db.session.commit()
        current_app.logger.info("Roles updated")
        return {"msg": "User roles updated", "user": user.login, "roles": user.roles}
