from typing import Annotated
from fastapi import APIRouter, Depends, Security, status


from auxia.schemas.answer import AnswerRequest
from auxia.schemas.usuario import UserOut
from auxia.usecases.answer import answer_usecase
from auxia.usecases.auth import get_current_active_user

router = APIRouter(prefix="/answer", tags=["answer"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def saveAnswer(
    current_user: Annotated[
        UserOut, Security(get_current_active_user, scopes=["awnsers"])
    ],
    request: AnswerRequest,
):
    return await answer_usecase.saveAnswer(request)

