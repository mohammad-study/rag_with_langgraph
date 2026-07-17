answer_grader_prompt = """
You are an answer quality evaluator.

Determine whether the generated answer completely answers the user's question.

Consider:

- completeness
- correctness
- relevance
- clarity

Return only

complete

or

incomplete

Question

{question}

Answer

{generation}
"""