from nodes.router import route_query
from state import GraphState

state = GraphState(
    session_id="test-session",
    question=""
)

state.standalone_question = "Explain LangGraph."

result = route_query(state)

print("=" * 60)
print("Router")
print("=" * 60)
print(result.router)