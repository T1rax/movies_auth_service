import pytest
import pytest_asyncio
import aiohttp
import uuid

from utils.helpers import AiohttpHelper


@pytest_asyncio.fixture(scope='session')
async def aiohttp_session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()

@pytest.fixture
def default_headers():
    return {'x-request-id': str(uuid.uuid4())}