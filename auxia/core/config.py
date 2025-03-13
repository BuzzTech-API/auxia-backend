from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Auxia API"
    ROOT_PATH: str = "/"

    DATABASE_URL: str
    API_KEY_GEMINI: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
