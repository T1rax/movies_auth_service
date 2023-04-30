import pytest
from http import HTTPStatus

from settings import test_settings


@pytest.mark.parametrize("test_config", [test_settings])
@pytest.mark.asyncio
async def test_authorize(
    test_config, default_headers_with_rpm, aiohttp_session, db_client, mds_client
):
    # Логинимся для получения токенов
    response_1 = await aiohttp_session.get(
        test_config.service_url + "/auth/v1/", headers=default_headers_with_rpm
    )

    cookies_dict_1 = response_1.cookies

    responses_codes = set()

    for i in range(50):
        response_2 = await aiohttp_session.get(
            test_config.service_url + "/auth/v1/",
            cookies=cookies_dict_1,
            headers=default_headers_with_rpm,
        )
        responses_codes.add(response_2.status)

    # Проверяем ответ
    assert HTTPStatus.OK in responses_codes
    assert HTTPStatus.TOO_MANY_REQUESTS in responses_codes
