from nodes.grounding_query_rewrite import rewrite_for_grounding
from state import GraphState

state = GraphState(
    session_id="test-session",
    question=""
)

state.chat_history = []

state.standalone_question = "What is LangGraph?"

state.generation = "LangGraph was created by Google."

state.hallucination_reason = "The answer is unsupported."

result = rewrite_for_grounding(state)

print("=" * 60)
print("Grounding Rewrite")
print("=" * 60)
print(result.rewritten_question)