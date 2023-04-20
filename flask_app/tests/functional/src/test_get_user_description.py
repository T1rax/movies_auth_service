import pytest
from http import HTTPStatus
import jwt

from settings import test_settings


@pytest.mark.parametrize(
    'test_config, admin_payload, login_payload, expected_answer',
    [
        (
                test_settings,
                {'login': 'superuser',
                'password': 'test_password'},
                {'login': 'preloaded_5',
                'password': 'test_password'},
                {'status': HTTPStatus.OK,
                 'length': 1}
        ),
    ]
)
@pytest.mark.asyncio
async def test_get_user_description_by_id(test_config, admin_payload, login_payload, expected_answer, db_client, mds_client, aiohttp_session):

    #Первый логин для получения id
    response_1 = await aiohttp_session.post(test_config.service_url+'/auth/sign-in', json=login_payload)

    #Получаем админские куки
    response_2 = await aiohttp_session.post(test_config.service_url+'/auth/sign-in', json=admin_payload)

    decoded = jwt.decode(response_1.cookies.get('access_token_cookie').value, options={"verify_signature": False})

    request_payload = {'id': decoded.get('userid')}

    response = await aiohttp_session.get(test_config.service_url+'/auth/get-user-description', json=request_payload, cookies=response_2.cookies)
    body = await response.json()
    user = body.get('user')

    #Проверяем ответ 
    assert response.status == expected_answer['status']
    assert user.get('id') == request_payload['id']
    assert user.get('first_name') is not None
    assert user.get('roles') is not None
    assert user.get('age_group') is not None