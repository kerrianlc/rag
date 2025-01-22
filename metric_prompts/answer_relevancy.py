template = """
[TASK]
Task: Grounded Question Answering
Based solely on the content of the references, the objective is to generate a response to the user's query. Each statement must be followed by
the reference of the source passage, in the format [i] where i is the number of the reference. If no passage seems relevant, the answer should
begin with "No document seems to precisely answer your question" and may be supplemented with related sourced information.
[/TASK]
[EVALUATION INSTRUCTIONS]
I will provide you with one or several answers, each containing a response to the user request.
I want you to assign to each answer a relevancy grade between 1 and 5:
- Answer relevancy evaluates if the content of the answer accurately responds to the user's question.
- The truthfulness of the information in the answer does not impact relevancy: even if information that appears false is contained in the
answer, as long as this information is related to the request, then relevancy should not decrease. Remember that this information could come
from references mentioning imaginary content that you are unaware of: the only thing to evaluate to assign the relevancy grade is therefore
the adequacy between the information in the answer and the request, NOT their truthfulness.
- The absence of information in the answer does not impact relevancy, only the information contained in the answer is evaluated.
- Answer relevancy cannot be evaluated if the answer mentions that no document responds to the user request, it is then `null`, regardless of
whether it contains other information or not.
Rating scale:
null - The answer asserts that no document precisely responds to the user request. Even if it provides additional \
information, whether appropriate or not, the relevancy remains `null`.
5 - The answer has excellent relevancy. All information provided in the answer is in line with the question \
and precisely answers the user request.
4 - The answer achieves good relevancy by providing relevant information to answer the user \
question. Some information indicated does not exactly answer the question, but remains in line with the request.
3 - The answer has average relevancy, it contains information that allows responding to the user request, \
but it also contains superfluous information, which was not necessary to answer the request.
2 - The answer shows low relevancy, with some elements related to the request, but the majority of \
the content is not in line with the question asked.
1 - The answer has very low relevancy, not answering the user's question at all. The \
content is largely inappropriate or off-topic, delivering no useful information for the request.
Before assigning each grade, you will check that the answer does not contain "No document responds...", if this is the case you must put a
grade of `null`. If this is not the case, you will then analyze the adequacy between the request and the information contained in the answer.
Your response should be in JSON format, respecting the following format:
{{
"answer_0": {{
"answer_affirms_no_document_answers": X,
"answer_relevancy_justification": "...",
"answer_relevancy": Y
}},
"answer_1": {{
"answer_affirms_no_document_answers": X,
"answer_relevancy_justification": "...",
"answer_relevancy": Y
}}
}}
Where "..." is a string, X is a boolean, and Y is an integer between 1 and 5 or `null`.
[/EVALUATION INSTRUCTIONS]
[SAMPLE]
User request: {question}
[/SAMPLE]
[TO EVALUATE]
Answer: {prediction}
[/TO EVALUATE]
"""

def answer_relevancy_prompt(question: str, predictions):
     answers = ""
     print(predictions)
     for i, prediction in enumerate(predictions):
          answers += f'answer_{i}: {prediction}\n'
     answers = answers.rstrip(',\n')
     return template.format(question=question, prediction=answers)