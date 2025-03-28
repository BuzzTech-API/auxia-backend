import asyncio

import pytest
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from auxia.db.mongo import db_client
from auxia.schemas.ai import AiRequest
from auxia.schemas.usuario import UserIn
from auxia.usecases.user import user_usecase
from tests.factories import ai_propmt_data, usuario_data


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
def user_in():
    return UserIn(**usuario_data())


@pytest.fixture()
async def create_user():
    await user_usecase.create_user(user_in=UserIn(**usuario_data()))


@pytest.fixture
def mongo_client() -> AsyncIOMotorClient:
    return db_client.get()


@pytest.fixture
def ais_url() -> str:
    return "/ai/"


@pytest.fixture
def answers_url() -> str:
    return "/answer"


@pytest.fixture
def ai_request() -> AiRequest:
    return AiRequest(**ai_propmt_data())


@pytest.fixture
@pytest.mark.anyio
async def client() -> AsyncClient:
    async with AsyncClient(base_url="http://localhost:8000") as client:
        yield client


# @pytest.fixture(autouse=True)
# async def clear_collections(mongo_client: AsyncIOMotorClient):
#     yield
#     collections_names = await mongo_client.get_database(
#         name="test"
#     ).list_collection_names()
#     for collections_name in collections_names:
#         if collections_name.startswith("system"):
#             continue
#
#         await mongo_client.get_database(name="test")[collections_name].delete_many({})
#


@pytest.fixture(autouse=True)
async def clear_collections_api(mongo_client: AsyncIOMotorClient):
    yield
    collections_names = await mongo_client.get_database(
        name="api"
    ).list_collection_names()
    for collections_name in collections_names:
        if collections_name.startswith("system"):
            continue

        await mongo_client.get_database(name="api")[collections_name].delete_many({})
