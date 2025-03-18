class BaseException(Exception):
    message: str = "Internal Server  Error"

    def __init__(self, *args: object, message: str | None = None) -> None:
        super().__init__(*args)
        if message:
            self.message = message


class AIGenerateException(BaseException):
    message = "Erro ao gerar mensagem"


class NotFoundExcpection(BaseException):
    message = "Not Found"
