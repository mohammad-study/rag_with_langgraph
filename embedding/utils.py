import csv
import chromadb
from sentence_transformers import SentenceTransformer


def read_csv_rows(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def create_collection_items(input_files: list):
    documents = []
    metadatas = []
    ids = []

    for file in input_files:
        rows = read_csv_rows(file)

        print("Rows:", len(rows))
        print("Sample row:", rows[0] if rows else "EMPTY")

        for r in rows:
            documents.append(r["chunk"])

            metadatas.append(
                {
                    "section": r["section"],
                    "subsection": r["subsection"],
                    "keywords": r["keywords"],
                }
            )

            ids.append(r["id"] + "_" + r["input_file"])

    return {"documents": documents, "metadatas": metadatas, "ids": ids}


def add_to_chroma(
    file_path: str,
    collection: chromadb.Collection,
    embedding_model: SentenceTransformer,
):
    print(f"Creating collection items from {file_path}...")
    collection_item = create_collection_items(input_files=[file_path])
    documents = collection_item["documents"]
    metadatas = collection_item["metadatas"]
    ids = collection_item["ids"]

    print("Documents:", len(documents))
    print("Metadatas:", len(metadatas))
    print("IDs:", len(ids))

    # ---------- Create Embeddings ----------
    if not documents:
        print("No documents found!")
        return
    embeddings = embedding_model.encode(documents).tolist()

    existing_ids = set(collection.get(ids=ids)["ids"])

    ids_to_delete = []
    new_docs = []
    new_meta = []
    new_ids = []
    new_embeddings = []

    for i, _ids in enumerate(ids):
        if _ids in existing_ids:
            ids_to_delete.append(
                _ids
            )  # mark for deletion to ensure we always have the latest version of the document in Chroma
        # always insert fresh version
        new_ids.append(_ids)
        new_docs.append(documents[i])
        new_meta.append(metadatas[i])
        new_embeddings.append(embeddings[i])

    # Step 2: Delete old records
    if ids_to_delete:
        collection.delete(ids=ids_to_delete)
        print(f"Deleted {len(ids_to_delete)} existing records")

    # ---------- Store in Chroma ----------
    collection.add(
        documents=new_docs, embeddings=new_embeddings, metadatas=new_meta, ids=new_ids
    )
