from nodes.contextualize import contextualize_question
from state import GraphState

state = GraphState(
    session_id="test-session",
    question="What is LangGraph?"
)

state.chat_history = [
    {"role": "user", "content": "Tell me about LangChain"},
    {"role": "assistant", "content": "LangChain is an LLM framework."}
]

result = contextualize_question(state)

print("=" * 60)
print("Contextualized Question")
print("=" * 60)
print(result.standalone_question)