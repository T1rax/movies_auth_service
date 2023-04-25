import sys
sys.path.insert(0, '/home/tirax/movies_auth_service/flask_app')
sys.path.insert(0, '/home/seo/proj/sprint_7/movies_auth_service/flask_app')

from flask import Flask
from flask_migrate import Migrate
from authlib.integrations.flask_client import OAuth

from database.db import db
from core.oauth import oauth

from blueprints.basic_endpoints import blueprint as basic_endpoints
from blueprints.basic_endpoints.swagger import swaggerui_blueprint
from core.flask_configuration import set_flask_configuration
from core.logger import set_up_logging
from encryption.jwt import create_jwt
from performance.requests_limit.rpm import set_rpm_limit
from performance.tracing.tracer import configure_tracer
from core.swagger.openapi import register_docs


set_up_logging()

app = Flask(__name__)
app.secret_key = 'secret key for oauth'
app.register_blueprint(basic_endpoints)
app.register_blueprint(swaggerui_blueprint) 

set_flask_configuration(app)

# bootstrap database migrate commands
db.init_app(app)
migrate = Migrate(app, db)

# Encryption
jwt = create_jwt(app)

# Performance logging 
set_rpm_limit(app)
configure_tracer(app)

# Documentation
register_docs(app)

# Registry OAuth
oauth.init_app(app)


if __name__ == '__main__':
    app.run()
