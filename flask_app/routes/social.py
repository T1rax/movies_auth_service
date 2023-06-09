from core.errors import RegistrationException
from sqlalchemy.exc import IntegrityError
from database.db import db
from database.models import User, SocialAccount
from flask import current_app
from performance.tracing.tracer import trace_it


@trace_it
def get_or_create_social_account(
    provider: str, social_id: str, first_name: str, last_name: str, email: str = None
) -> User:
    """
    Checks in database for social account
    If account is now found, creates it
    If user was not registered before, registers them
    After success returns filled user object
    """
    if email:
        login = email.split("@")[0]
    else:
        login = "_".join(first_name.lower(), last_name.lower())

    user = User.get_user_by_universal_login(email=email, login=login)

    if not user:
        user = User(
            login=login, first_name=first_name, last_name=last_name, roles=["basicRole"]
        )

        user.set_password(User.generate_random_string())

        try:
            db.session.add(user)
            db.session.commit()
            current_app.logger.info("User registered in DB")
        except IntegrityError:
            current_app.logger.error("User already exists")
            raise RegistrationException("User already exists")

    social = SocialAccount(provider=provider, social_id=social_id, user=user)

    try:
        db.session.add(social)
        db.session.commit()
        current_app.logger.info("Created social account")
    except IntegrityError:
        current_app.logger.error("User already exists")
        raise RegistrationException("User already exists")

    return user


@trace_it
def check_user_social(provider: str, social_id: str) -> SocialAccount:
    """
    Looks in database for user's social account
    Returns filled social account object
    """
    return SocialAccount.get_user_social(provider, social_id)
