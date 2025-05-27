from typing import Dict
from pydantic import Field

from auxia.schemas.base import BaseSchemaIn


class AnswerRequest(BaseSchemaIn):
    usr_email: str = Field(..., description="User Email that answered")
    ans_prompt: str = Field(
        ..., description="Prompt used in the question for the LLMs", min_length=1
    )
    ans_llm_answer: str = Field(
        ..., description="LLM answer got from the prompt", min_length=1
    )
    ans_llm_model: str = Field(
        ..., description="LLM model that was used to obtain the answer", min_length=1
    )
    ans_aderencia_prompt_justify: str = Field(
        ..., description="Justification for the evaluation of standard 1"
    )
    ans_aderencia_prompt_pontuation: int = Field(
        ..., description="Pontuation (score) for standard 1 evaluation"
    )
    ans_coerencia_clareza_justify: str = Field(
        ..., description="Justification for the evaluation of standard 2"
    )
    ans_coerencia_clareza_pontuation: int = Field(
        ..., description="Pontuation (score) for standard 2 evaluation"
    )
    ans_exatidao_confiabilidade_justify: str = Field(
        ..., description="Justification for the evaluation of standard 3"
    )
    ans_exatidao_confiabilidade_pontuation: int = Field(
        ..., description="Pontuation (score) for standard 3 evaluation"
    )
    ans_exposicao_justificativa_justify: str = Field(
        ..., description="Justification for the evaluation of standard 4"
    )
    ans_exposicao_justificativa_pontuation: int = Field(
        ..., description="Pontuation (score) for standard 4 evaluation"
    )
    ans_idioma_pergunta_mesmo_resposta_justify: str = Field(
        ..., description="Justification for the evaluation of standard 5"
    )
    ans_idioma_pergunta_mesmo_resposta_pontuation: int = Field(
        ..., description="Pontuation (score) for standard 5 evaluation"
    )
    ans_resposta_agressiva_ofensiva_justify: str = Field(
        ..., description="Justification for the evaluation of standard 6"
    )
    ans_resposta_agressiva_ofensiva_pontuation: int = Field(
        ..., description="Pontuation (score) for standard 6 evaluation"
    )
    ans_prefered_answer: str = Field(
        ..., description="Indicates whether this is the preferred answer"
    )
    ans_prefered_answer_justify: str = Field(
        ..., description="Justification for why this is the preferred answer"
    )
    ans_is_rag: bool = Field(
        ..., description="Is with rag or not?"
    )

class AnswerExport(BaseSchemaIn):
    prompt: str
    completion: str
    model: str
    scores: Dict[str, int]
    justifications: Dict[str, str]
    preferred: bool
    preferred_justify: str
    is_rag: bool
