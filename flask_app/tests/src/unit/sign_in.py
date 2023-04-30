from pytest_mock import mocker
from app import app
from blueprints.v1.basic_endpoints.core_endpoints import sign_in
import flask


def test_sign_in_route(mocker, generate_fake_user):
    request = {'login': 'test_user', 'password':'123qwer'}

    fake_user = generate_fake_user
    fake_user.login = request['login']
    fake_user.password = request['password']

    request_mock = mocker.patch.object(flask, 'request')
    request_mock.return_value = request
    
    mock_login_user = mocker.patch("blueprints.basic_endpoints.login_user")
    mock_login_user.return_value = fake_user

    mock_jwt_helper = mocker.patch("blueprints.basic_endpoints.jwt_helper")
    mock_jwt_helper.user_id = fake_user.id
    mock_jwt_helper.create_tokens = None
    mock_jwt_helper.set_tokens = None

    with app.app_context():
        response, status_code = sign_in()

    assert status_code == 200