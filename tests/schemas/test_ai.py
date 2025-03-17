from auxia.schemas.ai import AiRequest
from tests.factories import ai_propmt_data


def test_schemas_return_sucess():
    data = ai_propmt_data()
    aiPrompt = AiRequest.model_validate(data)

    assert aiPrompt.prompt == "Olá senhora IA como vai?"
