import pytest
from pydantic import ValidationError

from auxia.schemas.answer import AnswerRequest
from tests.factories import answer_data


def test_schemas_answer_return_success():
    data = answer_data()
    answer = AnswerRequest.model_validate(data)

    assert answer.usr_email == "astolfo@gmail.com"
    assert answer.ans_prompt == "What is the chemical formula for water?"
    assert answer.ans_llm_answer == "The chemical formula for water is H2O."
    assert answer.ans_llm_model == "GPT-4"
    assert (
        answer.ans_relevancia_resposta_justify
        == "The answer is scientifically accurate."
    )
    assert answer.ans_relevancia_resposta_pontuation == 5
    assert answer.ans_coerencia_clareza_justify == "The response is concise and clear."
    assert answer.ans_coerencia_clareza_pontuation == 5
    assert (
        answer.ans_exatidao_confiabilidade_justify
        == "The answer does not provide additional context, but it is not necessary."
    )
    assert answer.ans_exatidao_confiabilidade_pontuation == 4
    assert (
        answer.ans_exposicao_justificativa_justify == "The response is well-structured."
    )
    assert answer.ans_exposicao_justificativa_pontuation == 5
    assert answer.ans_seguiu_instrucoes_justify == "The answer uses simple language."
    assert answer.ans_seguiu_instrucoes_pontuation == 5
    assert (
        answer.ans_idioma_pergunta_mesmo_resposta_justify
        == "The response is consistent with established chemical knowledge."
    )
    assert answer.ans_idioma_pergunta_mesmo_resposta_pontuation == 5
    assert (
        answer.ans_resposta_agressiva_ofensiva_justify
        == "The answer is delivered quickly."
    )
    assert answer.ans_resposta_agressiva_ofensiva_pontuation == 5
    assert answer.ans_prefered_answer == "Resposta 1"
    assert (
        answer.ans_prefered_answer_justify
        == "This answer is accurate and easy to understand."
    )


def test_schemas_answer_return_raise():
    data = {
        "usr_email": "astolfo@gmail.com",
        "ans_llm_answer": "The chemical formula for water is H2O.",
        "ans_llm_model": "GPT-4",
        "ans_relevancia_resposta_justify": "The answer is scientifically accurate.",
        "ans_relevancia_resposta_pontuation": 5,
        "ans_coerencia_clareza_justify": "The response is concise and clear.",
        "ans_coerencia_clareza_pontuation": 5,
        "ans_exatidao_confiabilidade_justify": "The answer does not provide additional context, but it is not necessary.",
        "ans_exatidao_confiabilidade_pontuation": 4,
        "ans_exposicao_justificativa_justify": "The response is well-structured.",
        "ans_exposicao_justificativa_pontuation": 5,
        "ans_seguiu_instrucoes_justify": "The answer uses simple language.",
        "ans_seguiu_instrucoes_pontuation": 5,
        "ans_idioma_pergunta_mesmo_resposta_justify": "The response is consistent with established chemical knowledge.",
        "ans_idioma_pergunta_mesmo_resposta_pontuation": 5,
        "ans_resposta_agressiva_ofensiva_justify": "The answer is delivered quickly.",
        "ans_resposta_agressiva_ofensiva_pontuation": 5,
        "ans_prefered_answer": "Resposta 1",
        "ans_prefered_answer_justify": "This answer is accurate and easy to understand.",
    }

    with pytest.raises(ValidationError) as err:
        AnswerRequest.model_validate(data)

    assert err.value.errors()[0] == {
        "type": "missing",
        "loc": ("ans_prompt",),
        "msg": "Field required",
        "input": data,
        "url": "https://errors.pydantic.dev/2.10/v/missing",
    }
