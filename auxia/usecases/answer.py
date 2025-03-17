from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from auxia.db.mongo import db_client


class AnswerUsecase:
    def __init__(self, database: str = "api") -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database(database)
        self.collection = self.database.get_collection("answer")


answer_usecase = AnswerUsecase()
test_answer_usecase = AnswerUsecase(database="test")
