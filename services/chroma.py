import chromadb

CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "company_documents"

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="company_documents"   # use your actual collection name
)