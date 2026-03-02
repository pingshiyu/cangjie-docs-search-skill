"""Configuration for Cangjie docs database (Milvus + Elasticsearch)."""
import os

# Path to Cangjie documentation (markdown files). Repo includes docs/.
_DEFAULT_DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
DOCS_PATH = os.environ.get("CANGJIE_DOCS_PATH", _DEFAULT_DOCS)

# Milvus standalone (default container port)
MILVUS_URI = os.environ.get("MILVUS_URI", "http://localhost:19530")
MILVUS_COLLECTION = "cangjie_docs"

# Elasticsearch
ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL", "http://localhost:9200")
# Elasticsearch API key. Generate your own via: POST /_security/api_key
# Required when security enabled; leave unset/empty when xpack.security.enabled=false
ELASTICSEARCH_API_KEY = os.environ.get("ELASTICSEARCH_API_KEY") or None
ELASTICSEARCH_INDEX = "cangjie_docs"

# Embedding model for vector search (sentence-transformers)
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
# Dimension for all-MiniLM-L6-v2
EMBEDDING_DIM = 384

# Chunking
MAX_CHUNK_CHARS = 2000
CHUNK_OVERLAP_CHARS = 200
