from nodes.grading_query_rewrite import rewrite_query
from state import GraphState

state = GraphState(
    session_id="test-session",
    question=""
)

state.standalone_question = "What is it?"

state.chat_history = [
    {
        "role": "user",
        "content": "Tell me about LangGraph."
    }
]

result = rewrite_query(state)

print("=" * 60)
print("Query Rewrite")
print("=" * 60)
print(result.rewritten_question)