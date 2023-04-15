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
async def test_sign_in_history(test_config, admin_payload, login_payload, expected_answer, db_client, mds_client, aiohttp_session):

    #Первый логин для записи в историю
    response_1 = await aiohttp_session.post(test_config.service_url+'/auth/sign-in', json=login_payload)

    #Получаем админские куки
    response_2 = await aiohttp_session.post(test_config.service_url+'/auth/sign-in', json=admin_payload)

    decoded = jwt.decode(response_1.cookies.get('access_token_cookie').value, options={"verify_signature": False})

    request_payload = {'id': decoded.get('userid')}

    response = await aiohttp_session.get(test_config.service_url+'/auth/sign-in-history', json=request_payload, cookies=response_2.cookies)
    body = await response.json()

    #Проверяем ответ 
    assert response.status == expected_answer['status']
    assert type(body) == list
    assert len(body) >= expected_answer['length']
    assert body[0].get('user_id') == request_payload['id']
    assert body[0].get('useragent') is not None