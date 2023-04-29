import pytest
import pytest_asyncio
from redis.asyncio import Redis

from settings import test_settings


@pytest_asyncio.fixture(scope='session')
async def mds_client():
    client = Redis(host=test_settings.mds_host, port=test_settings.mds_port)
    await client.flushall()
    yield client
    await client.close()