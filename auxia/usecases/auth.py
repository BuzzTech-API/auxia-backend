from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import ValidationError

from auxia.models.auth import TokenData
from auxia.usecases.user import user_usecase
from auxia.schemas.usuario import UserOut
from auxia.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        "me": "Read information about the current user, and create evaluation os awnsers ",
        "users": "Create and Read Users.",
        "awnsers": "Create Awnsers.",
    },
)


class AuthUsecase:
    def __init__(self) -> None:
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 60
        self.user_usecase = user_usecase

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=self.ALGORITHM
        )
        return encoded_jwt

    async def get_current_user(
        self,
        security_scopes: SecurityScopes,
        token: Annotated[str, Depends(oauth2_scheme)],
    ):
        if security_scopes.scopes:
            authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
        else:
            authenticate_value = "Bearer"
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": authenticate_value},
        )
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[self.ALGORITHM]
            )
            username = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_scopes = payload.get("scopes", [])
            token_data = TokenData(scopes=token_scopes, email=username)
        except (InvalidTokenError, ValidationError):
            raise credentials_exception
        if token_data.email is None:
            raise credentials_exception
        user = await self.user_usecase.get_user(usr_email=token_data.email)
        if user is None:
            raise credentials_exception
        for scope in security_scopes.scopes:
            if scope not in token_data.scopes:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": authenticate_value},
                )
        return user

    async def authenticate_user(self, email: str, password: str):
        user = await self.user_usecase.get_user_with_password(usr_email=email)
        if not user:
            return False
        if not self.verify_password(password, user.usr_password):
            return False
        return user


auth_usecase = AuthUsecase()


async def get_current_active_user(
    current_user: Annotated[
        UserOut, Security(auth_usecase.get_current_user, scopes=["me"])
    ],
):
    if not current_user.usr_is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
