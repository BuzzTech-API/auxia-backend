from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from auxia.db.mongo import db_client
from auxia.models.answer import AnswerModel
from auxia.schemas.answer import AnswerRequest


class AnswerUsecase:
    def __init__(self, database: str = "api") -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database(database)
        self.collection = self.database.get_collection("answer")

    async def saveAnswer(self, answer: AnswerModel):
        try:

            await self.collection.insert_one(answer.model_dump())
            return {"message": "Resposta Salva com sucesso!"}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


answer_usecase = AnswerUsecase()
test_answer_usecase = AnswerUsecase(database="test")
