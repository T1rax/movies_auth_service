import pytest
from http import HTTPStatus

from settings import test_settings


@pytest.mark.parametrize(
    "test_config, payload, expected_answer",
    [
        (
            test_settings,
            {"login": "preloaded_1", "password": "test_password"},
            {"status": HTTPStatus.OK, "msg": "User authorized"},
        ),
    ],
)
@pytest.mark.asyncio
async def test_authorize(
    test_config,
    payload,
    expected_answer,
    default_headers,
    aiohttp_session,
    db_client,
    mds_client,
):
    # Логинимся для получения токенов
    response_1 = await aiohttp_session.post(
        test_config.service_url + "/auth/v1/sign-in",
        json=payload,
        headers=default_headers,
    )

    cookies_dict_1 = response_1.cookies

    response_2 = await aiohttp_session.post(
        test_config.service_url + "/auth/v1/authorize",
        cookies=cookies_dict_1,
        headers=default_headers,
    )

    body = await response_2.json()

    # Проверяем ответ
    assert response_1.status == expected_answer["status"]
    assert response_2.status == expected_answer["status"]
    assert cookies_dict_1.get("access_token_cookie").value is not None
    assert cookies_dict_1.get("refresh_token_cookie").value is not None
    assert body.get("msg") == expected_answer["msg"]
    assert body.get("first_name") is not None
    assert body.get("roles") is not None
