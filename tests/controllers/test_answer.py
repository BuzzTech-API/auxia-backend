from fastapi import status
from httpx import AsyncClient

from tests.factories import answer_data


async def test_controller_generate_should_return_success(
    client: AsyncClient, answers_url: str
):
    response = await client.post(answers_url, json=answer_data())
    assert response.status_code == status.HTTP_201_CREATED