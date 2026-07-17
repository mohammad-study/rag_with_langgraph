import hashlib

import chromadb
from sentence_transformers import SentenceTransformer

from models.retrieved_document import RetrievedDocument



def semantic_search(
    query: str, top_k: int, model: SentenceTransformer, collection: chromadb.Collection
):
    """
    Perform semantic search using the provided query, embedding model, and Chroma collection.
    Args:        query (str): The input query for which to perform the search.
        top_k (int): The number of top results to retrieve.
        model (SentenceTransformer): The embedding model to encode the query.
        collection (chromadb.Collection): The Chroma collection to search within.
    """

    query_embedding = model.encode([query]).tolist()

    results = collection.query(query_embeddings=query_embedding, n_results=top_k)

    retrieved_id = []
    for id in results["ids"][0]:
        retrieved_id.append(id)
    return retrieved_id


def keyword_search(query: str, top_k: int, collection: chromadb.Collection) -> list:
    """
    Perform keyword search using the provided query and Chroma collection.
    Args:        query (str): The input query for which to perform the search.
        top_k (int): The number of top results to retrieve.
    """
    all_data = collection.get(include=["metadatas"])

    query_words = set(query.lower().split())
    keyword_scores = {}

    for id_, meta in zip(all_data["ids"], all_data["metadatas"]):
        keywords = set(k.strip() for k in meta["keywords"].lower().split(","))

        score = len(query_words & keywords) / max(len(query_words), 1)
        keyword_scores[id_] = score

    sorted_ids = sorted(keyword_scores, key=keyword_scores.get, reverse=True)

    return sorted_ids[:top_k]


def reciprocal_rank_fusion(
    semantic_ids: list,
    keyword_ids: list,
    semantic_weight: float = 0.8,
    keyword_weight: float = 0.2,
    k: int = 60,
    top_k: int = 5,
) -> list:
    """
    Perform Reciprocal Rank Fusion (RRF) to combine semantic and keyword search results.
    Args:        semantic_ids (list): List of document IDs from semantic search.
        keyword_ids (list): List of document IDs from keyword search.
        semantic_weight (float): Weight for semantic search scores.
        keyword_weight (float): Weight for keyword search scores.
        k (int): The constant used in the RRF formula to dampen the effect of lower-ranked results.
        top_k (int): The number of top results to return after fusion.
    """
    rpf_scores = {}

    semantic_rank_map = {
        doc_id: rank for rank, doc_id in enumerate(semantic_ids, start=1)
    }
    keyword_rank_map = {
        doc_id: rank for rank, doc_id in enumerate(keyword_ids, start=1)
    }

    all_doc_ids = set(semantic_ids) | set(keyword_ids)

    for doc_id in all_doc_ids:
        semantic_score = (
            1 / (k + semantic_rank_map[doc_id]) if doc_id in semantic_rank_map else 0
        )

        keyword_score = (
            1 / (k + keyword_rank_map[doc_id]) if doc_id in keyword_rank_map else 0
        )

        final_score = semantic_weight * semantic_score + keyword_weight * keyword_score

        rpf_scores[doc_id] = final_score

    sorted_ids = sorted(rpf_scores, key=rpf_scores.get, reverse=True)

    return sorted_ids[:top_k]


def query_knowledge_base(
    query: str,
    model: SentenceTransformer,
    collection: chromadb.Collection,
    alpha: float,
    semantic_top_k: int,
    keyword_top_k: int,
    top_k: int,
) -> list:
    """
    Query the knowledge base using a combination of semantic and keyword search, followed by Reciprocal Rank Fusion (RRF) to retrieve the most relevant information.
    Args:        query (str): The input query for which to retrieve information.
        model (SentenceTransformer): The embedding model to encode the query for semantic search.
        collection (chromadb.Collection): The Chroma collection to search within.
        alpha (float): The weight for semantic search in the RRF calculation.
        semantic_top_k (int): The number of top results to retrieve from semantic search.
        keyword_top_k (int): The number of top results to retrieve from keyword search.
        top_k (int): The number of top results to return after RRF fusion.
    """
    top_semantic_ids = semantic_search(
        query=query, top_k=semantic_top_k, model=model, collection=collection
    )
    top_keyword_ids = keyword_search(
        query=query, top_k=keyword_top_k, collection=collection
    )

    top_k_ids = reciprocal_rank_fusion(
        semantic_ids=top_semantic_ids,
        keyword_ids=top_keyword_ids,
        semantic_weight=alpha,
        keyword_weight=1 - alpha,
        k=30,
        top_k=top_k,
    )

    # Nothing found
    if not top_k_ids:
        return []

    collection_data = collection.get(ids=top_k_ids, include=["documents", "metadatas"])

    retrieved_info = []
    for doc, metadata, id in zip(
        collection_data["documents"],
        collection_data["metadatas"],
        collection_data["ids"],
    ):
        retrieved_info.append(
            RetrievedDocument(
                chunk=doc,
                section=metadata["section"],
                subsection=metadata["subsection"],
                id=id,
            )
        )
    return retrieved_info