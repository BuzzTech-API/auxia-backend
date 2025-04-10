import chromadb
from chromadb.api import ClientAPI

from auxia.core.config import settings


class ChromaClient:
    def __init__(self) -> None:
        self.client: ClientAPI = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)

    def get(self) -> ClientAPI:
        return self.client


db_client_chroma = ChromaClient()
