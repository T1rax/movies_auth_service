from flask import Flask
from flask_migrate import Migrate

from database.db import db
from core.oauth import register_oauth_apps

from blueprints.v1.basic_endpoints.core_endpoints import blueprint as basic_endpoints_v1
from blueprints.v1.bash_endpoints.users import blueprint as bash_endpoints_v1
from blueprints.v1.basic_endpoints.swagger import swaggerui_blueprint
from blueprints.v1.basic_endpoints.swagger import blueprint as swagger_json_blueprint
from core.flask_configuration import set_flask_configuration
from core.logger import set_up_logging
from core.config import configs
from encryption.jwt import create_jwt
from performance.requests_limit.rpm import set_rpm_limit
from performance.tracing.tracer import configure_tracer
from core.swagger.openapi import register_docs


set_up_logging()

app = Flask(__name__)

# Set App variables
set_flask_configuration(app)

# Blueprints
app.register_blueprint(basic_endpoints_v1, url_prefix="/auth/v1")
app.register_blueprint(bash_endpoints_v1)
app.register_blueprint(swagger_json_blueprint, url_prefix="/auth")
app.register_blueprint(swaggerui_blueprint)

# Registry OAuth
register_oauth_apps(app)

# bootstrap database migrate commands
db.init_app(app)
migrate = Migrate(app, db)

# Encryption
jwt = create_jwt(app)

# Performance logging
if configs.rpm.need_to_launch:
    set_rpm_limit(app)

if configs.tracing.need_to_launch:
    configure_tracer(app)

# Documentation
register_docs(app)


if __name__ == "__main__":
    app.run()
