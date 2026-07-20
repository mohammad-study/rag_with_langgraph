# Embedding Module

This folder contains the code used to build and manage the ChromaDB vector index for the policy documents.

## Files

- `main.py`
  - Loads configuration from `config.yaml`
  - Instantiates the embedding model: `SentenceTransformer("all-MiniLM-L6-v2")`
  - Connects to ChromaDB via `chromadb.PersistentClient`
  - Processes CSV files from the configured `process_folder`
  - Uses `add_to_chroma()` to add document chunks and embeddings to the `policy_docs` collection

- `utils.py`
  - `read_csv_rows(file_path)`: Reads processed CSV rows into a list of dictionaries
  - `create_collection_items(input_files)`: Converts CSV rows into ChromaDB documents, metadata, and IDs
  - `add_to_chroma(file_path, collection, embedding_model)`: Encodes documents, deletes stale IDs, and writes embeddings into ChromaDB

## Usage

1. Ensure `config.yaml` is configured with:
   - `process_folder`: path to processed CSV files
   - `CHROMA_PATH`: path to ChromaDB storage

2. Run the embedding script:
```bash
python app/src/embedding/main.py
```

## Notes

- Processed CSV files in `app/data/processed/` are the source data for embeddings.
- IDs are generated from the CSV row `id` plus `input_file` to ensure uniqueness.
- Existing records are deleted before re-adding updated embeddings, keeping the index fresh.
