import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class CreateBaseModel(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    created_at: datetime = Field(default_factory=datetime.now)
