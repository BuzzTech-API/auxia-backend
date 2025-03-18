from fastapi import APIRouter
from auxia.controllers.ai import router as ai_router
from auxia.controllers.user import router as user_router

api_router = APIRouter()

api_router.include_router(ai_router)

api_router.include_router(user_router)
