import pytest
import pytest_asyncio
import aiohttp

from utils.helpers import AiohttpHelper


@pytest_asyncio.fixture(scope='session')
async def aiohttp_session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()

@pytest.fixture
def aiohttp_helper(aiohttp_session, test_config):
    return AiohttpHelper(aiohttp_session, test_config)