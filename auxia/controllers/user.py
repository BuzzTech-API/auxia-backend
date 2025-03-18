from fastapi import APIRouter, Depends
from auxia.schemas.usuario import UserIn
from auxia.usecases.user import user_usecase

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/create", response_model=dict)
async def create_user(user: UserIn):
    return await user_usecase.create_user(user)

@router.post("/search", response_model=dict)
async def get_user(user: UserIn):
    return await user_usecase.get_user(user)
