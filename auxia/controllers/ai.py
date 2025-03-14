from fastapi import APIRouter
from ..usecases.ai import ai_usecase
from ..schemas.ai import AiRequest
import logging

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/llm1")
def callLLM1(request: AiRequest):
  return ai_usecase.callLLM_GoogleAiStudio(request)

@router.post("/llm2")
def callLLM2(request: AiRequest):
  return ai_usecase.callLLM_OpenRouter(request)


