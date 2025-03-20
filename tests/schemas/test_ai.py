import pytest
from pydantic import ValidationError

from auxia.schemas.ai import AiRequest, AiResponse
from tests.factories import ai_propmt_data, ai_response_data


def test_schemas_ai_request_return_sucess():
    data = ai_propmt_data()
    aiPrompt = AiRequest.model_validate(data)

    assert aiPrompt.prompt == "Olá senhora IA como vai?"


def test_schemas_ai_response_return_sucess():
    data = ai_response_data()
    aiPrompt = AiResponse.model_validate(data)

    assert aiPrompt.response1 == "Muito bem obrigado!"
    assert aiPrompt.response2 == "Estou muito mal hoje!"
    assert aiPrompt.modelLlm1 == "gemini-2.0-flash"
    assert aiPrompt.modelLlm2 == "deepseek/deepseek-chat:free"


def test_schemas_ai_request_return_raise():
    data = {"promptt": ""}

    with pytest.raises(ValidationError) as err:
        AiRequest.model_validate(data)

    assert err.value.errors()[0] == {
        "type": "missing",
        "loc": ("prompt",),
        "msg": "Field required",
        "input": {"promptt": ""},
        "url": "https://errors.pydantic.dev/2.10/v/missing",
    }


def test_schemas_ai_request_return_raise402():
    data = {"prompt": ""}

    with pytest.raises(ValidationError) as err:
        AiRequest.model_validate(data)

    assert err.value.errors()[0] == {
        "type": "string_too_short",
        "loc": ("prompt",),
        "msg": "String should have at least 1 character",
        "input": "",
        "ctx": {"min_length": 1},
        "url": "https://errors.pydantic.dev/2.10/v/string_too_short",
    }


def test_schemas_ai_response_return_raise():
    data = {
        "response1": "Muito bem obrigado!",
        "modelLlm1": "gemini-2.0-flash",
        "modelLlm2": "deepseek/deepseek-chat:free",
    }

    with pytest.raises(ValidationError) as err:
        AiResponse.model_validate(data)

    assert err.value.errors()[0] == {
        "type": "missing",
        "loc": ("response2",),
        "msg": "Field required",
        "input": {
            "response1": "Muito bem obrigado!",
            "modelLlm1": "gemini-2.0-flash",
            "modelLlm2": "deepseek/deepseek-chat:free",
        },
        "url": "https://errors.pydantic.dev/2.10/v/missing",
    }
