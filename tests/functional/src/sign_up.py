import pytest
from http import HTTPStatus

from settings import test_settings


@pytest.mark.parametrize(
    'test_config, payload, expected_answer',
    [
        (
                test_settings,
                {'login': 'test_login1',
                'password': 'test_password',
                'first_name': 'Nikola',
                'last_name': 'Lenivetc'},
                {'status': HTTPStatus.OK}
        ),
    ]
)
@pytest.mark.asyncio
async def test_registration(test_config, film_id, expected_answer, prepare_film_es, cache_clear_cache, aiohttp_helper):

    # 1. Генерируем данные и загружаем данные в ES (запускается 1 раз для всех тестов)
    try:
        await prepare_film_es
    except RuntimeError:
        prepare_film_es
    
    # 2. Чистим кеш редиса (запускается 1 раз для всех тестов)
    try:
        await cache_clear_cache
    except RuntimeError:
        cache_clear_cache

    # 3. Запрашиваем данные из ES по API
    status, array_length, body, headers = await aiohttp_helper.make_get_request(test_config.service_url, '/api/v1/films/'+film_id)

    # 4. Проверяем ответ 
    assert status == expected_answer['status']
    assert body.get('id') == expected_answer['id'] 