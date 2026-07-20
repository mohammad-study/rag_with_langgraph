import os
from sentence_transformers import SentenceTransformer

from .utils import add_to_chroma
from services.chroma import collection


CHROMA_PATH = "./chroma_db"
process_folder = "C:\\Users\\hassa\\Documents\\Data_Engineering_Project\\rag_with_langgraph\\data\\processed"

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Process documents and add to Chroma
def process_documents(
    is_process_folder: bool,
    is_process_file: bool,
    process_folder: str,
    process_file: str,
):

    if is_process_folder:
        for file in os.listdir(process_folder):

            if file.endswith(".csv"):
                file_path = os.path.join(process_folder, file)
                print(f"Processing {file_path}...")
                add_to_chroma(
                    file_path=file_path, collection=collection, embedding_model=model
                )
    elif is_process_file:
        if process_file.endswith(".csv"):
            file_path = os.path.join(process_folder, process_file)
            print(f"Processing {file_path}...")
            add_to_chroma(
                file_path=file_path, collection=collection, embedding_model=model
            )


if __name__ == "__main__":
    print(collection.count())
    process_documents(
        is_process_folder=True,
        is_process_file=False,
        process_folder=process_folder,
        process_file="code_of_conduct.csv",
    )
