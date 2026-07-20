from services.retrieval import retrieval_service
from state import GraphState


def retrieve_documents(state: GraphState):

    documents = retrieval_service.retrieve(
        question=(
            state.rewritten_question
            if state.rewritten_question is not None
            else state.standalone_question
        ),
        top_k=5,
    )

    state.retrieved_documents = documents
    state.documents_found = len(documents) > 0

    return state