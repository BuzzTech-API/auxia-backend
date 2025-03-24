from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from bson import Binary, UuidRepresentation
import uuid

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
        # Por algum motivo no windows o driver do mongo pro python não consegue trabalhar com o uuid padrão do mongo
        
        if hasattr(answer_data, "id") and isinstance(answer_data.id, uuid.UUID):
            answer_data.id = Binary.from_uuid(answer_data.id, uuid_representation=UuidRepresentation.STANDARD)
        
        await self.collection.insert_one(answer_data.model_dump())
        return 


answer_usecase = AnswerUsecase()
test_answer_usecase = AnswerUsecase(database="test")
