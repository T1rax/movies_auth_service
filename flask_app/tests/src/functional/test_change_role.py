import pytest
from http import HTTPStatus
import jwt

from settings import test_settings


@pytest.mark.parametrize(
    'test_config, admin_payload, login_payload, roles_payload, expected_answer',
    [
        (
                test_settings,
                {'login': 'superuser',
                'password': 'test_password'},
                {'login': 'preloaded_2',
                'password': 'test_password'},
                {'role': 'premiumUser',
                'action_type': 'add'},
                {'status': HTTPStatus.OK,
                 'msg': 'User roles updated'}
        ),
    ]
)
@pytest.mark.asyncio
async def test_add(test_config, admin_payload, login_payload, roles_payload, expected_answer, default_headers, aiohttp_session, db_client, mds_client):

    #Первый логин для получения id
    response_1 = await aiohttp_session.post(test_config.service_url+'/auth/v1/sign-in', json=login_payload, headers=default_headers)

    #Получаем админские куки
    response_2 = await aiohttp_session.post(test_config.service_url+'/auth/v1/sign-in', json=admin_payload, headers=default_headers)

    decoded = jwt.decode(response_1.cookies.get('access_token_cookie').value, options={"verify_signature": False})

    request_payload = {'id': decoded.get('userid'), 
                       'role': roles_payload['role'],
                       'action_type': 'add'}

    response_3 = await aiohttp_session.post(test_config.service_url+'/auth/v1/change-role', json=request_payload, cookies=response_2.cookies, headers=default_headers)
    body_3 = await response_3.json()

    response_4 = await aiohttp_session.get(test_config.service_url+'/auth/v1/get-user-description', json=request_payload, cookies=response_2.cookies, headers=default_headers)
    body_4 = await response_4.json()
    user = body_4.get('user')

    #Проверяем ответ 
    assert response_3.status == expected_answer['status']
    assert body_3.get('msg') == expected_answer['msg']
    assert roles_payload['role'] in body_3.get('roles')
    assert body_3.get('roles') == user.get('roles')
