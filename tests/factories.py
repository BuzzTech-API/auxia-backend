def usuario_data():

    return {
        "usr_name": "Astolfo",
        "usr_email": "astolfo@gmail.com",
        "usr_password": "123456",
        "usr_is_adm": True,
    }


def ai_propmt_data():
    return {"prompt": "Olá senhora IA como vai?"}


def ai_response_data():
    return {
        "response1": "Muito bem obrigado!",
        "response2": "Estou muito mal hoje!",
        "modelLlm1": "gemini-2.0-flash",
        "modelLlm2": "deepseek/deepseek-chat:free",
    }


def answer_data():
    return {
        "usr_id": 202,
        "ans_prompt": "What is the chemical formula for water?",
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
    }
