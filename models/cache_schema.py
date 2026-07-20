CACHE_SCHEMA = {
    "index": {
        "name": "semantic_cache",
        "prefix": "cache",
        "storage_type": "json"
    },
    "fields": [
        {
            "name": "question",
            "type": "text"
        },
        {
            "name": "answer",
            "type": "text"
        },
        {
            "name": "embedding",
            "type": "vector",
            "attrs": {
                "dims": 384,
                "distance_metric": "cosine",
                "algorithm": "hnsw",
                "datatype": "float32"
            }
        }
    ]
}