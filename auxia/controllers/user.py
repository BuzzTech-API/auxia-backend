from typing import Annotated
from fastapi import APIRouter, Depends, Security

from auxia.schemas.usuario import UserIn, UserOut
from auxia.usecases.user import user_usecase
from auxia.usecases.auth import get_current_active_user

router = APIRouter(prefix="/user", tags=["user"])


@router.post("", response_model=UserOut)
async def create_user(
    current_user: Annotated[
        UserOut, Security(get_current_active_user, scopes=["users"])
    ],
    user: UserIn,
):
    return await user_usecase.create_user(user)


@router.get("", response_model=list[UserOut])
async def get_user(
    current_user: Annotated[
        UserOut, Security(get_current_active_user, scopes=["users"])
    ],
):
    return await user_usecase.get_users()


@router.get("/me/", response_model=UserOut)
async def read_users_me(
    current_user: Annotated[UserOut, Depends(get_current_active_user)],
):
    return current_user
