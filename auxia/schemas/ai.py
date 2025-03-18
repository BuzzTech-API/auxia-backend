from pydantic import Field

from auxia.schemas.base import BaseSchemaIn


class AiRequest(BaseSchemaIn):
    prompt: str = Field(..., description="Prompt para ser respondido pelas LLM")


class AiResponse(BaseSchemaIn):
    response1: str = Field(..., min_length=1, description="Resposta do modelo de LLM 1")
    response2: str = Field(..., description="Resposta do modelo de LLM 2")
    modelLlm1: str = Field(..., description="Modelo da LLM 1")
    modelLlm2: str = Field(..., description="Modelo de LLM 2")
