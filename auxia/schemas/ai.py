from auxia.schemas.base import BaseSchemaIn


class AiRequest(BaseSchemaIn):
    prompt: str


class AiResponse(BaseSchemaIn):
    response1: str
    response2: str
