from authlib.integrations.flask_client import OAuth

oauth = OAuth()


oauth.register(
    name='google',
    client_id='109695332650-15l1hiljbtf6l5u8krj80fvu7a9hcfm0.apps.googleusercontent.com',
    client_secret='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',
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)