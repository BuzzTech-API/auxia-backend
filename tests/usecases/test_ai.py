from auxia.schemas.ai import AiRequest, AiResponse
from auxia.usecases.ai import ai_usecase


async def test_ai_generate_should_return_sucess(ai_request: AiRequest):
    response = ai_usecase.callMainLLMs(prompt=ai_request)

    assert isinstance(response, AiResponse)
    assert response.modelLlm1 == "gemini-2.0-flash"
    assert response.modelLlm1 == "deepseek/deepseek-chat:free"
