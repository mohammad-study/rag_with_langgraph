# Ingestion Module

The ingestion module handles the extraction, preprocessing, and preparation of raw documents for the RAG (Retrieval-Augmented Generation) pipeline.

## Overview

This module reads `.docx` files from a configured raw folder, preprocesses them through text cleaning and chunking, extracts keywords, and outputs structured data in CSV and/or JSONL formats.

## Directory Structure

```
ingestion/
├── main.py          # Entry point for document processing
├── preprocess.py    # Core preprocessing logic
├── utils.py         # Utility functions for file I/O and text processing
└── README.md        # This file
```

## Files

### `main.py`
Main entry point that orchestrates the ingestion pipeline:
- Loads configuration from `config.yaml`
- Creates the output `process_folder` if it doesn't exist
- Iterates through all `.docx` files in `raw_folder`
- Calls `pre_process_documents()` for each file

### `preprocess.py`
Contains core preprocessing logic:
- **`pre_process_documents(input_file, output_file, is_csv, is_json)`**
  - Reads `.docx` files and extracts content
  - Performs section-based chunking using markdown-like headers
  - Cleans text and extracts keywords from each chunk
  - Outputs to CSV and/or JSONL format

### `utils.py`
Helper functions for file operations and text processing:
- `read_docx_file(input_file)` - Reads `.docx` file content
- `write_to_csv(rows, output_file)` - Writes data to CSV format
- `write_to_jsonl(rows, output_file)` - Writes data to JSONL format
- `extract_keywords(text)` - Extracts keywords from text
- `clean_text(text)` - Normalizes and cleans text

## Configuration

Configure the ingestion module in `config.yaml`:

```yaml
raw_folder: path/to/raw/documents      # Input folder with .docx files
process_folder: path/to/processed      # Output folder for processed files
```

## Usage

Run the ingestion pipeline:

```bash
python app/src/ingestion/main.py
```

## Output Format

Processed documents are saved as CSV files with the following columns:
- `section` - Section (header level 2)
- `subsection` - Subsection (header level 3)
- `content` - Chunk text
- `keywords` - Extracted keywords

## Requirements

- Python 3.x
- `python-docx` - For reading `.docx` files
- `pyyaml` - For configuration loading

## Notes

- Input `.docx` files must be placed in the configured `raw_folder`
- Output files use the same filename as input (minus `.docx` extension)
- Processed files serve as input for the embedding module
- Text chunking is based on markdown-like headers (## and ###)
