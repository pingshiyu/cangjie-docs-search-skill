# Cangjie documentation database

A script that searches through the Cangjie documentation. It is intended to be used as a skill by agents. Unlike grepping the Cangjie docs directly—which yields raw line matches and forces the agent to sift through many files—this tool returns pre-chunked, semantically relevant snippets (via vector search) or keyword-matched sections (via full-text search), so the agent gets compact, context-ready answers instead of sprawling grep output.

## For humans

**You just need to get an agent to follow the instructions in [AGENT_SETUP.md](AGENT_SETUP.md).** That document walks through Docker setup (Milvus, Elasticsearch), Python dependencies, index ingestion, and skill configuration. Once set up, the agent can use this search system via the configured Cursor skill.

## Setup

1. **Containers**
   - Milvus: run `milvus-standalone` (default port 19530).
   - Elasticsearch: run at `http://localhost:9200` with your API key.

2. **Python** (3.8+)
   ```bash
   cd cangjie_docs_db
   pip install -r requirements.txt
   ```
   Use `python3` and `pip3` if your system does not alias them to `python`/`pip`.

3. **Config** (optional)
   - Edit `config.py` or set env vars: `CANGJIE_DOCS_PATH`, `MILVUS_URI`, `ELASTICSEARCH_URL`, `ELASTICSEARCH_API_KEY`.

## Ingest

Populate both backends from the repo's `docs/` folder:

```bash
# Vector DB (Milvus) – embeds chunks with sentence-transformers
python ingest_milvus.py

# Full-text (Elasticsearch)
python ingest_elasticsearch.py
```

Chunks are built from all `.md` files under the docs path, split by sections with a max size so results stay compact for LLM context.

## Query (for LLMs)

Script to fetch relevant doc chunks for a given question. Choose **vector** (semantic) or **keyword** (full-text):

```bash
# Vector search (Milvus) – good for natural-language questions
python query.py --backend vector "How do I define a struct in Cangjie?"
python query.py -b vector -n 5 "generic types"

# Keyword search (Elasticsearch) – good for exact terms (e.g. "cjpm init")
python query.py --backend keyword "cjpm init"
python query.py -b keyword -n 3 "package import"
```

Output is formatted as context blocks (source path + text). Use `--raw` to get JSON lines instead.

## Example output

Default output is ready to paste into an LLM context:

```
--- Result 1 | Source: docs/dev-guide/source_en/struct/define_struct.md ---
...
--- Result 2 | Source: ...
```

This gives the model compact, relevant snippets instead of the full documentation.
