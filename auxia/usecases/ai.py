import json
import random
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
from auxia.usecases.embedding import embedding_usecase

BASE_PROMPT = """
Baseado no contexto abaixo:

{context}

Responda utilizando e referenciando o contexto a seguinte pergunta: {question}
!important include fonte!
"""

# Cenários de randomização: (primeiro modelo, usa RAG?, segundo modelo, usa RAG?)
_SCENARIOS = [
    ("llm1", True,  "llm1", False),
    ("llm1", True,  "llm2", False),
    ("llm2", True,  "llm2", False),
    ("llm2", True,  "llm1", False),
    ("llm1", True,  "llm2", True),
]

class AIUsecase:
    def __init__(self) -> None:
        self.modelLlm1 = "gemini-2.0-flash"
        self.modelLlm2 = "deepseek/deepseek-chat:free"
        self.client: ClientAPI = db_client_chroma.get()
        self.collection: Collection = self.client.get_collection(
            name="test_collection_chunknized"
        )

    def callMainLLMs(self, request: AiRequest) -> AiResponse:
        # Seleciona cenário aleatório
        first_key, first_rag, second_key, second_rag = random.choice(_SCENARIOS)

        def prepare_request(use_rag: bool) -> str:
            if use_rag:
                embedding = embedding_usecase.embed_text(text=request.prompt)
                context   = self.getContext(embedding=embedding, prompt=None)
                return self.getPromptWithContext(context=context, question=request.prompt)
            return request.prompt

        # Prepara prompts
        prompt1 = prepare_request(first_rag)
        prompt2 = prepare_request(second_rag)

        # Constroi objetos de requisição
        req1 = AiRequest(prompt=prompt1)
        req2 = AiRequest(prompt=prompt2)

        # Executa chamadas
        if first_key == "llm1":
            response1 = self.callLLM_GoogleAiStudio(req1)
            model1    = self.modelLlm1
        else:
            response1 = self.callLLM_OpenRouter(req1)
            model1    = self.modelLlm2

        if second_key == "llm1":
            response2 = self.callLLM_GoogleAiStudio(req2)
            model2    = self.modelLlm1
        else:
            response2 = self.callLLM_OpenRouter(req2)
            model2    = self.modelLlm2

        if response1 is not None and response2 is not None:
            # Retorna também as flags de RAG
            return AiResponse(
                response1=response1,
                response2=response2,
                modelLlm1=model1,
                modelLlm2=model2,
                is_rag1=first_rag,
                is_rag2=second_rag,
            )
        # Validação de erros
        err1 = "Erro na primeira LLM" if response1 is None else ""
        err2 = "Erro na segunda LLM"  if response2 is None else ""
        raise AIGenerateException(message=f"{err1} {err2}".strip())


    def callMainLLMsAllRag(self, request: AiRequest) -> AiResponse:
        """
        Chama os dois LLMs sempre usando RAG:
        1) gera embedding
        2) busca contexto
        3) formata prompt
        4) envia para cada LLM
        """
        # 1. embedding e contexto
        embedding = embedding_usecase.embed_text(text=request.prompt)
        context = self.getContext(embedding=embedding, prompt=None)
        prompt_with_context = self.getPromptWithContext(
            context=context,
            question=request.prompt
        )
        # 2. prepara nova requisição
        rag_req = AiRequest(prompt=prompt_with_context)

        # 3. chama ambas as LLMs
        response1 = self.callLLM_GoogleAiStudio(rag_req)
        response2 = self.callLLM_OpenRouter(rag_req)

        # 4. validação e retorno
        if response1 is not None and response2 is not None:
            return AiResponse(
                response1=response1,
                response2=response2,
                modelLlm1=self.modelLlm1,
                modelLlm2=self.modelLlm2,
            )
        err1 = "Erro no Google AI Studio" if response1 is None else ""
        err2 = "Erro no OpenRouter"      if response2 is None else ""
        raise AIGenerateException(message=f"{err1} {err2}".strip())


    def callMainLLMsNoRag(self, prompt: AiRequest) -> AiResponse:
        # Mantém comportamento original: sem RAG
        response2 = self.callLLM_OpenRouter(prompt)
        response1 = self.callLLM_GoogleAiStudio(prompt)
        if response1 is not None and response2 is not None:
            return AiResponse(
                response1=response1,
                response2=response2,
                modelLlm1=self.modelLlm1,
                modelLlm2=self.modelLlm2,
            )
        err1 = "Tudo certo com o Google AI Studio" if response1 is not None else "Erro no Google AI Studio"
        err2 = "Tudo certo com o OpenRouter"      if response2 is not None else "Erro no OpenRouter"
        raise AIGenerateException(message=err1 + "; " + err2)

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

    def callLLM_OpenRouter(self, request: AiRequest):
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": "Bearer " + settings.API_KEY_OPENROUTER,
                    "Content-Type": "application/json",
                },
                data=json.dumps({
                    "model": self.modelLlm2,
                    "messages": [{"role": "user", "content": request.model_dump_json()}],
                }),
            )
            response.raise_for_status()
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
        # Solicita metadados na query para capturar fonte
        return self.collection.query(
            query_embeddings=embedding,
            query_texts=prompt,
            include=["documents", "distances", "metadatas"]
        )

    def getPromptWithContext(self, context: QueryResult, question: str) -> str:
        chunks = []
        docs = context["documents"]
        dists = context["distances"]
        metas = context.get("metadatas", [])
        for i, (doc_list, dist_list) in enumerate(zip(docs, dists)):
            for j, (doc, dist) in enumerate(zip(doc_list, dist_list)):
                if dist < 1.0:
                    meta = metas[i][j] if metas and i < len(metas) and j < len(metas[i]) else {}
                    fonte = meta.get("Title", "desconhecida")
                    chunks.append(f"{doc}\n\nFonte: {fonte}")
        context_text = "\n\n---\n\n".join(chunks)
        prompt_template = ChatPromptTemplate.from_template(BASE_PROMPT)
        return prompt_template.format(context=context_text, question=question)

ai_usecase = AIUsecase()

