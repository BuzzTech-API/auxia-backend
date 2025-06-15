from uuid import uuid4
from pydantic import Field
from auxia.schemas.answer import AnswerRequest
from auxia.models.base import CreateBaseModel

class AnswerModel(AnswerRequest, CreateBaseModel):
    ans_pair_id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Identificador único da comparação (mesmo para as duas respostas do par)"
    )
    ans_pair_position: int = Field(
        ..., description="1 ou 2, para indicar se é a primeira ou segunda resposta do par", ge=1, le=2
    )
