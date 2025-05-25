from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str = Field("Bearer")
    refresh_token: str
    expires_in: int
    scope: str


class TokenData(BaseModel):
    email: str | None = None
    scopes: list[str] = []
