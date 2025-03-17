import asyncio

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from auxia.db.mongo import db_client


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mongo_client() -> AsyncIOMotorClient:
    return db_client.get()


@pytest.fixture(autouse=True)
async def clear_collections(mongo_client: AsyncIOMotorClient):
    yield
    collections_names = await mongo_client.get_database(
        name="test"
    ).list_collection_names()
    for collections_name in collections_names:
        if collections_name.startswith("system"):
            continue

        await mongo_client.get_database()[collections_name].delete_many({})
