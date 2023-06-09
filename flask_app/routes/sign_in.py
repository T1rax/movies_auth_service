from core.errors import LoginException
from database.models import User
from routes.sign_in_history import add_history
from performance.tracing.tracer import trace_it
from flask import current_app, Request


@trace_it
def login_user(request: Request) -> User:
    """
    Checks provided ligon in password in database
    If succeeds, returns user object and adds ligon to history
    """
    body_json = request.get_json()

    current_app.logger.info("Looking for user in DB")
    user = User.get_user_by_universal_login(login=body_json.get("login"))
    if not user:
        current_app.logger.error("invalid login")
        raise LoginException("invalid login")
    else:
        current_app.logger.info("Checking password")
        pswd = user.check_password(body_json.get("password"))

    if not pswd:
        current_app.logger.error("invalid password")
        raise LoginException("invalid password")
    else:
        current_app.logger.info("Adding login to user history")
        add_history(request, user.id, "login")
        return user
