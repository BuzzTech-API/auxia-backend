from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Auxia API"
    ROOT_PATH: str = "/"

    DATABASE_URL: str
    API_KEY_GOOGLE_AI_STUDIO: str
    API_KEY_OPENROUTER: str
    ADM_EMAIL: str
    ADM_PASSWORD: str
    ADM_NAME: str
    CHROMA_DB_PATH: str
    SECRET_KEY: str
    REFRESH_KEY:str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
