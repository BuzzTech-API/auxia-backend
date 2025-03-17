from fastapi import APIRouter
from auxia.controllers.ai import router as ai_router

api_router = APIRouter()

api_router.include_router(ai_router)
