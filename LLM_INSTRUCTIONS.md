# Cangjie docs DB — instructions for LLMs

Set up Python environment: `source /Users/jacob/projects/python-venvs/llms/bin/activate`

**Purpose:** Return relevant Cangjie language documentation chunks for context. Use this instead of dumping full docs.

**Location:** `pbt-dev/cangjie_docs_db/`

## Query (main entrypoint)

Run `query.py` from `cangjie_docs_db`:

- **Vector search** (semantic; use for conceptual questions):
  ```bash
  python3 query.py --backend vector "How do I use generics?"
  ```
- **Keyword search** (exact terms, e.g. commands/APIs):
  ```bash
  python3 query.py --backend keyword "cjpm init"
  ```

**Options:** `-n 5` = number of chunks (default 5). `--raw` = JSON lines.

**Output:** Formatted text blocks with `Source: <path>` and chunk text. Feed this directly into the user’s context.

## Prerequisites

- Python 3.8+, deps: `pip install -r requirements.txt` in `cangjie_docs_db`.
- **Vector:** Milvus running (e.g. `milvus-standalone`).
- **Keyword:** Elasticsearch at `http://localhost:9200` with API key (see `config.py` or env `ELASTICSEARCH_API_KEY`).

## (Re)building the indexes

Only if docs or config changed:

- `python3 ingest_milvus.py` — populate Milvus (needs embedding model download first run).
- `python3 ingest_elasticsearch.py` — populate Elasticsearch.

**Config:** `config.py`; override via env: `CANGJIE_DOCS_PATH`, `MILVUS_URI`, `ELASTICSEARCH_URL`, `ELASTICSEARCH_API_KEY`.
