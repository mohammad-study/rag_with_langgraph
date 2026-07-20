import chromadb
from config import config, abs_path

CHROMA_PATH = abs_path(config["chroma"]["path"])
COLLECTION_NAME = config["chroma"]["collection_name"]

client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)