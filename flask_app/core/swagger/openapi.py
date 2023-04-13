from apispec import APISpec
from apispec_webframeworks.flask import FlaskPlugin
from apispec_fromfile import FromFilePlugin

import blueprints.basic_endpoints as bp
import json


spec = APISpec(
    title="Movies Auth Service",
    version="0.0.1",
    openapi_version="3.0.2",
    info=dict(description="Auth API"),
    servers=[
        dict(
            description="localhost",
            url="http://127.0.0.1"
            )
        ],
    tags=[
        dict(
            name="Authentification",
            description="Endpoints related to Authentification"
            ),
        dict(
            name="Tokens",
            description="Token-related routes"
            ),
        dict(
            name="Roles",
            description="Roles routes"
            ),
        dict(
            name="Additional",
            description="Other routes"
            ),
        ],
    plugins=[FlaskPlugin(), FromFilePlugin()],
)

def register_docs(app):

    with app.test_request_context():
        # Account authorization routes
        spec.path(view=bp.authorize)
        spec.path(view=bp.logout)
        spec.path(view=bp.sign_in)
        spec.path(view=bp.sign_up)

        # Token-related routes
        spec.path(view=bp.refresh)

        # Roles routes
        spec.path(view=bp.change_role)

        # Additional routes
        spec.path(view=bp.get_user_description)
        spec.path(view=bp.sign_in_history)

    with open('core/swagger/swagger.json', 'w') as f:
        json.dump(spec.to_dict(), f)