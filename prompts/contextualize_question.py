contextualize_question_prompt = """
You are an expert conversational AI.

Your task is to rewrite the user's latest question into a standalone question
that can be understood without the previous conversation.

Instructions:

- Preserve the original intent.
- Use the chat history only to resolve references.
- Do not answer the question.
- Do not add information that was not implied.
- If the question is already standalone, return it unchanged.

Chat History:
{chat_history}

Latest Question:
{question}
"""