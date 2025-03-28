from fastapi import status
from fastapi.testclient import TestClient

from tests.factories import ai_propmt_data


async def test_controller_generate_should_return_success(
    client: TestClient, ais_url: str
):
    response = client.post(ais_url + "generate", json=ai_propmt_data())
    content = response.json()
    del content["response1"]
    del content["response2"]

    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "modelLlm1": "gemini-2.0-flash",
        "modelLlm2": "deepseek/deepseek-chat:free",
    }


async def test_controller_generate_should_return_unprocesseble(
    client,
    ais_url,
):
    response = client.post(ais_url + "generate", json={"prompt": ""})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
