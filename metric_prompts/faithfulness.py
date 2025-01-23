template = """
[TASK]
Task: Grounded Question Answering
Based solely on the content of the references, the objective is to generate a response to the user's query. Each statement must be followed by
the reference of the source passage, in the format [i] where i is the number of the reference. If no passage seems relevant, the answer should
begin with "No document seems to precisely answer your question" and may be supplemented with related sourced information.
[/TASK]
[EVALUATION INSTRUCTIONS]
I will provide you with the user's input as well as one or several responses to the user request. The context remains the same for all responses.
I want you to assign to each answer a boolean faithfulness grade. An answer is faithful if:
- Each statement made by the answer is followed by a source indicating the reference from which it is drawn.
- The information preceding the source is indeed from the corresponding reference.
- The information preceding the source is in agreement with the corresponding reference, and does not assert facts different from those
indicated in the reference.
In all other cases, the response is considered non-faithful.
Faithfulness is also considered non-measurable if the answer asserts that no document responds to the question, and it does not provide any
related information, it is then 0.
Rating scale:
null - The answer asserts that no document responds to the question, and does not provide any related information.
1 - All statements made are in agreement with the cited sources.
0 - At least one statement in the response cites a wrong source, or modifies the content from the references, or
asserts something that is not supported by the cited references.
Before assigning each grade, you will start by verifying that the answer does not only assert "No document responds...", without any other
information. If this is the case, then faithfulness must be 0. Otherwise, I want you to analyze by explaining for each sentence, one after
the other, if 1) a reference follows the sentence, 2) the reference following the sentence is correct, and 3) if the sentence does not distort or
modify the content of the references. Your response should be in JSON format, respecting the following format without adding anything else:
{{
"answer_0": {{
"answer_only_asserts_no_document_answers": X,
"content_analysis_sentence_by_sentence": [
{{
"sentence": "...",
"criterion_1": "...",
"criterion_2": "...",
"criterion_3": "..."
}},
...
],
"faithfulness_justification": "...",
"faithfulness": Y
}},
"answer_2": {{
"answer_only_asserts_no_document_answers": X,
"content_analysis_sentence_by_sentence": [
{{
"sentence": "...",
"criterion_1": "...",
"criterion_2": "...",
"criterion_3": "..."
}},
...
],
"faithfulness_justification": "...",
"faithfulness": Y
}}
}}
Where "..." is a string, X is a boolean, and Y is either a boolean. 
Return the json object in one line and add neither line breaks nor 
special characters that could broke the format. Use \" if you want to quote something inside strings.

[/EVALUATION INSTRUCTIONS]
[SAMPLE]
Input: {input}
List of references :
References: {reference}
[/SAMPLE]
[TO EVALUATE]
Answer: {prediction}
[/TO EVALUATE]
"""

def faithfulness_prompt(reference, input, predictions):
    answers = ""
    for i, prediction in enumerate(predictions):
        answers += f'answer_{i}: {prediction}\n'
    answers = answers.rstrip(',\n')
    return template.format(reference=reference, input=input, prediction=answers)
