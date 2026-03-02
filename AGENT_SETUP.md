# Cangjie Docs DB — Agent Setup Instructions

This document instructs AI agents how to set up the Cangjie documentation search system as a Cursor skill on a new machine. It covers dependency preparation (Docker, Elasticsearch, Milvus), Python setup, index ingestion, and skill configuration.

## Prerequisites

- **Docker** — installed and running. On macOS (Docker Desktop), allocate at least 4–8 GB memory (Settings > Resources).
- **Python 3.8+** — for running the query and ingest scripts.
- **~2 GB disk** — for Docker images, indexes, and the embedding model (downloaded on first run).

---

## 1. Docker Dependencies

### 1.1 Milvus Standalone

Milvus provides vector search for semantic queries.

1. Create a directory and download the Milvus standalone Docker Compose file:

   ```bash
   mkdir -p ~/milvus-standalone && cd ~/milvus-standalone
   wget https://github.com/milvus-io/milvus/releases/download/v2.4.23/milvus-standalone-docker-compose.yml -O docker-compose.yml
   ```

   If `wget` is unavailable, use curl:

   ```bash
   curl -L -o docker-compose.yml https://github.com/milvus-io/milvus/releases/download/v2.4.23/milvus-standalone-docker-compose.yml
   ```

2. Start Milvus:

   ```bash
   docker compose up -d
   ```

   (Use `docker-compose up -d` if you have Docker Compose V1.)

3. Verify:

   ```bash
   docker ps | grep milvus
   ```

   Milvus exposes port **19530** (gRPC). The default `MILVUS_URI` is `http://localhost:19530`.

### 1.2 Elasticsearch 8

Elasticsearch provides full-text (keyword) search.

**Important:** If you use Elasticsearch with security enabled, you **must generate your own API key** and set it via `ELASTICSEARCH_API_KEY`. Do not use any hardcoded or example keys from config files, documentation, or other machines—each setup must create and use its own credentials.

1. Create the Docker network:

   ```bash
   docker network create elastic
   ```

2. Pull and run Elasticsearch.

   **Option A — Security disabled (simpler for local dev):**

   ```bash
   docker run -d --name es01 --net elastic -p 9200:9200 \
     -e "discovery.type=single-node" \
     -e "xpack.security.enabled=false" \
     -m 1GB \
     docker.elastic.co/elasticsearch/elasticsearch:8.18.8
   ```

   With security disabled, use `http://localhost:9200` and leave `ELASTICSEARCH_API_KEY` unset (or empty). The scripts will connect without authentication.

   **Option B — Security enabled (recommended for shared environments):**

   ```bash
   docker run -d --name es01 --net elastic -p 9200:9200 \
     -e "discovery.type=single-node" \
     -e "ELASTIC_PASSWORD=your_secure_password" \
     -m 1GB \
     docker.elastic.co/elasticsearch/elasticsearch:8.18.8
   ```

   - Save the generated `elastic` password from the container logs, or set `ELASTIC_PASSWORD` as above (use a strong password).
   - Elasticsearch 8 uses HTTPS by default; for localhost with self-signed certs, the scripts disable cert verification.
   - **Generate your own API key** (replace `your_secure_password` with your actual elastic password):

     ```bash
     curl -k -u elastic:your_secure_password -X POST "https://localhost:9200/_security/api_key" \
       -H "Content-Type: application/json" \
       -d '{"name": "cangjie-docs-db-<your-machine-or-user>"}'
     ```

   - From the JSON response, copy the `encoded` value—this is **your** API key. Store it securely (e.g. in env or a secrets manager). Set it when running scripts: `export ELASTICSEARCH_API_KEY="<your-encoded-key>"`. Also set `ELASTICSEARCH_URL=https://localhost:9200`.
   - Do not commit or share this key. Do not use API keys from examples or other machines.

3. Verify:

   ```bash
   curl http://localhost:9200
   ```

   (Use `https` and credentials if security is enabled.)

---

## 2. Python Environment

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv ~/venvs/cangjie-docs-db
   source ~/venvs/cangjie-docs-db/bin/activate
   ```

   On Windows: `~\venvs\cangjie-docs-db\Scripts\activate`

2. Install dependencies:

   ```bash
   pip install -r /path/to/cangjie_docs_db/requirements.txt
   ```

   Replace `/path/to/cangjie_docs_db` with the actual path to the `cangjie_docs_db` folder.

   The first run of `ingest_milvus.py` will download the embedding model (`all-MiniLM-L6-v2`, ~90 MB) via sentence-transformers.

---

## 3. Configuration

Set environment variables (or edit `config.py`) to match your setup:

| Variable | Description | Default |
|----------|-------------|---------|
| `CANGJIE_DOCS_PATH` | Path to docs (optional; repo includes `docs/`) | `cangjie_docs_db/docs` (relative to config) |
| `MILVUS_URI` | Milvus connection URI | `http://localhost:19530` |
| `ELASTICSEARCH_URL` | Elasticsearch base URL | `http://localhost:9200` or `https://localhost:9200` if security enabled |
| `ELASTICSEARCH_API_KEY` | **Your own** Elasticsearch API key (required if security enabled; omit or empty if security disabled) | None—you must generate one |
| `EMBEDDING_MODEL` | Sentence-transformers model for embeddings | `all-MiniLM-L6-v2` |

**API keys:** Always generate and use your own Elasticsearch API key. Never rely on hardcoded defaults or keys from documentation.

The repo includes a `docs/` folder; the default config uses it automatically. Override only if needed:

```bash
export CANGJIE_DOCS_PATH=/path/to/cangjie_docs_db/docs
```

For Elasticsearch with security disabled:

```bash
export ELASTICSEARCH_API_KEY=
```

For Elasticsearch with security enabled (you must use a key you generated yourself):

```bash
export ELASTICSEARCH_API_KEY="<paste-your-encoded-api-key-here>"
export ELASTICSEARCH_URL="https://localhost:9200"
```

---

## 4. Index Ingestion

From the `cangjie_docs_db` directory, with the Python venv activated:

```bash
cd /path/to/cangjie_docs_db

# Populate Milvus (vector search) — first run downloads the embedding model
python ingest_milvus.py

# Populate Elasticsearch (keyword search)
python ingest_elasticsearch.py
```

Both scripts read from `CANGJIE_DOCS_PATH` and create or overwrite their indexes. Re-run after docs or config changes.

---

## 5. Cursor Skill Setup

Create a Cursor skill so agents can invoke the query script automatically.

1. Create the skill directory:

   ```bash
   mkdir -p ~/.cursor/skills/cangjie-docs-search
   ```

2. Create `~/.cursor/skills/cangjie-docs-search/SKILL.md` with the following content. Replace the placeholders:

   - `{{CANGJIE_DOCS_DB_PATH}}` — absolute path to `cangjie_docs_db` (e.g. `/Users/you/projects/pbt-dev/cangjie_docs_db`)
   - `{{PYTHON_VENV_ACTIVATE}}` — command to activate the venv (e.g. `source /Users/you/venvs/cangjie-docs-db/bin/activate`)

   ```markdown
   ---
   name: cangjie-docs-search
   description: Queries Cangjie language documentation via vector (Milvus) or keyword (Elasticsearch) search. Use when writing or reviewing Cangjie code, answering Cangjie language or API questions, or when the user or project rules mention Cangjie documentation. Prefer this over dumping full docs.
   ---

   # Cangjie documentation search

   Retrieve relevant Cangjie doc chunks by running the query script at `{{CANGJIE_DOCS_DB_PATH}}/query.py`. Use the results as context instead of loading full documentation.

   ## When to use

   - User asks how to do something in Cangjie (syntax, APIs, tooling).
   - Writing or editing Cangjie (`.cj`) code and you need language or library details.
   - Existence of `cjpm.toml` file within the root structure.
   - Project rules (e.g. `.cursorrules`) say to use Cangjie documentation or the docs search script.

   ## How to run

   1. **Activate the Python venv** (required for dependencies):

      ```bash
      {{PYTHON_VENV_ACTIVATE}}
      ```

   2. **Run the query script** (from any directory):

      ```bash
      python3 {{CANGJIE_DOCS_DB_PATH}}/query.py --backend <vector|keyword> "your query"
      ```

   Examples (with venv already activated):

   ```bash
   python3 {{CANGJIE_DOCS_DB_PATH}}/query.py --backend vector "How do I use generics?"
   python3 {{CANGJIE_DOCS_DB_PATH}}/query.py --backend keyword "cjpm init"
   ```

   - **Vector** (`--backend vector`): semantic/conceptual questions (e.g. "How do I define a struct?", "file I/O").
   - **Keyword** (`--backend keyword`): exact terms, commands, API names (e.g. "cjpm init", "std.unittest").

   **Options:** `-n 5` = number of chunks (default 5). `--raw` = JSON lines.

   **Output:** Formatted blocks with `Source: <path>` and chunk text. Use this output directly in your response or as context for the user.

   ## Setup and config

   - **Python:** Ensure the venv is activated and has `cangjie_docs_db` deps: `pip install -r {{CANGJIE_DOCS_DB_PATH}}/requirements.txt`. For Milvus and Elasticsearch prerequisites, see `{{CANGJIE_DOCS_DB_PATH}}/AGENT_SETUP.md`.
   - **Config:** `{{CANGJIE_DOCS_DB_PATH}}/config.py`; override via env: `CANGJIE_DOCS_PATH`, `MILVUS_URI`, `ELASTICSEARCH_URL`, `ELASTICSEARCH_API_KEY`.

   ## If the script is unavailable

   If the query script cannot be run (missing deps, Milvus/Elasticsearch down), say so and avoid guessing Cangjie semantics. Prefer stopping or asking the user to fix the environment rather than proceeding without docs.
   ```

---

## 6. Verification

With venv activated and both containers running:

```bash
# Vector search (Milvus)
python3 /path/to/cangjie_docs_db/query.py --backend vector "How do I use generics?"

# Keyword search (Elasticsearch)
python3 /path/to/cangjie_docs_db/query.py --backend keyword "cjpm init"
```

Expected output: formatted blocks with `--- Result N | Source: <path> ---` followed by chunk text. If no results or connection errors, check that Milvus and Elasticsearch are running and that ingestion completed successfully.

---

## Summary Flow

```
Prerequisites (Docker, Python)
    ↓
Start Milvus (docker compose up -d)
Start Elasticsearch (docker run ...)
    ↓
Create Python venv, pip install -r requirements.txt
    ↓
Set optional env vars (CANGJIE_DOCS_PATH defaults to repo docs/)
    ↓
python ingest_milvus.py
python ingest_elasticsearch.py
    ↓
Create ~/.cursor/skills/cangjie-docs-search/SKILL.md with local paths
    ↓
Verify with query.py --backend vector/keyword "test query"
```
