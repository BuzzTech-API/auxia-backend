from fastapi import APIRouter
from ..usecases.ai import ai_usecase
from ..schemas.ai import AiRequest
import logging

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/")
def callAI_Gemini(request: AiRequest):
  return ai_usecase.callAI_Gemini(request.prompt)


