from fastapi import APIRouter

from auxia.schemas.answer import AnswerRequest
from auxia.usecases.answer import answer_usecase

router = APIRouter(prefix="/answer", tags=["answer"])

@router.post()
def callLLM(request: AnswerRequest):
  return answer_usecase.saveAnswer(request)