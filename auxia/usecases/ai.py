import json

import requests
from google import genai

from auxia.core.config import settings
from auxia.core.excepetions import AIGenerateException
from auxia.schemas.ai import AiRequest, AiResponse


class AIUsecase:
    def __init__(self) -> None:
        pass

    def callMainLLMs(self, prompt: AiRequest) -> AiResponse:
        response1 = self.callLLM_GoogleAiStudio(prompt)
        response2 = self.callLLM_OpenRouter(prompt)

        if response1 is not None and response2 is not None:
            return AiResponse(response1=response1, response2=response2)
        error1 = (
            "Tudo certo com o Google AI Studio "
            if response1 is not None
            else "Erro no Google AI Studio"
        )
        error2 = (
            "Tudo certo com o OpenRouter"
            if response2 is not None
            else "Erro no OpenRouter"
        )

        raise AIGenerateException(message=error1 + error2)

    # docs da API: https://ai.google.dev/gemini-api/docs
    # site da LLM (outras também podem ser encontradas aqui): https://ai.google.dev/api?lang=python
    def callLLM_GoogleAiStudio(self, request: AiRequest):
        client = genai.Client(api_key=settings.API_KEY_GOOGLE_AI_STUDIO)
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=request,
            )
            if response.text is None:
                raise Exception()

            return response.text[:-2]
        except Exception as e:
            print(f"Erro ao Chamar Google AI Studio: {e}")
            return None

    # docs da API: https://openrouter.ai/docs/quickstart
    # docs da LLM: https://openrouter.ai/deepseek/deepseek-r1-zero:free
    def callLLM_OpenRouter(self, request: AiRequest):
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": "Bearer " + settings.API_KEY_OPENROUTER + "",
                    "Content-Type": "application/json",
                },
                data=json.dumps(
                    {
                        "model": "deepseek/deepseek-chat:free",
                        "messages": [{"role": "user", "content": request}],
                    }
                ),
            )
            response.raise_for_status()

            # Isso aqui formata num json (pq vem de um jeito muito estranho) e depois pega somente o texto por que ele devolve muita informação.
            return json.loads(response.content)["choices"][0]["message"]["content"]

        except requests.exceptions.RequestException as e:
            print(f"Erro ao chamar OpenRouter (Request Error): {e}")
            return None
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Erro no parse da resposta do OpenRouter: {e}")
            return None


ai_usecase = AIUsecase()
