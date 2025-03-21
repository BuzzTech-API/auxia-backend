from datetime import datetime
from http import HTTPStatus
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
    
    async def saveAnswer(self, answer: AnswerRequest):
        answer_data = AnswerModel(**answer.model_dump())
        
        await self.collection.insert_one(answer_data.model_dump())
        return 
    
    
    
    
    
    
    
    
    async def getAllAnswers(self) -> AnswerModel:
        answers = await self.collection.find()

        # Convertendo o ObjectId para string e garantindo os campos exigidos
        answers["id"] = str(answers["_id"])  # Convertendo o ObjectId para string
        answers.pop("_id", None)  # Removendo o _id original
        answers["created_at"] = answers.get(
            "created_at", datetime.now()
        )  # Garantindo created_at

        return answers



answer_usecase = AnswerUsecase()
test_answer_usecase = AnswerUsecase(database="test")
