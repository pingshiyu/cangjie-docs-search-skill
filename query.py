#!/usr/bin/env python3
"""
Query Cangjie documentation via vector search (Milvus) or full-text search (Elasticsearch).
Returns compact, relevant chunks for LLM context.

Usage:
  python query.py --backend vector "How do I define a struct in Cangjie?"
  python query.py --backend keyword "cjpm init"
  python query.py -b vector -n 5 "generic types"
"""
from __future__ import annotations

import argparse
import sys

from config import (
    MILVUS_URI,
    MILVUS_COLLECTION,
    ELASTICSEARCH_URL,
    ELASTICSEARCH_API_KEY,
    ELASTICSEARCH_INDEX,
    EMBEDDING_MODEL,
    EMBEDDING_DIM,
)


def search_milvus(query: str, top_k: int = 5) -> list[dict]:
    """Vector search: embed query and return top_k similar chunks."""
    from pymilvus import connections, Collection
    from sentence_transformers import SentenceTransformer

    connections.connect(uri=MILVUS_URI)
    coll = Collection(MILVUS_COLLECTION)
    coll.load()
    model = SentenceTransformer(EMBEDDING_MODEL)
    qvec = model.encode([query], normalize_embeddings=True).tolist()
    results = coll.search(
        data=qvec,
        anns_field="vector",
        param={"metric_type": "IP", "params": {"nprobe": 16}},
        limit=top_k,
        output_fields=["source_path", "title", "text"],
    )
    out = []
    for hits in results:
        for h in hits:
            out.append({
                "source_path": h.entity.get("source_path", ""),
                "title": h.entity.get("title", ""),
                "text": h.entity.get("text", ""),
                "score": float(h.score),
            })
    return out


def search_elasticsearch(query: str, top_k: int = 5) -> list[dict]:
    """Full-text search: return top_k matching chunks."""
    from elasticsearch import Elasticsearch

    verify_certs = "localhost" not in ELASTICSEARCH_URL
    es = Elasticsearch(
        ELASTICSEARCH_URL,
        api_key=ELASTICSEARCH_API_KEY,
        verify_certs=verify_certs,
    )
    resp = es.search(
        index=ELASTICSEARCH_INDEX,
        size=top_k,
        source=["source_path", "title", "text"],
        query={
            "multi_match": {
                "query": query,
                "fields": ["title^2", "text"],
                "type": "best_fields",
            }
        },
    )
    out = []
    for hit in resp["hits"]["hits"]:
        s = hit.get("_source", {})
        out.append({
            "source_path": s.get("source_path", ""),
            "title": s.get("title", ""),
            "text": s.get("text", ""),
            "score": float(hit.get("_score", 0)),
        })
    return out


def format_for_llm(results: list[dict]) -> str:
    """Format search results as a single context string for an LLM."""
    blocks = []
    for i, r in enumerate(results, 1):
        blocks.append(f"--- Result {i} | Source: {r['source_path']} ---\n{r['text']}")
    return "\n\n".join(blocks)


def main():
    parser = argparse.ArgumentParser(
        description="Query Cangjie docs: vector (Milvus) or keyword (Elasticsearch) search."
    )
    parser.add_argument(
        "query",
        nargs="+",
        help="Search query (words or natural language for vector).",
    )
    parser.add_argument(
        "-b", "--backend",
        choices=["vector", "keyword"],
        default="vector",
        help="Backend: 'vector' (Milvus) or 'keyword' (Elasticsearch).",
    )
    parser.add_argument(
        "-n", "--top-k",
        type=int,
        default=5,
        help="Number of chunks to return (default 5).",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Print raw JSON lines instead of LLM context.",
    )
    args = parser.parse_args()
    query = " ".join(args.query).strip()
    if not query:
        print("Please provide a non-empty query.", file=sys.stderr)
        sys.exit(1)

    try:
        if args.backend == "vector":
            results = search_milvus(query, top_k=args.top_k)
        else:
            results = search_elasticsearch(query, top_k=args.top_k)
    except Exception as e:
        print(f"Search failed: {e}", file=sys.stderr)
        sys.exit(1)

    if not results:
        print("No results found.", file=sys.stderr)
        sys.exit(0)

    if args.raw:
        import json
        for r in results:
            print(json.dumps(r, ensure_ascii=False))
    else:
        print(format_for_llm(results))


if __name__ == "__main__":
    main()
