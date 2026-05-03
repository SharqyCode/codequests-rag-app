# CodeQuests RAG App

CodeQuests RAG App is a full-stack AI knowledge assistant. Users upload documents, the backend parses and chunks them, OpenAI embeddings are stored in ChromaDB, and the chat UI asks questions against the indexed document chunks.

The project contains a React/Vite frontend, a FastAPI backend, and a Docker Compose setup for local development. A few backend helper methods are still placeholders; see [Current Gaps](#current-gaps) before treating this as production-ready.

## Features

- Upload multiple documents from the browser.
- Parse `.txt`, `.md`, `.pdf`, and `.json` files.
- Split documents into overlapping sentence-based chunks.
- Generate embeddings with OpenAI `text-embedding-3-small`.
- Store vectors locally in ChromaDB under `backend/app/data/chroma`.
- Ask questions through a chat interface.
- View uploaded documents and jump from answer sources to the document viewer.
- Persist chat messages in browser `localStorage`.

## Tech Stack

### Frontend

- React 19
- TypeScript
- Vite
- React Router
- Tailwind CSS
- Lucide React icons

### Backend

- FastAPI
- OpenAI Python SDK
- ChromaDB
- pypdf
- python-dotenv
- Pydantic

## Project Structure

```text
.
|-- backend/
|   |-- app/
|   |   |-- api/              # FastAPI routers
|   |   |-- db/               # Chroma client and placeholder DB modules
|   |   |-- services/         # Ingestion, embeddings, retrieval, AI response services
|   |   |-- schemas/          # Pydantic schemas, some still placeholders
|   |   |-- utils/            # File parsing, chunking, logging helpers
|   |   |-- data/chroma/      # Local ChromaDB persistence
|   |   `-- main.py           # FastAPI app entry point
|   |-- Dockerfile            # Backend container image
|   `-- requirements.txt      # Python dependencies
|-- frontend/
|   |-- src/
|   |   |-- components/       # Layout, chat, upload, and document UI components
|   |   |-- context/          # Chat state provider
|   |   |-- lib/api.ts        # Frontend API client
|   |   |-- pages/            # Chat, upload, and docs pages
|   |   `-- main.tsx          # React app entry point
|   |-- Dockerfile            # Frontend container image
|   `-- package.json
|-- samples/                  # Example documents for ingestion
|-- docker-compose.yml        # Local Docker development stack
`-- README.md
```

## How It Works

1. A user uploads files from the frontend `/upload` page.
2. The frontend posts the selected files to `POST /api/ingest/files`.
3. `IngestionService` parses each file using `FileParser`.
4. `TextChunker` splits the parsed text into sentence-based chunks with overlap.
5. `EmbeddingService` sends each chunk to OpenAI for embeddings.
6. `ChromaClient` stores chunks, embeddings, and metadata in the `documents` collection.
7. The chat page sends questions to `POST /api/ai/query`.
8. `RetrievalService` embeds the query and retrieves the closest chunks from ChromaDB.
9. `AIService` is intended to build a context prompt and return an answer with sources.

## Prerequisites

- Python 3.12 recommended
- Node.js 20+ recommended
- npm
- Docker and Docker Compose for the containerized setup
- An OpenAI API key

## Environment Variables

Create a `.env` file in the repository root:

```bash
cp .env.example .env
```

Then add your key:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

The frontend uses `http://localhost:8000` by default. To point it somewhere else, create `frontend/.env.local`:

```bash
VITE_API_URL=http://localhost:8000
```

## Docker Setup

The fastest way to run the full app locally is Docker Compose:

```bash
docker compose up --build
```

This starts:

- Backend API: `http://localhost:8000`
- Backend Swagger docs: `http://localhost:8000/docs`
- Frontend app: `http://localhost:5173`

The Compose stack has two services:

- `backend` builds from `backend/Dockerfile`, runs FastAPI with `uvicorn --reload`, reads `OPENAI_API_KEY` from `.env`, and bind-mounts `backend/app` for live code reload.
- `frontend` builds from `frontend/Dockerfile`, runs the Vite dev server, points `VITE_API_URL` at `http://localhost:8000`, and bind-mounts `frontend` for live reload.

Stop the stack:

```bash
docker compose down
```

Stop the stack and remove the frontend dependency volume:

```bash
docker compose down -v
```

ChromaDB data is stored in the bind-mounted backend app directory:

```text
backend/app/data/chroma
```

## Manual Backend Setup

If you prefer to run the backend outside Docker:

```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the FastAPI server from the `backend` directory:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Useful URLs:

- API root: `http://localhost:8000/`
- Swagger docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Manual Frontend Setup

If you prefer to run the frontend outside Docker:

```bash
cd frontend
npm install
npm run dev
```

Vite will print the local frontend URL, usually:

```text
http://localhost:5173
```

## Local Smoke Test

From the repository root, with the backend running, verify the API root:

```bash
curl http://localhost:8000/
```

Upload one of the sample documents:

```bash
curl -F "files=@samples/golden_retrievers_mini.txt" http://localhost:8000/api/ingest/files
```

List indexed documents:

```bash
curl http://localhost:8000/api/docs/
```

Ask a question:

```bash
curl -X POST http://localhost:8000/api/ai/query \
  -H "Content-Type: application/json" \
  -d '{"query":"What are golden retrievers known for?"}'
```

The query endpoint depends on the retrieval and AI helper methods listed in [Current Gaps](#current-gaps).

## API Endpoints

### Health

- `GET /` returns a simple API status message.

### Ingestion

- `POST /api/ingest/files`
  - Multipart form upload.
  - Form field name: `files`.
  - Accepts multiple files.
  - Supported extensions: `.txt`, `.md`, `.pdf`, `.json`.

- `POST /api/ingest/source`
  - Intended for external structured sources.
  - Body shape:

```json
{
  "source_type": "example",
  "data": [
    {
      "title": "Example",
      "content": "Example source content"
    }
  ]
}
```

### Documents

- `GET /api/docs/` lists indexed Chroma records.
- `GET /api/docs/{doc_id}` returns one stored document/chunk by ID.
- `DELETE /api/docs/truncate` clears the Chroma collection.

### AI

- `POST /api/ai/query`
  - Body shape:

```json
{
  "query": "Ask a question about the indexed documents",
  "document_id": "optional-document-filter"
}
```

  - Expected response shape:

```json
{
  "answer": "Answer text",
  "sources": [
    {
      "source": "filename.txt",
      "document_id": "document-id"
    }
  ],
  "confidence": 0.75
}
```

## Frontend Routes

- `/` - Chat page.
- `/upload` - Document upload page.
- `/docs` - Document list and document viewer.
- `/docs?docId=<id>` - Opens the document viewer with a selected document ID.

## Sample Data

The `samples/` directory contains files that can be uploaded for manual testing:

- `samples/golden_retrievers_mini.txt`
- `samples/golden_retrievers.txt`
- `samples/german_shepards.txt`
- `samples/Huskies.json`
- `samples/Plan/Beagles.md`
- `samples/The Versatile Companion.pdf`

## Data Storage

ChromaDB persists data locally at:

```text
backend/app/data/chroma
```

Deleting this directory or calling `DELETE /api/docs/truncate` removes indexed vector data. The `backend/app/db/postgres.py` and `backend/app/db/models.py` files are placeholders; the current application flow uses ChromaDB directly and does not yet use Postgres.

## Current Gaps

- `AIService` calls helper methods that are not implemented yet: `_build_context`, `_build_prompt`, `_call_llm`, `_extract_sources`, and `_estimate_confidence`.
- `RetrievalService` calls `_deduplicate` and `_format_results`, but those helper methods are not implemented yet.
- `backend/app/api/docs.py` raises `HTTPException` without importing it.
- `POST /api/ingest/source` calls `ingest_external_source`, which is not implemented in `IngestionService`.
- The frontend API types do not fully match current backend response wrappers for uploads and document listing.

## Development Notes

- Run backend commands from `backend/` so imports like `app.main` resolve correctly.
- Keep `OPENAI_API_KEY` out of version control.
- Avoid committing generated folders such as `.venv`, `node_modules`, and Chroma persistence data unless intentionally needed for a demo.
- The Docker setup is development-oriented. For production, build static frontend assets and serve them from a production web server or API gateway.
