from fastapi import APIRouter
from auxia.controllers.ai import router as ai
from auxia.controllers.answer import router as answer
from auxia.controllers.user import router as user_router

api_router = APIRouter()

api_router.include_router(ai)
api_router.include_router(answer)
api_router.include_router(user_router)

