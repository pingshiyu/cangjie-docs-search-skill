# Cangjie Docs DB — Agent Setup Instructions

This document instructs AI agents how to set up the Cangjie documentation search system as a Cursor skill on a new machine. It covers dependency preparation (Docker, Elasticsearch, Milvus), Python setup, index ingestion, and skill configuration.

**Path convention:** In this doc, "the project" or "project root" means the folder that contains `query.py`, `ingest_milvus.py`, `ingest_elasticsearch.py`, `config.py`, and the `docs/` directory. It may be named `cangjie-docs-search-skill`, `cangjie_docs_db`, or similar. Replace any `/path/to/cangjie_docs_db` (or `{{CANGJIE_DOCS_DB_PATH}}`) with the **absolute** path to that folder on the machine you are setting up.

---

**For the agent:** Before executing any setup steps, verify that all prerequisites below are available on the machine (e.g. Docker installed and running, Python 3.8+ available). **If any dependency is missing or unavailable, STOP and DO NOT continue.** Inform the user exactly what is missing and that they must install or start it before setup can proceed. Do not attempt to work around missing dependencies or proceed with a partial setup.

If you cannot write to the user's home directory (e.g. sandbox restrictions), use **project-local paths** instead: put Milvus under `<project>/milvus-standalone`, use a venv at `<project>/.venv`, and create `SKILL.md` in the project and tell the user to copy it to `~/.cursor/skills/cangjie-docs-search/`. See the relevant sections and **Troubleshooting** for details.

---

## Prerequisites

- **Docker** — installed and running. On macOS (Docker Desktop), allocate at least 4–8 GB memory (Settings > Resources).
- **Python 3.8+** — for running the query and ingest scripts.
- **~2 GB disk** — for Docker images, indexes, and the embedding model. The first `pip install` downloads large packages (e.g. PyTorch, sentence-transformers); allow several minutes and ensure network access for the install.
- **Elasticsearch 8.x server** — the Python client must match: use `elasticsearch>=8.0.0,<9`. The repo `requirements.txt` pins this; do not upgrade to client 9.x while the server is 8.x, or ingest/query will fail with a version header error.

---

## 1. Docker Dependencies

### 1.1 Milvus Standalone

Milvus provides vector search for semantic queries.

1. Create a directory and download the Milvus standalone Docker Compose file. Use a path the agent can write to (if `~/milvus-standalone` is not writable, use the project: `<project>/milvus-standalone`).

   ```bash
   mkdir -p ~/milvus-standalone && cd ~/milvus-standalone
   wget https://github.com/milvus-io/milvus/releases/download/v2.4.23/milvus-standalone-docker-compose.yml -O docker-compose.yml
   ```

   If `wget` is unavailable, use curl:

   ```bash
   curl -L -o docker-compose.yml https://github.com/milvus-io/milvus/releases/download/v2.4.23/milvus-standalone-docker-compose.yml
   ```

   **Alternative (project-local):** If the agent cannot write to the user's home:

   ```bash
   mkdir -p /path/to/project/milvus-standalone && cd /path/to/project/milvus-standalone
   curl -sL -o docker-compose.yml https://github.com/milvus-io/milvus/releases/download/v2.4.23/milvus-standalone-docker-compose.yml
   ```

2. Start Milvus (requires network for pulling images; first run may take 1–2 minutes):

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

3. Verify (Elasticsearch may take 10–20 seconds to become ready after `docker run`):

   ```bash
   curl http://localhost:9200
   ```

   (Use `https` and credentials if security is enabled.)

---

## 2. Python Environment

1. Create and activate a virtual environment. Prefer a path the agent can write to.

   **Option A — User home (typical):**

   ```bash
   python3 -m venv ~/venvs/cangjie-docs-db
   source ~/venvs/cangjie-docs-db/bin/activate
   ```

   **Option B — Project-local (self-contained; use when home is not writable):**

   ```bash
   cd /path/to/project
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   On Windows: use `Scripts\activate` (e.g. `~\venvs\cangjie-docs-db\Scripts\activate` or `\.venv\Scripts\activate`).

2. Install dependencies (requires network; first install pulls large packages and may take 2–5 minutes or timeout—retry with same command or `pip install --resume-retries 5 -r requirements.txt`):

   ```bash
   pip install -r /path/to/project/requirements.txt
   ```

   Replace `/path/to/project` with the absolute path to the project folder. Keep `requirements.txt` as-is: it pins `elasticsearch>=8.0.0,<9` for compatibility with the ES 8.x server. Do not upgrade to `elasticsearch>=9`.

   The first run of `ingest_milvus.py` (and the first vector query) will download the embedding model (`all-MiniLM-L6-v2`, ~90 MB) via sentence-transformers if not already cached.

---

## 3. Configuration

Set environment variables (or edit `config.py`) to match your setup:

| Variable | Description | Default |
|----------|-------------|---------|
| `CANGJIE_DOCS_PATH` | Path to docs (optional; repo includes `docs/`) | `<project>/docs` (auto from config) |
| `MILVUS_URI` | Milvus connection URI | `http://localhost:19530` |
| `ELASTICSEARCH_URL` | Elasticsearch base URL | `http://localhost:9200` or `https://localhost:9200` if security enabled |
| `ELASTICSEARCH_API_KEY` | **Your own** Elasticsearch API key (required if security enabled; omit or empty if security disabled) | None—you must generate one |
| `EMBEDDING_MODEL` | Sentence-transformers model for embeddings | `all-MiniLM-L6-v2` |
| `HF_HOME` / `TRANSFORMERS_CACHE` | Hugging Face cache dir (optional) | `~/.cache/huggingface` — set to a writable path if that fails (see Troubleshooting) |

**API keys:** Always generate and use your own Elasticsearch API key. Never rely on hardcoded defaults or keys from documentation.

The repo includes a `docs/` folder; the default config uses it automatically. Override only if needed:

```bash
export CANGJIE_DOCS_PATH=/path/to/project/docs
```

**Hugging Face cache:** If you get a permission error writing to `~/.cache/huggingface` (common in sandboxes or restricted envs), set a writable cache inside the project before running ingest or vector query:

```bash
mkdir -p /path/to/project/.cache/huggingface
export HF_HOME=/path/to/project/.cache/huggingface
export TRANSFORMERS_CACHE=/path/to/project/.cache/huggingface
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

From the project directory, with the Python venv activated. Ensure Docker containers (Milvus, Elasticsearch) are running and that the agent has network access if localhost connections are restricted.

```bash
cd /path/to/project

# Optional: use project-local Hugging Face cache if ~/.cache is not writable
export HF_HOME=/path/to/project/.cache/huggingface
export TRANSFORMERS_CACHE=/path/to/project/.cache/huggingface
mkdir -p .cache/huggingface

# Populate Milvus (vector search) — first run downloads the embedding model (~90 MB); allow 1–2 min
python ingest_milvus.py

# Populate Elasticsearch (keyword search) — requires connection to localhost:9200
python ingest_elasticsearch.py
```

Both scripts read from `CANGJIE_DOCS_PATH` (default: `<project>/docs`) and create or overwrite their indexes. Re-run after docs or config changes. If Elasticsearch ingest fails with a 400 "Accept version must be 8 or 7, but found 9", ensure the client is 8.x (see Troubleshooting).

---

## 5. Cursor Skill Setup

Create a Cursor skill so agents can invoke the query script automatically. If the agent cannot write to `~/.cursor/skills/` (e.g. permission or sandbox), create `SKILL.md` in the project root instead and inform the user to copy it to `~/.cursor/skills/cangjie-docs-search/SKILL.md` or to create a symlink.

1. Create the skill directory (or skip and write SKILL.md in the project):

   ```bash
   mkdir -p ~/.cursor/skills/cangjie-docs-search
   ```

2. Create `~/.cursor/skills/cangjie-docs-search/SKILL.md` (or `<project>/SKILL.md` for the user to copy). Replace the placeholders:

   - `{{CANGJIE_DOCS_DB_PATH}}` — absolute path to the project folder (e.g. `/Users/you/projects/cangjie/cangjie-docs-search-skill`)
   - `{{PYTHON_VENV_ACTIVATE}}` — command to activate the venv (e.g. `source /Users/you/venvs/cangjie-docs-db/bin/activate` or `source /path/to/project/.venv/bin/activate`)

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

   - **Python:** Ensure the venv is activated and has deps: `pip install -r {{CANGJIE_DOCS_DB_PATH}}/requirements.txt`. For Milvus and Elasticsearch prerequisites, see `{{CANGJIE_DOCS_DB_PATH}}/AGENT_SETUP.md`.
   - **Config:** `{{CANGJIE_DOCS_DB_PATH}}/config.py`; override via env: `CANGJIE_DOCS_PATH`, `MILVUS_URI`, `ELASTICSEARCH_URL`, `ELASTICSEARCH_API_KEY`. For vector search, if the default Hugging Face cache is not writable, set `HF_HOME` and `TRANSFORMERS_CACHE` to a writable path (e.g. `{{CANGJIE_DOCS_DB_PATH}}/.cache/huggingface`).

   ## If the script is unavailable

   If the query script cannot be run (missing deps, Milvus/Elasticsearch down), say so and avoid guessing Cangjie semantics. Prefer stopping or asking the user to fix the environment rather than proceeding without docs.
   ```

---

## 6. Troubleshooting

| Issue | Cause | Fix |
|-------|--------|-----|
| **PermissionError** or **Permission denied** at `~/.cache/huggingface` | Default Hugging Face cache not writable (e.g. sandbox, multi-user). | Create a writable cache and set env before running ingest or vector query: `mkdir -p <project>/.cache/huggingface` and `export HF_HOME=<project>/.cache/huggingface` and `export TRANSFORMERS_CACHE=$HF_HOME`. |
| **joblib** "Permission denied" / "will operate in serial mode" during `ingest_milvus.py` | joblib cannot use multiprocessing (e.g. sandbox or restricted env). | Safe to ignore. Ingest continues in single-process mode and still completes; no fix needed. |
| **Elasticsearch 400** "Accept version must be 8 or 7, but found 9" or "Invalid media-type" | Python client 9.x sends a header ES 8.x rejects. | Use client 8.x: `pip install 'elasticsearch>=8,<9'`. Ensure `requirements.txt` has `elasticsearch>=8.0.0,<9` and reinstall. |
| **Connection refused** to `localhost:9200` or `localhost:19530` | Containers not running, or agent has no network access to localhost. | Run `docker ps` and start Milvus/ES if needed. In restricted environments, run ingest/query with network permission so localhost is reachable. |
| **pip install** times out or "incomplete-download" (e.g. torch) | Large downloads (~900 MB+); slow or interrupted connection. | Retry with network enabled and a long timeout. Use `pip install --resume-retries 5 -r requirements.txt` on retry. |
| **Cannot create** `~/milvus-standalone` or `~/.cursor/skills/...` | Agent cannot write to user home (e.g. sandbox). | Use project-local paths: `<project>/milvus-standalone`, `<project>/.venv`, and create `SKILL.md` in the project; tell the user to copy it to `~/.cursor/skills/cangjie-docs-search/`. |

---

## 7. Verification

With venv activated and both containers running (set `HF_HOME`/`TRANSFORMERS_CACHE` if you use a project cache for vector):

```bash
# Vector search (Milvus) — may load embedding model on first run
python3 /path/to/project/query.py --backend vector -n 2 "How do I use generics?"

# Keyword search (Elasticsearch)
python3 /path/to/project/query.py --backend keyword -n 2 "cjpm init"
```

Expected output: formatted blocks with `--- Result N | Source: <path> ---` followed by chunk text. If no results or connection errors, check that Milvus and Elasticsearch are running, that ingestion completed successfully, and (for ES) that the client is 8.x.

---

## Summary Flow

```
Prerequisites (Docker, Python; requirements.txt keeps elasticsearch 8.x)
    ↓
Start Milvus (docker compose up -d) — use project/milvus-standalone if ~ not writable
Start Elasticsearch (docker run ...)
    ↓
Create Python venv (e.g. project/.venv if home not writable), pip install -r requirements.txt (allow time/retry)
    ↓
Set optional env: CANGJIE_DOCS_PATH; HF_HOME/TRANSFORMERS_CACHE if cache not writable
    ↓
python ingest_milvus.py  [set HF_HOME if needed]
python ingest_elasticsearch.py  [need network; use ES client 8.x if 400]
    ↓
Create SKILL.md (in ~/.cursor/skills/cangjie-docs-search/ or in project for user to copy)
    ↓
Verify: query.py --backend vector "..." and --backend keyword "..."
```

If anything fails, see **§6 Troubleshooting**.
