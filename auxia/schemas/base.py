from pydantic import BaseModel


class BaseSchemaIn(BaseModel):
    class Config:
        from_attributes=True