from fastapi import APIRouter
from ..usecases.ai import ai_usecase
from ..schemas.ai import AiRequest

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/generate")
def callLLM(request: AiRequest):
  return ai_usecase.callMainLLMs(request)


# Vou manter essas rotas por debug, assim podemos testar as LLMs individualmente
@router.post("/llm1")
def callLLM1(request: AiRequest):
  return ai_usecase.callLLM_GoogleAiStudio(request)

@router.post("/llm2")
def callLLM2(request: AiRequest):
  return ai_usecase.callLLM_OpenRouter(request)


