# RAG with LangGraph

## Overview

This repository implements a Retrieval-Augmented Generation (RAG) workflow using `langgraph`, `langchain`, Redis, Chroma, and Hugging Face models. It is designed to route user questions between direct LLM answers and document retrieval, validate inputs, cache results, and detect hallucinations.

## Architecture

The system is built as a state graph with the following major stages:

1. Input validation
2. Session history loading
3. Question contextualization
4. Semantic cache lookup
5. Query routing (LLM vs RAG)
6. Document retrieval and grading
7. Response generation
8. Hallucination grounding and retries
9. History saving and cache update

The main workflow is defined in `graph.py`.

## Key Components

- `graph.py`: Defines the LangGraph state machine, nodes, and conditional routing logic.
- `state.py`: Contains the `GraphState` model used to carry data through the workflow.
- `nodes/`: Contains the graph nodes that implement each step in the workflow.
- `services/`: Contains shared service classes for LLM access, Redis history, embeddings, retrieval, and cache.
- `models/`: Pydantic response schemas and domain models used across services.
- `prompts/`: Prompt templates for guiding the LLM and router decisions.
- `ingestion/`: Document preprocessing workflow for building the knowledge base.
- `docker-compose.yml`: Defines the Redis service used for chat history and cache.

## Requirements

- Python 3.11+
- Redis (provided via `docker-compose.yml`)
- Hugging Face or OpenRouter API credentials for the LLM

## Dependencies

Primary dependencies are listed in `requirements.txt` and `pyproject.toml`:

- `langchain`
- `langgraph`
- `langchain-openai`
- `langchain-huggingface`
- `langchain-redis`
- `redis`
- `redisvl`
- `sentence-transformers`
- `chromadb`
- `python-docx`
- `pydantic`
- `dotenv`

## Setup

1. Create or activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Start Redis:

```powershell
docker compose up -d
```

4. Set environment variables:

- `HF_TOKEN`: Hugging Face API token for the OpenAI-compatible router endpoint.
- Optionally `OPENROUTER_API_KEY` if you switch to the alternative OpenRouter configuration.

Create a `.env` file in the project root if needed.

## Running the Workflow

The main execution entrypoint is `graph.py`.

```powershell
python graph.py
```

It will instantiate the workflow and invoke it with a sample question, printing the final state or result.

## Data Ingestion

Documents are ingested from the `data/raw` folder and processed into `data/processed` by the ingestion script.

```powershell
python ingestion/main.py
```

This script looks for `.docx` files in `data/raw`, preprocesses them, and saves transformed output in `data/processed`.

## Redis and Cache Behavior

- `services/redis.py` manages chat history using `RedisChatMessageHistory`.
- `services/cache.py` implements an embedding-based semantic cache using `redisvl`.
- The cache stores question-answer pairs and returns cached answers when a sufficiently similar question is asked.

## Customization

- `services/llm.py`: Configure the model, base URL, and API key.
- `services/embedding.py`: Change the embedding model for semantic similarity.
- `prompts/`: Adjust prompt templates for router, grading, and hallucination control.

## Notes

- `Dockerfile` is currently empty; only `docker-compose.yml` is configured for Redis.
- `folder_structure.md` documents the intended layout but may not exactly match the current repo contents.

## Project Structure

```text
rag_with_langgraph/
├── graph.py
├── state.py
├── services/
│   ├── cache.py
│   ├── embedding.py
│   ├── llm.py
│   ├── redis.py
│   └── retrieval.py
├── nodes/
│   ├── input_validation.py
│   ├── load_history.py
│   ├── contextualize.py
│   ├── semantic_cache.py
│   ├── router.py
│   ├── direct_generate.py
│   ├── retriever.py
│   ├── document_grade.py
│   ├── generate.py
│   ├── hallucination.py
│   ├── grounding_query_rewrite.py
│   ├── grading_query_rewrite.py
│   ├── fallback.py
│   ├── save_history.py
│   └── update_cache.py
├── models/
├── prompts/
├── ingestion/
├── data/
├── docker-compose.yml
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Future Enhancements

- Add a web/API entrypoint for interactive usage.
- Implement a complete Dockerfile and container build.
- Add tests for graph nodes and state transitions.
- Persist vector store to disk or an external DB.
