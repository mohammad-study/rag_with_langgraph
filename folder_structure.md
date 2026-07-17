production-rag/
│
├── app.py
├── graph.py
├── state.py
├── config.py
├── requirements.txt
│
├── nodes/
│   ├── input_validation.py
│   ├── load_history.py
│   ├── contextualize_question.py
│   ├── cache_lookup.py
│   ├── router.py
│   ├── retrieve.py
│   ├── grade_documents.py
│   ├── rewrite_query.py
│   ├── generate.py
│   ├── hallucination_check.py
│   ├── save_history.py
│   └── update_cache.py
│
├── prompts/
│   ├── router.txt
│   ├── rewrite.txt
│   ├── grader.txt
│   ├── generation.txt
│   └── hallucination.txt
│
├── services/
│   ├── llm.py
│   ├── vectorstore.py
│   ├── cache.py
│   └── history.py
│
├── api/
│   └── routes.py
│
├── tests/
│
└── docker/