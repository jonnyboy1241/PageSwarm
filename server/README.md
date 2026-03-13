# PageSwarm API Service

FastAPI module responsible for document ingestion and API-facing workflows in the PageSwarm system.

## What This Module Does

The API service currently provides:

- Service health and liveness endpoint
- PDF upload validation
- Page count extraction using PyPDF
- Job metadata generation (`job_id`, file metadata, queued status)
- Structured logging for request and error flows

## Directory Snapshot

```text
server/
	Dockerfile
	pyproject.toml
	uv.lock
	main.py
	api/
		endpoints/
			health.py
		v1/
			api.py
			endpoints/
				documents.py
	core/
		logging.py
		middleware.py
	schemas/
		documents.py
		health.py
```

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/health` | Liveness + timestamp response |
| POST | `/api/v1/documents/upload` | Accept PDF, validate content, return queued job metadata |

Upload request example:

```bash
curl -X POST \
	-F "file=@/path/to/document.pdf" \
	http://localhost:8000/api/v1/documents/upload
```

Successful response shape:

```json
{
	"job_id": "uuid",
	"filename": "document.pdf",
	"size_bytes": 12345,
	"total_pages": 12,
	"status": "queued",
	"accepted_at": "2026-03-12T00:00:00Z"
}
```

## Run This Component Locally (Without Docker)

This repository uses `uv` for environment and dependency management.

1. Install dependencies:

```bash
cd server
uv sync --frozen --no-dev
```

2. Run the API:

```bash
uv run --frozen --no-sync uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

3. Verify health endpoint:

```bash
curl http://localhost:8000/api/health
```

## Run This Component In Docker (Standalone)

From the repository root:

1. Build API image:

```bash
docker build -t pageswarm-api:local ./server
```

2. Run API container:

```bash
docker run --rm -p 8000:8000 --name pageswarm-api pageswarm-api:local
```

Note: current endpoints work without external services. As S3/SQS integration is added, run this service with LocalStack and environment configuration.

## Run Via Compose (Recommended For Full Stack)

From repository root:

```bash
docker compose up --build api localstack
```

## Configuration Notes

- Python target: 3.12+
- ASGI server: Uvicorn
- Multipart upload support: `python-multipart`
- PDF parsing: `pypdf`

## Development Notes

- Keep route handlers thin and push orchestration/business logic to dedicated services as the module grows.
- Preserve idempotent behavior for document/page processing contracts.
- Add/maintain tests as endpoint behavior evolves.
