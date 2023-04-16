import sys
sys.path.insert(0, '/home/tirax/movies_auth_service/flask_app')
sys.path.insert(0, '/home/seo/proj/sprint_7/movies_auth_service/flask_app')

from flask import Flask
from flask_migrate import Migrate

from database.db import db

from blueprints.basic_endpoints import blueprint as basic_endpoints
from blueprints.basic_endpoints.swagger import swaggerui_blueprint
from core.flask_configuration import set_flask_configuration
from core.logger import set_up_logging
from encryption.jwt import create_jwt
from core.swagger.openapi import register_docs, spec


set_up_logging()

app = Flask(__name__)
app.register_blueprint(basic_endpoints)
app.register_blueprint(swaggerui_blueprint) 

set_flask_configuration(app)

# bootstrap database migrate commands
db.init_app(app)
migrate = Migrate(app, db)

# swagger = Swagger(app)
jwt = create_jwt(app)

register_docs(app)


if __name__ == '__main__':
    app.run()
