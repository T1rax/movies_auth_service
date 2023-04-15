import pytest
from http import HTTPStatus

from settings import test_settings


@pytest.mark.parametrize(
    'test_config, payload, expected_answer',
    [
        (
                test_settings,
                {'login': 'preloaded_1',
                'password': 'test_password'},
                {'status': HTTPStatus.OK}
        ),
    ]
)
@pytest.mark.asyncio
async def test_login(test_config, payload, expected_answer, db_client, mds_client, aiohttp_session):

    response = await aiohttp_session.post(test_config.service_url+'/auth/sign-in', json=payload)

    cookies_dict = response.cookies

    #Проверяем ответ 
    assert response.status == expected_answer['status']
    assert cookies_dict.get('access_token_cookie').value is not None
    assert cookies_dict.get('refresh_token_cookie').value is not None