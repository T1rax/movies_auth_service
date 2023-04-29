from pytest_mock import mocker
from app import app
from routes.authorize import authorize_user


def test_authorize_route_func():
    jwt_token = {
        'first_name': 'Ivan',
        'last_name': 'Ivanov',
        'roles': ['someRole'],
    }

    with app.app_context():
        response = authorize_user(jwt_token)

    expected_answer = {
        'msg': 'User authorized',
        'first_name': 'Ivan',
        'last_name': 'Ivanov',
        'roles': ['someRole']
        }
    
    assert response == expected_answer