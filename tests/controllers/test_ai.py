from fastapi import status
from httpx import AsyncClient

from tests.factories import ai_propmt_data


async def test_controller_generate_should_return_success(
    client: AsyncClient, ais_url: str
):
    response = await client.post(ais_url + "generate", json=ai_propmt_data())
    content = response.json()
    del content["response1"]
    del content["response2"]

    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "modelLlm1": "gemini-2.0-flash",
        "modelLlm2": "deepseek/deepseek-chat:free",
    }
