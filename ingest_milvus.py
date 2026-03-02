"""Populate Milvus with embedded Cangjie documentation chunks."""
from __future__ import annotations

import sys
from chunk import load_and_chunk_docs, DocChunk
from config import (
    DOCS_PATH,
    MILVUS_URI,
    MILVUS_COLLECTION,
    EMBEDDING_MODEL,
    EMBEDDING_DIM,
)


def get_embedding_model():
    """Lazy load sentence-transformers model."""
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(EMBEDDING_MODEL)


def embed_chunks(model, chunks: list[DocChunk]) -> list[list[float]]:
    """Compute embeddings for chunk texts (normalized for cosine similarity)."""
    texts = [c.text for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True, normalize_embeddings=True)
    return embeddings.tolist()


def create_collection(drop_if_exists: bool = True):
    """Create collection with schema; optionally drop existing for re-ingest."""
    from pymilvus import Collection, CollectionSchema, FieldSchema, DataType, utility

    if drop_if_exists and utility.has_collection(MILVUS_COLLECTION):
        utility.drop_collection(MILVUS_COLLECTION)

    if utility.has_collection(MILVUS_COLLECTION):
        return Collection(MILVUS_COLLECTION)

    schema = CollectionSchema(
        fields=[
            FieldSchema(name="id", dtype=DataType.VARCHAR, max_length=512, is_primary=True),
            FieldSchema(name="source_path", dtype=DataType.VARCHAR, max_length=512),
            FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=512),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=EMBEDDING_DIM),
        ],
        description="Cangjie documentation chunks for semantic search",
    )
    coll = Collection(name=MILVUS_COLLECTION, schema=schema)
    index_params = {
        "metric_type": "IP",  # inner product = cosine when vectors are normalized
        "index_type": "IVF_FLAT",
        "params": {"nlist": 128},
    }
    coll.create_index(field_name="vector", index_params=index_params)
    return coll


def main():
    from pymilvus import connections, utility, Collection

    print("Loading documentation chunks...")
    chunks = load_and_chunk_docs(DOCS_PATH)
    if not chunks:
        print("No chunks found. Check DOCS_PATH:", DOCS_PATH, file=sys.stderr)
        sys.exit(1)
    print(f"Loaded {len(chunks)} chunks.")

    print("Loading embedding model...")
    model = get_embedding_model()
    print("Computing embeddings...")
    vectors = embed_chunks(model, chunks)

    print("Connecting to Milvus...")
    connections.connect(uri=MILVUS_URI)
    coll = create_collection(drop_if_exists=True)
    data = [
        [c.id for c in chunks],
        [c.source_path for c in chunks],
        [c.title for c in chunks],
        [c.text for c in chunks],
        vectors,
    ]
    print("Inserting into Milvus...")
    coll.insert(data)
    coll.flush()
    coll.load()
    print("Done. Milvus collection", MILVUS_COLLECTION, "ready for vector search.")


if __name__ == "__main__":
    main()
