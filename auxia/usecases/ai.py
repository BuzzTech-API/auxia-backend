from auxia.schemas.ai import AiRequest
from google import genai
import requests
import json
from auxia.core.config import settings


class AIUsecase:
    def __init__(self) -> None:
        pass
    
        
    def callMainLLMs(self, prompt: AiRequest):
        response1 = self.callLLM_GoogleAiStudio(prompt.prompt)
        response2 = self.callLLM_OpenRouter(prompt.prompt)
        
        response1 = response1 if response1 is not None else "Erro no Google AI Studio"
        response2 = response2 if response2 is not None else "Erro no OpenRouter"
        
        data = {
            "response1": response1,
            "response2": response2
        }
        return data    



    # docs da API: https://ai.google.dev/gemini-api/docs
    # site da LLM (outras também podem ser encontradas aqui): https://ai.google.dev/api?lang=python
    def callLLM_GoogleAiStudio(self, request: AiRequest):
        client = genai.Client(api_key=settings.API_KEY_GOOGLE_AI_STUDIO)
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=request,
            )
            
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
            
            #Isso aqui formata num json (pq vem de um jeito muito estranho) e depois pega somente o texto por que ele devolve muita informação.
            return json.loads(response.content)["choices"][0]["message"]["content"]

        except requests.exceptions.RequestException as e:
            print(f"Erro ao chamar OpenRouter (Request Error): {e}")
            return None
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Erro no parse da resposta do OpenRouter: {e}")
            return None
        

        
ai_usecase = AIUsecase()
