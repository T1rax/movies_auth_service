from flask_swagger_ui import get_swaggerui_blueprint


swaggerui_blueprint = get_swaggerui_blueprint(
    "/auth/swagger",  # swagger url
    "http://127.0.0.1/auth/swagger.json",  # api url
    config={"app_name": "Sample API"},
)
