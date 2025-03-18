import asyncio
import pytest
from auxia.schemas.usuario import UserIn
from tests.factories import usuario_data


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture()
def user_in():
    return UserIn(**usuario_data())