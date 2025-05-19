from typing import Annotated
from fastapi import APIRouter, Depends, Security

from auxia.schemas.usuario import UserIn, UserOut, UserUpdate, UserUpdateMe
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


@router.put("/{usr_email}", response_model=UserOut)
async def update_user(
    current_user: Annotated[
        UserOut, Security(get_current_active_user, scopes=["users"])
    ],
    usr_email: str,
    user: UserUpdate,
):
    return await user_usecase.update_user(usr_email, user)


@router.patch("/", response_model=UserOut)
async def update_me(
    current_user: Annotated[UserOut, Depends(get_current_active_user)],
    user: UserUpdateMe,
):
    return await user_usecase.update_user_me(
        usr_email=current_user.usr_email, user_update=user
    )
