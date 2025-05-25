import uuid
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import ValidationError
from motor.motor_asyncio import AsyncIOMotorDatabase

from auxia.models.auth import TokenData
from auxia.schemas.usuario import UserOut
from auxia.usecases.user import user_usecase
from auxia.core.config import settings
from auxia.db.mongo import db_client

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/oauth/token",
    scopes={
        "me": "Acessar dados do próprio usuário",
        "users": "Gerenciar usuários",
        "awnsers": "Criar avaliações",
    },
)

class AuthUsecase:
    def __init__(self) -> None:
        self.ALGORITHM = "HS256"
        self.SECRET_KEY = settings.SECRET_KEY
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 5
        self.REFRESH_TOKEN_EXPIRE_DAYS = 30

        self.user_usecase = user_usecase
        client = db_client.get()
        self.database: AsyncIOMotorDatabase = client.get_database("api")
        self.refresh_collection = self.database.get_collection("refresh_tokens")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def create_access_token(
        self,
        subject: str,
        roles: list[str],
        expires_delta: timedelta | None = None
    ) -> str:
        now = datetime.now(timezone.utc)
        expire = now + (expires_delta or timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES))
        payload = {
            "sub": subject,
            "roles": roles,
            "iat": now,
            "exp": expire,
        }
        return jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)

    async def create_refresh_token(self, user_email: str) -> str:
        # gera e salva um novo refresh token
        token_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS)
        doc = {
            "tokenId": token_id,
            "userId": user_email,
            "issuedAt": now,
            "expiresAt": expires_at,
            "revoked": False,
        }
        await self.refresh_collection.insert_one(doc)
        return token_id

    async def authenticate_user(self, email: str, password: str):
        user = await self.user_usecase.get_user_with_password(usr_email=email)
        if not user or not self.verify_password(password, user.usr_password):
            return False
        return await self.user_usecase.get_user(usr_email=email)

    async def get_current_user(
        self,
        security_scopes: SecurityScopes,
        token: str = Depends(oauth2_scheme),
    ) -> UserOut:
        auth_value = (
            f'Bearer scope="{security_scopes.scope_str}"'
            if security_scopes.scopes else "Bearer"
        )
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": auth_value},
        )

        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email: str = payload.get("sub")
            roles: list[str] = payload.get("roles", [])
            if email is None:
                raise credentials_exception
        except (InvalidTokenError, ValidationError):
            raise credentials_exception

        user = await self.user_usecase.get_user(usr_email=email)
        if not user:
            raise credentials_exception

        for scope in security_scopes.scopes:
            if scope not in roles:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": auth_value},
                )
        return user

    async def refresh_access_token(self, old_refresh_token: str):
        now = datetime.now(timezone.utc)
        # 1) pega o doc
        doc = await self.refresh_collection.find_one({"tokenId": old_refresh_token})

        # 2) valida existência
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "invalid_grant",
                    "error_description": "Refresh token inválido."
                },
            )

        # 3) valida revogação
        if doc.get("revoked", False):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "invalid_grant",
                    "error_description": "Refresh token já foi revogado."
                },
            )

        # 4) compara expiry — usando ambos aware em UTC
        expires_at = doc.get("expiresAt")
        if not isinstance(expires_at, datetime):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "invalid_grant",
                    "error_description": "Expiry do token inválido."
                },
            )

        # Se o expires_at vier sem tzinfo, assume UTC
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        if expires_at < now:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "invalid_grant",
                    "error_description": "Refresh token expirado."
                },
            )

        # revoga o token antigo
        await self.refresh_collection.delete_one(
            {"_id": doc["_id"]}
        )

        # emite novos tokens
        user = await self.user_usecase.get_user(usr_email=doc["userId"])
        roles = ["me", "awnsers"] + (["users"] if user.usr_is_adm else [])
        access_expires = timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

        new_access = self.create_access_token(
            subject=user.usr_email, 
            roles=roles, 
            expires_delta=access_expires
        )
        new_refresh = await self.create_refresh_token(user.usr_email)
        return new_access, new_refresh, int(access_expires.total_seconds())

auth_usecase = AuthUsecase()


async def get_current_active_user(
    current_user: UserOut = Security(auth_usecase.get_current_user, scopes=["me"])
):
    if not current_user.usr_is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

