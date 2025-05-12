from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm


from auxia.models.auth import Token
from auxia.usecases.auth import auth_usecase

router = APIRouter(prefix="/token", tags=["Auth"])


@router.post("")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await auth_usecase.authenticate_user(form_data.username, form_data.password)
    scopes = ["me", "awnsers"]
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth_usecase.ACCESS_TOKEN_EXPIRE_MINUTES)
    if user.usr_is_adm:
        scopes.append("users")
    access_token = auth_usecase.create_access_token(
        data={"sub": user.usr_email, "scopes": scopes},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")
