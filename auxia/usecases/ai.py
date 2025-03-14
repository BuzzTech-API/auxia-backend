from auxia.schemas.ai import AiRequest
from google import genai
import requests
import json
from auxia.core.config import settings


class AIUsecase:
    def __init__(self) -> None:
        pass

    # docs da API: https://ai.google.dev/gemini-api/docs
    # site da LLM (outras também podem ser encontradas aqui): https://ai.google.dev/api?lang=python
    def callLLM_GoogleAiStudio(self, request: AiRequest):
        client = genai.Client(api_key=settings.API_KEY_GOOGLE_AI_STUDIO)
        response = client.models.generate_content(
            # para mudar o modelo do Google AI Studio, só trocar aqui
            model="gemini-2.0-flash",
            contents=request.prompt,
        )
        return response.text

    # docs da API: https://openrouter.ai/docs/quickstart
    # docs da LLM: https://openrouter.ai/deepseek/deepseek-r1-zero:free
    def callLLM_OpenRouter(self, request: AiRequest):
        print(settings.API_KEY_OPENROUTER)
        
        response = requests.post(
        
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": "Bearer "+settings.API_KEY_OPENROUTER+"",
            "Content-Type": "application/json",
        },
        data=json.dumps(
                {
                    "model": "deepseek/deepseek-chat:free",
                    "messages": [{"role": "user", "content": request.prompt}],
                }
            ),
        )
        
        return json.loads(response.content)
        
        
        
ai_usecase = AIUsecase()
