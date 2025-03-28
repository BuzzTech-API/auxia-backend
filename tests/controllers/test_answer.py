from fastapi import status
from httpx import AsyncClient

from tests.factories import answer_data


async def test_controller_generate_should_return_success(
    client: AsyncClient, answers_url: str
):
    response = await client.post(answers_url, json=answer_data())
    assert response.status_code == status.HTTP_201_CREATED
    
async def test_controller_generate_should_return_unprocesseble(
    client,
    answers_url,
):
    response = await client.post(answers_url, json={
        "usr_id": 202,
        "ans_prompt": "",
        "ans_llm_answer": "The chemical formula for water is H2O.",
        "ans_llm_model": "GPT-4",
        "ans_evaluation_standard_1_justify": "The answer is scientifically accurate.",
        "ans_evaluation_standard_1_pontuation": 5,
        "ans_evaluation_standard_2_justify": "The response is concise and clear.",
        "ans_evaluation_standard_2_pontuation": 5,
        "ans_evaluation_standard_3_justify": "The answer does not provide additional context, but it is not necessary.",
        "ans_evaluation_standard_3_pontuation": 4,
        "ans_evaluation_standard_4_justify": "The response is well-structured.",
        "ans_evaluation_standard_4_pontuation": 5,
        "ans_evaluation_standard_5_justify": "The answer uses simple language.",
        "ans_evaluation_standard_5_pontuation": 5,
        "ans_evaluation_standard_6_justify": "The response is consistent with established chemical knowledge.",
        "ans_evaluation_standard_6_pontuation": 5,
        "ans_evaluation_standard_7_justify": "The answer is delivered quickly.",
        "ans_evaluation_standard_7_pontuation": 5,
        "ans_prefered_answer": True,
        "ans_prefered_answer_justify": "This answer is accurate and easy to understand.",  
    })

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY