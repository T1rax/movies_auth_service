import pytest
import pytest_asyncio
from redis.asyncio import Redis

from utils.helpers import Mds_helper
from settings import test_settings


@pytest_asyncio.fixture(scope='session')
async def mds_client():
    client = Redis(host=test_settings.mds_host, port=test_settings.mds_port)
    await client.flushall()
    yield client
    await client.close()

@pytest.fixture
def mds_helper(mds_client):
    return Mds_helper(mds_client, test_settings)