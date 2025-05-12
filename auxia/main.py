from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auxia.core.config import settings
from auxia.routers import api_router
from auxia.schemas.usuario import UserIn
from auxia.usecases.user import user_usecase


class App(FastAPI):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            *args,
            **kwargs,
            title=settings.PROJECT_NAME,
            root_path=settings.ROOT_PATH,
            version="0.0.1",
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Cria um usuário administrador ao iniciar a aplicação."""
    user_data = UserIn(
        usr_email=settings.ADM_EMAIL,
        usr_is_adm=True,
        usr_is_active=True,
        usr_name=settings.ADM_NAME,
        usr_password=settings.ADM_PASSWORD,
    )
    await user_usecase.create_user(user_in=user_data)
    print("Usuário administrador criado com sucesso!")
    yield


app = App(lifespan=lifespan)
app.include_router(api_router)

# Evento de inicialização para criar o usuário admin


# Resposta base do backend, tava muito nada a ver antes, se quiser que mova daqui no problem
@app.get("")
def read_root():
    return "Backend Funcionando!"


origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],  # Permitir apenas o frontend em localhost:5173
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)
