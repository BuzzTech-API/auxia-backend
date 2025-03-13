from auxia.schemas.ai import AiRequest
from google import genai
from auxia.core.config import settings


class AIUsecase:
    def __init__(self) -> None:
        pass

    # Tem que definir os das funções pra ficar mais coerente
    # Essa API Aceita 15 Req/min e 1500 req/dia
    # https://ai.google.dev/api?lang=python
    def callAI_Gemini(self, request: AiRequest):
        client = genai.Client(api_key=settings.API_KEY_GEMINI)
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=request.prompt
        )
        return response.text


ai_usecase = AIUsecase()
