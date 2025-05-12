from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from passlib.context import CryptContext

from auxia.core.excepetions import BaseException, NotFoundExcpection
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

    async def get_user(self, usr_email: str) -> UserOut:
        """Busca um usuário baseado no email."""
        user = await self.collection.find_one({"usr_email": usr_email})

        if not user:
            raise NotFoundExcpection(message="Usuário não encontrado")

        # Convertendo para UserOut (removendo a senha)
        user_out = UserOut(**user)
        return user_out

    async def get_users(self) -> list[UserOut]:
        """Busca um usuário baseado no email."""
        users: list[UserOut] = []
        for user in await self.collection.find({}).to_list():
            user_out = UserOut(**user)
            users.append(user_out)
        return users

    async def create_user(self, user_in: UserIn):
        """Cria um novo usuário no banco."""
        user_data = UserModel(**user_in.model_dump())
        try:
            user_by_email = await self.verify_email_is_signup(
                usr_email=user_data.usr_email
            )
            if user_by_email:
                raise BaseException(
                    message="Email já cadastrado no sistema",
                )

            user_data.usr_password = pwd_context.hash(user_data.usr_password)

            await self.collection.insert_one(user_data.model_dump())
            return UserOut(**user_data.model_dump(exclude={"usr_password"}))
        except Exception:
            pass

    async def verify_email_is_signup(self, usr_email: str) -> bool:
        """Busca um usuário baseado no email."""
        user = await self.collection.find_one({"usr_email": usr_email})

        if not user:
            return False

        return True

    async def get_user_with_password(self, usr_email: str) -> UserIn:
        """Busca um usuário baseado no email."""
        user = await self.collection.find_one({"usr_email": usr_email})
        if not user:
            raise NotFoundExcpection(message="Usuário não encontrado")

        return UserIn(**user)


# Instanciando para utilizar na aplicação
user_usecase = UserUsecase()
test_user_usecase = UserUsecase(database="test")
