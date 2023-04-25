from authlib.integrations.flask_client import OAuth
from core.config import configs


oauth = OAuth()


def register_oauth_apps(app) -> None:
    register_google_oauth()
    oauth.init_app(app)


def register_google_oauth() -> None:
    oauth.register(
        name='google',
        client_id=configs.oauth.google.client_id,
        client_secret=configs.oauth.google.secret,
        access_token_url='https://oauth2.googleapis.com/token',
        access_token_params=None,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
        client_kwargs={'scope': 'openid email profile'},
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
    )