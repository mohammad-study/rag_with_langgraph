import os
from sentence_transformers import SentenceTransformer

from .utils import add_to_chroma
from services.chroma import collection
from config import config, abs_path

process_folder = abs_path(config["embedding"]["process_folder"])

# Embedding model
model = SentenceTransformer(config["embedding"]["model_name"])


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
