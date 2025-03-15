from pydantic import BaseModel

class AiRequest(BaseModel):
  prompt: str
  
  class Config:
        form_attributes = True
        
