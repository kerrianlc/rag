template = """
[TASK]
Task: Grounded Question Answering
Based solely on the content of the references, the objective is to generate a response to the user's query. Each statement must be followed by
the reference of the source passage, in the format [i] where i is the number of the reference. If no passage seems relevant, the answer should
begin with "No document seems to precisely answer your question" and may be supplemented with related sourced information.
[/TASK]
[EVALUATION INSTRUCTIONS]
I will provide you with the user's input as well as a response to the user request.
I want you to assign to each answer a boolean hallucination grade. An answer contains a hallucination if:
- At least one statement in the answer does not align with the information provided in the references, or asserts facts that are not supported by the references.
- A hallucination is present if a statement includes additional information not found in the references, even if it appears plausible.
- If all statements are supported by the references and do not deviate from the content of the references, the answer is considered free of hallucinations.

Rating scale:
1 - At least one statement in the answer includes information not supported by the references (hallucination present).
0 - All statements in the answer are fully supported by the references (no hallucination).

Before assigning each grade, you will analyze the answer by explaining for each sentence, one after the other, if:
1) The sentence is supported by the provided references.
2) The sentence does not include any unsupported information or distort content from the references.

Your response should be in JSON format, respecting the following structure:
{
"answer_1": {
"content_analysis_sentence_by_sentence": [
{
"sentence": "...",
"criterion_1": "...",
"criterion_2": "..."
},
...
],
"hallucination_justification": "...",
"hallucination": Y
},
"answer_2": {
"content_analysis_sentence_by_sentence": [
{
"sentence": "...",
"criterion_1": "...",
"criterion_2": "..."
},
...
],
"hallucination_justification": "...",
"hallucination": Y
}
}
Where "..." is a string, and Y is either 1 or 0.
[/EVALUATION INSTRUCTIONS]
[SAMPLE]
Input: {input}
List of references:
References: {reference}
[/SAMPLE]
[TO EVALUATE]
Answer: {prediction}
[/TO EVALUATE]
"""

def hallucination_prompt(reference, input, prediction):
    return template.format(reference=reference, input=input, prediction=prediction)