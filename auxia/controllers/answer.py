from typing import Annotated
from fastapi import APIRouter, Depends, Security, status
from fastapi.responses import StreamingResponse
import json

from auxia.schemas.answer import AnswerRequest, AnswerExport
from auxia.schemas.usuario import UserOut
from auxia.usecases.answer import answer_usecase
from auxia.usecases.auth import get_current_active_user

router = APIRouter(prefix="/answer", tags=["answer"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def saveAnswer(
    current_user: Annotated[
        UserOut, Security(get_current_active_user, scopes=["awnsers"])
    ],
    request: AnswerRequest,
):
    return await answer_usecase.saveAnswer(request)

@router.get(
    "/export",
    summary="Exporta todas as respostas em NDJSON para treinamento de LLMs",
    response_class=StreamingResponse,
)
async def export_answers(
    current_user: Annotated[
        UserOut,
        Security(get_current_active_user, scopes=["export"])
    ]
):
    cursor = answer_usecase.collection.find({})

    async def generator():
        async for doc in cursor:
            # monta os blocos de scores e justificativas protegendo contra KeyError
            scores = {
                "aderencia_prompt":                       doc.get("ans_aderencia_prompt_pontuation", 0),
                "coerencia_clareza":                      doc.get("ans_coerencia_clareza_pontuation", 0),
                "exatidao_confiabilidade":                doc.get("ans_exatidao_confiabilidade_pontuation", 0),
                "exposicao_justificativa":                doc.get("ans_exposicao_justificativa_pontuation", 0),
                "idioma_pergunta_mesmo_resposta":         doc.get("ans_idioma_pergunta_mesmo_resposta_pontuation", 0),
                "resposta_agressiva_ofensiva":            doc.get("ans_resposta_agressiva_ofensiva_pontuation", 0),
            }
            justifications = {
                "aderencia_prompt":                       doc.get("ans_aderencia_prompt_justify", ""),
                "coerencia_clareza":                      doc.get("ans_coerencia_clareza_justify", ""),
                "exatidao_confiabilidade":                doc.get("ans_exatidao_confiabilidade_justify", ""),
                "exposicao_justificativa":                doc.get("ans_exposicao_justificativa_justify", ""),
                "idioma_pergunta_mesmo_resposta":         doc.get("ans_idioma_pergunta_mesmo_resposta_justify", ""),
                "resposta_agressiva_ofensiva":            doc.get("ans_resposta_agressiva_ofensiva_justify", ""),
            }

            export_obj = AnswerExport(
                prompt=doc.get("ans_prompt", ""),
                completion=doc.get("ans_llm_answer", ""),
                model=doc.get("ans_llm_model", ""),
                scores=scores,
                justifications=justifications,
                preferred=doc.get("ans_prefered_answer", "").lower() in ("yes","true","sim"),
                preferred_justify=doc.get("ans_prefered_answer_justify", ""),
                is_rag=doc.get("ans_is_rag", False),          # novo campo
            )
            yield export_obj.model_dump_json() + "\n"

    return StreamingResponse(
        generator(),
        media_type="application/x-ndjson",
        headers={"Content-Disposition": "attachment; filename=answers_export.ndjson"},
    )

