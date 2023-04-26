import json
from authlib.integrations.flask_client import OAuth
from flask import current_app

from routes.social import get_or_create_social_account, check_user_social


oauth = OAuth()


def register_oauth_apps(app) -> None:
    oauth.init_app(app)
    oauth.register(name='yandex')
    oauth.register(name='google',
                jwks_uri='https://www.googleapis.com/oauth2/v3/certs',
                userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo')


def oauth_google(provider):
    user_data = oauth.google.userinfo()
    social_account = check_user_social(provider, user_data['sub'])

    if not social_account:
        current_app.logger.info("Create new account")
        user = get_or_create_social_account(provider,
                                            social_id=user_data['sub'],
                                            first_name=user_data['given_name'],
                                            last_name=user_data['family_name'],
                                            email=user_data['email'])
    else:
        current_app.logger.info("Account already exists")
        user = social_account.user

    return user


def oauth_yandex(provider):
    user_data = json.loads(oauth.yandex.get('info').content)
    social_account = check_user_social(provider, user_data['id'])

    if not social_account:
        current_app.logger.info("Create new account")
        user = get_or_create_social_account(provider,
                                            social_id=user_data['id'],
                                            first_name=user_data['first_name'],
                                            last_name=user_data['last_name'],
                                            email=user_data['default_email'])
    else:
        current_app.logger.info("Account already exists")
        user = social_account.user

    return user