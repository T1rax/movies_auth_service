from flask import Blueprint, jsonify, current_app
import json
from http import HTTPStatus
from flask_swagger_ui import get_swaggerui_blueprint


swaggerui_blueprint = get_swaggerui_blueprint(
    "/auth/swagger",  # swagger url
    "http://127.0.0.1/auth/swagger.json",  # api url
    config={"app_name": "Sample API"},
)

blueprint = Blueprint("swagger", __name__)

# Documentation
@blueprint.route("/swagger.json")
def swagger():
    try:
        with open("core/swagger/swagger.json", "r") as f:
            return jsonify(json.load(f))
    except Exception as e:
        current_app.logger.error(e)
        return (
            jsonify({"msg": "Internal server error"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
