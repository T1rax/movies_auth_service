import pytest
import pytest_asyncio
from tests.testdata.fake_variables import FakeUser


@pytest.fixture()
def generate_fake_user():
    return FakeUser()