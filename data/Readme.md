# Data Folder

This folder contains the datasets used by the RAG_POC application. It is organized into raw and processed subfolders.

## Folder Structure

- `raw/`
  - Stores original uploaded or sourced documents before preprocessing.
  - Use this folder for the unmodified input files or text that must be cleaned and transformed.

- `processed/`
  - Contains cleaned and preprocessed data files ready for embedding, indexing, and retrieval.
  - The current files are CSV exports for each policy or document type used by the app.


## Processing Method: Markdown Header-Based Chunking

The ingestion pipeline uses **markdown header-based chunking** to intelligently split documents:

### What is Markdown Header-Based Chunking?

This approach splits documents at markdown header boundaries:

1. **Header Detection**: The pipeline identifies all `##` (headers) and `###` (subheaders) in the document
2. **Content Grouping**: Content is grouped under each header/subheader section
3. **Semantic Chunks**: Each header and its associated content form a logical, self-contained chunk
4. **Hierarchical Context**: Subheaders with their content are kept together while maintaining the relationship to parent headers

### Benefits

- **Natural Document Structure**: Chunks follow the document's intended organization
- **Improved Retrieval**: Content is retrieved based on logical sections and meaningful topics
- **Clear Boundaries**: No arbitrary splitting—chunks align with document structure
- **Semantic Coherence**: Related information under the same header stays together
- **Easy to Navigate**: Users can easily understand which section retrieved content comes from

### Processing Pipeline

The `app/src/ingestion/main.py` script:
1. Reads DOCX files from the `raw/` folder
2. Converts documents to markdown format
3. Detects `##` headers and `###` subheaders
4. Splits content at these header boundaries
5. Creates chunks with full context preservation
6. Outputs processed chunks to the `processed/` folder as CSV files

Each output CSV file contains the following fields:
- `id`: A unique identifier for each chunk
- `section`: The main header (e.g., from `##` in markdown)
- `subsection`: The subheader (e.g., from `###` in markdown), if applicable
- `chunk`: The actual text content of the chunk
- `keywords`: Extracted keywords for the chunk to aid in search and retrieval
- `input_file`: The name of the original input file from which the chunk was derived


## Usage

- Place raw source files in `raw/`.
- Run the ingestion/preprocessing pipeline from `app/src/ingestion`.
- The pipeline will write cleaned outputs into `processed/`.
- The retriever and embedding code use the files in `processed/` to build the RAG index.

## Notes

- Keep raw files untouched once you start preprocessing.
- Use version control or backups for `raw/` data when needed.
- The processed CSVs are the primary input for the application’s query and retrieval workflows.
