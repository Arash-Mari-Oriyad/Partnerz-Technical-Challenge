# Intercom Help Center Retrieval-Augmented Q&A Agent

This project implements a retrieval-augmented question-answering (RAG) agent over the exported Intercom Help Center (`articles.json`). It supports fast and accurate answers to user questions, grounded in the help center’s knowledge base.

---

## Features

- **Data ingestion & indexing:** Parses, chunks, embeds, and indexes your help articles for robust retrieval.
- **Modern RAG pipeline:** Uses OpenAI-compatible embeddings & LLMs (e.g., Metis, Aval AI) with Chroma for fast vector search.
- **CLI agent:** Interactively answers questions, always citing sources, and gracefully refusing out-of-domain queries.
- **Dockerized & tested:** Reproducible with Docker, with unit/integration tests provided.

---

## Project Structure

```
task1/
  app.py                # Main CLI interface
  data_ingestion.py     # Data ingestion, chunking, and indexing
  qa_agent.py           # RetrievalQA pipeline logic
  config.py             # Environment/config loading
  requirements.txt      # Python dependencies
  articles.json         # (Your exported help center)
  tests/
    test_pipeline.py    # Automated tests
  README.md
  Dockerfile
  .env                  # (Your API keys/configs, not in repo)
```

---

## Setup Instructions

### 1. Prerequisites

- Python 3.10+ recommended
- [Docker](https://www.docker.com/) (optional, for containerized usage)
- API key and base URL for an OpenAI-compatible provider (e.g., Metis, Aval AI)

---

### 2. Environment Variables

Create a `.env` file in the project root (no quotes around values):

```
OPENAI_API_KEY=your-api-key-here
OPENAI_BASE_URL=https://api.metisai.ir/openai/v1
EMBEDDING_MODEL=text-embedding-3-small
```

---

### 3. Install Dependencies

**Locally:**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### 4. Data Ingestion & Indexing Pipeline

Before using the agent, ingest and index your help center data:

```bash
python data_ingestion.py articles.json
```

**What this does (sub-steps):**
1. **Parsing:** Loads and validates `articles.json` (must be a list of dicts with `title`, `url`, `content`).
2. **Chunking:** Splits each article into smaller, context-preserving chunks (~1000 chars, adjustable in `config.py`). **Titles are prepended to each chunk** for better retrieval.
3. **Embedding:** Converts each chunk into a dense vector using the specified OpenAI-compatible embedding model.
4. **Indexing:** Stores all embeddings and metadata in a persistent Chroma vector database (`chroma_db/`).

**Note:**  
- **If you change the embedding model, delete `chroma_db/` and re-run ingestion.**

---

### 5. Running the Q&A Agent (CLI)

**Locally:**
```bash
python app.py
```
You’ll get a prompt:
```
Welcome to the Intercom Help Center AI Agent!
Enter your question (or 'exit' to quit):
```

---

## Docker Usage

### Option 1: Everything Inside Docker (Quickstart)

This is simple but the Chroma DB won’t persist outside the container.

```bash
docker build -t partnerz-rag-agent .
docker run -it --env-file .env partnerz-rag-agent python data_ingestion.py articles.json
docker run -it --env-file .env partnerz-rag-agent
```
- **Drawback:** Each time you start a new container, the DB is reset unless you use volumes.

---

### Option 2: Sharing Chroma DB and Data with Host (Recommended for Dev)

Mount your local `chroma_db` and `articles.json` into the container:

```bash
docker run -it --env-file .env \
  -v $(pwd)/chroma_db:/app/chroma_db \
  -v $(pwd)/articles.json:/app/articles.json \
  partnerz-rag-agent python data_ingestion.py articles.json

docker run -it --env-file .env \
  -v $(pwd)/chroma_db:/app/chroma_db \
  -v $(pwd)/articles.json:/app/articles.json \
  partnerz-rag-agent
```

- This ensures your ingested data persists between runs and is accessible both inside and outside Docker.

---

### Notes on Docker and Chroma DB
- **If you build or ingest data on your host but run the agent in Docker, you must use volume mounts** or the agent will not see the same Chroma DB.
- **If you change embedding models,** delete the `chroma_db/` directory before rebuilding.

---

## Testing

Run tests with:
```bash
pytest tests/test_pipeline.py
```
- Ensure you run from the project root (where `qa_agent.py` is).

---

## Customization

- **Chunk size/overlap:** Adjustable in `config.py` (default: 1000 chars, 200 overlap).
- **Prompt:** Customizable in `qa_agent.py` for answer style/refusal handling.
- **Embedding/LLM models:** Configurable via `.env`/`config.py` for different OpenAI-compatible providers.

---

## Troubleshooting

- **API/auth errors:** Double-check `.env` values, remove quotes, and ensure Docker is using `--env-file .env`.
- **“No module named ...” during testing:** Run tests from the project root, or add the root to `sys.path` in test files.
- **Chroma DB not found in Docker:** Use volume mounts as shown above.
- **Out-of-domain queries return random sources:** The agent suppresses sources for “I don’t know” refusals (see `qa_agent.py`).

---

## License

MIT

---

**For any issues or questions, please contact the maintainer or open an issue!**