from fastapi import FastAPI

from auxia.core.config import settings
from auxia.routers import api_router


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
