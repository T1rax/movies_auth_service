import pytest
import pytest_asyncio
import aiohttp
import uuid


@pytest_asyncio.fixture(scope="session")
async def aiohttp_session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def default_headers():
    return {"x-request-id": str(uuid.uuid4()), "ignore_rpm": str(True)}


@pytest.fixture
def default_headers_with_rpm():
    return {"x-request-id": str(uuid.uuid4()), "ignore_rpm": str(False)}
