from nodes.input_validation import input_guardrails
from state import GraphState

state = GraphState(
    question="What is LangGraph?",
    session_id="test-session"
)

result = input_guardrails(state)

print(result)
print("Valid:", result.is_valid)
print("Reason:", result.validation_error)
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
