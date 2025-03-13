from pydantic import BaseModel

class AiRequest(BaseModel):
  prompt: str

class AiResponse(BaseModel):
  response: str
  
  class Config:
        orm_mode = True