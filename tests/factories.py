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
        "usr_email": "astolfo@gmail.com",
        "ans_prompt": "What is the chemical formula for water?",
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
