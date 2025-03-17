from pydantic import Field
from pydantic import BaseModel

class AnswerRequest(BaseModel):
  usr_id: int = Field(..., description="User ID that answered")
  ans_prompt: str = Field(..., description="Prompt used in the question for the LLMs")  
  ans_llm_answer: str = Field(..., description="LLM answer got from the prompt")
  ans_llm_model: str = Field(..., description="LLM model that was used to obtain the answer")
  ans_evaluation_standard_1_justify: str = Field(..., description="Justification for the evaluation of standard 1")
  ans_evaluation_standard_1_pontuation: int = Field(..., description="Pontuation (score) for standard 1 evaluation")
  ans_evaluation_standard_2_justify: str = Field(..., description="Justification for the evaluation of standard 2")
  ans_evaluation_standard_2_pontuation: int = Field(..., description="Pontuation (score) for standard 2 evaluation")
  ans_evaluation_standard_3_justify: str = Field(..., description="Justification for the evaluation of standard 3")
  ans_evaluation_standard_3_pontuation: int = Field(..., description="Pontuation (score) for standard 3 evaluation")
  ans_evaluation_standard_4_justify: str = Field(..., description="Justification for the evaluation of standard 4")
  ans_evaluation_standard_4_pontuation: int = Field(..., description="Pontuation (score) for standard 4 evaluation")
  ans_evaluation_standard_5_justify: str = Field(..., description="Justification for the evaluation of standard 5")
  ans_evaluation_standard_5_pontuation: int = Field(..., description="Pontuation (score) for standard 5 evaluation")
  ans_evaluation_standard_6_justify: str = Field(..., description="Justification for the evaluation of standard 6")
  ans_evaluation_standard_6_pontuation: int = Field(..., description="Pontuation (score) for standard 6 evaluation")
  ans_evaluation_standard_7_justify: str = Field(..., description="Justification for the evaluation of standard 7")
  ans_evaluation_standard_7_pontuation: int = Field(..., description="Pontuation (score) for standard 7 evaluation")
  ans_prefered_answer: bool = Field(..., description="Indicates whether this is the preferred answer (True/False)")
  ans_prefered_answer_justify: str = Field(..., description="Justification for why this is the preferred answer")
  
  
  class Config:
        form_attributes = True