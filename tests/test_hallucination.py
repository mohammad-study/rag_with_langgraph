from nodes.hallucination import hallucination_check
from state import GraphState
from models.retrieved_document import RetrievedDocument

state = GraphState(
    session_id="test-session",
    question=""
)

state.standalone_question = "What is LangGraph?"

state.generation = "LangGraph is used to build stateful AI applications."

state.retrieved_documents = [
    RetrievedDocument(
        id="doc-1",
        section="Intro",
        subsection="Overview",
        chunk="LangGraph is a framework for building stateful AI agents."
    )
]

result = hallucination_check(state)

print("=" * 60)
print("Hallucination")
print("=" * 60)
print(result.grounded)
print(result.hallucination_reason)