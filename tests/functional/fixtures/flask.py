import pytest_asyncio

from flask_app.database.db import db
from flask_app.database.models import User, UserHistory


@pytest_asyncio.fixture(scope='session')
async def db_client():
    clear_db()
    yield db
    db.session.remove()

@pytest_asyncio.fixture(scope='session')
async def clear_db():

    models = [User, UserHistory]

    def truncate_tables(models):
        for model in models:
            model.query.delete()

    truncate_tables(models)




# @pytest_asyncio.fixture(scope='session')
# async def aiohttp_session():
#     session = aiohttp.ClientSession()
#     yield session
#     await session.close()

# @pytest.fixture
# def aiohttp_helper(aiohttp_session, test_config):
#     return Aiohttp_helper(aiohttp_session, test_config)