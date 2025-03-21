from datetime import datetime

from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from passlib.context import CryptContext

from auxia.db.mongo import db_client
from auxia.models.user import UserModel
from auxia.schemas.usuario import UserIn, UserOut

# Configurando o hasheador de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserUsecase:
    def __init__(self, database: str = "api") -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database(database)
        self.collection = self.database.get_collection("user")

    async def create_user(self, user_in: UserIn) -> UserOut:
        """Cria um novo usuário no banco."""
        # Hashear senha antes de armazenar?
        user_data = UserModel(**user_in.model_dump())
        user_data.usr_password = pwd_context.hash(user_data.usr_password)

        # Inserindo...
        await self.collection.insert_one(user_data.model_dump())
        return UserOut(**user_data.model_dump(exclude={"usr_password"}))

    # async def get_user(self, usr_email: str) -> UserOut:
    #     """Busca um usuário baseado no email."""
    #     user = await self.collection.find_one({"usr_email": usr_email})

    #     if not user:
    #         raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    #     # Convertendo para UserOut (removendo a senha)
    #     user_out = UserOut(**user)
    #     return user_out
    async def get_user(self, usr_email: str) -> UserOut:
        """Busca um usuário baseado no email."""
        user = await self.collection.find_one({"usr_email": usr_email})

        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")

        # Convertendo o ObjectId para string e garantindo os campos exigidos
        user["id"] = str(user["_id"])  # Convertendo o ObjectId para string
        user.pop("_id", None)  # Removendo o _id original
        user["created_at"] = user.get(
            "created_at", datetime.now()
        )  # Garantindo created_at

        return UserOut(**user)


# Instanciando para utilizar na aplicação
user_usecase = UserUsecase()
test_user_usecase = UserUsecase(database="test")
