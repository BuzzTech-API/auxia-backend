from auxia.schemas.answer import AnswerRequest
from tests.factories import answer_data


def test_schemas_return_success():
  data = answer_data()
  answer = AnswerRequest.model_validate(data)
  
  assert answer.usr_id == 202
  assert answer.ans_prompt == "What is the chemical formula for water?"
  assert answer.ans_llm_answer == "The chemical formula for water is H2O."
  assert answer.ans_llm_model == "GPT-4"
  assert answer.ans_evaluation_standard_1_justify == "The answer is scientifically accurate."
  assert answer.ans_evaluation_standard_1_pontuation == 5
  assert answer.ans_evaluation_standard_2_justify == "The response is concise and clear."
  assert answer.ans_evaluation_standard_2_pontuation == 5
  assert answer.ans_evaluation_standard_3_justify == "The answer does not provide additional context, but it is not necessary."
  assert answer.ans_evaluation_standard_3_pontuation == 4
  assert answer.ans_evaluation_standard_4_justify == "The response is well-structured."
  assert answer.ans_evaluation_standard_4_pontuation == 5
  assert answer.ans_evaluation_standard_5_justify == "The answer uses simple language."
  assert answer.ans_evaluation_standard_5_pontuation == 5
  assert answer.ans_evaluation_standard_6_justify == "The response is consistent with established chemical knowledge."
  assert answer.ans_evaluation_standard_6_pontuation == 5
  assert answer.ans_evaluation_standard_7_justify == "The answer is delivered quickly."
  assert answer.ans_evaluation_standard_7_pontuation == 5
  assert answer.ans_prefered_answer is True
  assert answer.ans_prefered_answer_justify == "This answer is accurate and easy to understand."
  
  
  