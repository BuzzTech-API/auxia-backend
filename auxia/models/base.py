from datetime import datetime

from pydantic import BaseModel, Field


class CreateBaseModel(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
