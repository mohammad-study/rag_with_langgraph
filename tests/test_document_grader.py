from nodes.document_grade import grade_documents
from state import GraphState

from models.retrieved_document import RetrievedDocument

state = GraphState(
    session_id="test-session",
    question=""
)

state.standalone_question = "What is LangGraph?"

state.retrieved_documents = [
    RetrievedDocument(
        id="doc-1",
        section="Intro",
        subsection="Overview",
        chunk="LangGraph is a framework for building stateful AI agents."
    )
]

result = grade_documents(state)

print("=" * 60)
print("Document Grader")
print("=" * 60)
print(result.documents_relevant)