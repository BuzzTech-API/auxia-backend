import json

import requests
from chromadb import Collection, QueryResult
from chromadb.api import ClientAPI
from chromadb.api.types import Document, Embedding, OneOrMany, PyEmbedding
from google import genai
from langchain.prompts import ChatPromptTemplate

from auxia.core.config import settings
from auxia.core.excepetions import AIGenerateException
from auxia.db.chroma import db_client_chroma
from auxia.schemas.ai import AiRequest, AiResponse

BASE_PROMPT = """
Baseado no contexto abaixo:

{context}

Responda utilizando o contexto a seguinte pergunta: {question}
"""


class AIUsecase:
    def __init__(self) -> None:
        self.modelLlm1 = "gemini-2.0-flash"
        self.modelLlm2 = "deepseek/deepseek-chat:free"
        self.client: ClientAPI = db_client_chroma.get()
        self.collection: Collection = self.client.get_collection(
            name="test_collection_chunknized"
        )

    def callMainLLMs(self, prompt: AiRequest) -> AiResponse:
        response1 = self.callLLM_GoogleAiStudio(prompt)
        response2 = self.callLLM_OpenRouter(prompt)

        if response1 is not None and response2 is not None:
            return AiResponse(
                response1=response1,
                response2=response2,
                modelLlm1=self.modelLlm1,
                modelLlm2=self.modelLlm2,
            )
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
                model=self.modelLlm1,
                contents=request.model_dump_json(),
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
                        "model": self.modelLlm2,
                        "messages": [
                            {"role": "user", "content": request.model_dump_json()}
                        ],
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

    def getContext(
        self,
        embedding: OneOrMany[Embedding] | OneOrMany[PyEmbedding] | None,
        prompt: OneOrMany[Document] | None,
    ) -> QueryResult:
        context = self.collection.query(query_embeddings=embedding, query_texts=prompt)
        return context

    def getPromptWithContext(self, context: QueryResult, question: str) -> str:
        context_text = ""
        documents = context["documents"]
        if documents:
            for docs in documents:
                context_text = "\n\n---\n\n".join(docs)
        prompt_template = ChatPromptTemplate.from_template(BASE_PROMPT)
        prompt = prompt_template.format(context=context_text, question=question)
        return prompt


ai_usecase = AIUsecase()
