from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from auxia.db.mongo import db_client


class UserUsecase:
    def __init__(self, database: str = "api") -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database(database)
        self.collection = self.database.get_collection("user")


user_usecase = UserUsecase()
test_user_usecase = UserUsecase(database="test")
