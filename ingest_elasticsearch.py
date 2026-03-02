"""Populate Elasticsearch with Cangjie documentation chunks for full-text search."""
from __future__ import annotations

import sys
from chunk import load_and_chunk_docs
from config import DOCS_PATH, ELASTICSEARCH_URL, ELASTICSEARCH_API_KEY, ELASTICSEARCH_INDEX


def create_index(es):
    """Create index with mapping suitable for doc chunks (full-text and keyword)."""
    if es.indices.exists(index=ELASTICSEARCH_INDEX):
        es.indices.delete(index=ELASTICSEARCH_INDEX)
    es.indices.create(
        index=ELASTICSEARCH_INDEX,
        mappings={
            "properties": {
                "id": {"type": "keyword"},
                "source_path": {"type": "keyword"},
                "title": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                "text": {"type": "text"},
            }
        },
        settings={
            "number_of_shards": 1,
            "number_of_replicas": 0,
        },
    )


def main():
    from elasticsearch import Elasticsearch

    print("Loading documentation chunks...")
    chunks = load_and_chunk_docs(DOCS_PATH)
    if not chunks:
        print("No chunks found. Check DOCS_PATH:", DOCS_PATH, file=sys.stderr)
        sys.exit(1)
    print(f"Loaded {len(chunks)} chunks.")

    print("Connecting to Elasticsearch...")
    # Disable cert verification for localhost (e.g. Docker)
    verify_certs = "localhost" not in ELASTICSEARCH_URL
    es_kwargs = {"verify_certs": verify_certs}
    if ELASTICSEARCH_API_KEY:
        es_kwargs["api_key"] = ELASTICSEARCH_API_KEY
    es = Elasticsearch(ELASTICSEARCH_URL, **es_kwargs)
    try:
        es.info()
    except Exception as e:
        print("Elasticsearch connection failed:", e, file=sys.stderr)
        sys.exit(1)

    print("Creating index and indexing chunks...")
    create_index(es)
    for i, c in enumerate(chunks):
        es.index(
            index=ELASTICSEARCH_INDEX,
            id=c.id,
            document={
                "id": c.id,
                "source_path": c.source_path,
                "title": c.title,
                "text": c.text,
            },
        )
        if (i + 1) % 50 == 0:
            print(f"  Indexed {i + 1}/{len(chunks)}")
    es.indices.refresh(index=ELASTICSEARCH_INDEX)
    print("Done. Elasticsearch index", ELASTICSEARCH_INDEX, "ready for full-text search.")


if __name__ == "__main__":
    main()
