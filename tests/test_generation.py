from nodes.generate import generate_answer
from state import GraphState
from models.retrieved_document import RetrievedDocument

state = GraphState(
    session_id="test-session",
    question=""
)

state.chat_history = []

state.standalone_question = "What is LangGraph?"

state.retrieved_documents = [
    RetrievedDocument(
        id="doc-1",
        section="Intro",
        subsection="Overview",
        chunk="LangGraph is a framework for building stateful AI agents."
    )
]

result = generate_answer(state)

print("=" * 60)
print("Generation")
print("=" * 60)
print(result.generation)