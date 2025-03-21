from fastapi import FastAPI

from auxia.core.config import settings
from auxia.routers import api_router
from fastapi.middleware.cors import CORSMiddleware


class App(FastAPI):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            *args,
            **kwargs,
            title=settings.PROJECT_NAME,
            root_path=settings.ROOT_PATH,
            version="0.0.1",
        )


app = App()
app.include_router(api_router)

# Resposta base do backend, tava muito nada a ver antes, se quiser que mova daqui no problem
@app.get("/")
def read_root():
    return "Backend Funcionando!"

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Permitir apenas o frontend em localhost:5173
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)
