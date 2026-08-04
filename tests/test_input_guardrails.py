from nodes.input_validation import input_guardrails
from state import GraphState

state = GraphState(
    session_id="test-session",
    question="What is LangGraph?"
)

result = input_guardrails(state)

print("=" * 60)
print("Input Guardrail")
print("=" * 60)
print("Valid:", result.is_valid)
print("Reason:", result.validation_error)