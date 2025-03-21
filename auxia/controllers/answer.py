from fastapi import APIRouter, status


from auxia.schemas.answer import AnswerRequest
from auxia.usecases.answer import answer_usecase

router = APIRouter(prefix="/answer", tags=["answer"])

@router.post("", status_code=status.HTTP_201_CREATED)
async def saveAnswer(request: AnswerRequest):
  return await answer_usecase.saveAnswer(request)