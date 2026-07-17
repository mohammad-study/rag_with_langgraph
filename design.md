                     START
                        │
                        ▼
              Input Validation
                        │
                        ▼
               Load Chat History
                        │
                        ▼
          Contextualize Question
                        │
                        ▼
               Semantic Cache
                │            │
          Cache Hit      Cache Miss
                │            │
                │            ▼
                │         Router
                │      ┌────┴─────┐
                │      │          │
                │      ▼          ▼
                │   Retrieve   Direct LLM
                │      │
                │      ▼
                │ Grade Documents
                │   │         │
                │ Good      Rewrite
                │   │         │
                │   └────┬────┘
                │        ▼
                │    Generate
                │        │
                │        ▼
                │ Hallucination
                │    │       │
                │  Pass    Retry
                │    │       │
                └────┴───────┘
                        │
                        ▼
               Save Chat History
                        │
                        ▼
                Update Cache
                        │
                        ▼
                       END