from sentence_transformers import SentenceTransformer

class EmbeddingUsecase:
    def __init__(self):
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    def embed_text(self, text: str) -> list[float]:
        embedding = self.model.encode(text)
        return embedding.tolist()

embedding_usecase = EmbeddingUsecase()