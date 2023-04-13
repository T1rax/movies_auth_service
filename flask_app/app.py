import sys
sys.path.insert(0, '/home/tirax/movies_auth_service/flask_app')

from flask import Flask
from flask_migrate import Migrate

from database.db import db

from blueprints.basic_endpoints import blueprint as basic_endpoints
from core.flask_configuration import set_flask_configuration
from encryption.jwt import create_jwt


app = Flask(__name__)
app.register_blueprint(basic_endpoints)

set_flask_configuration(app)

# bootstrap database migrate commands
db.init_app(app)
migrate = Migrate(app, db)

# swagger = Swagger(app)
jwt = create_jwt(app)


if __name__ == '__main__':
    app.run()
