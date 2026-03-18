# Pet Project

Demo service that processes text with FastAPI and LangGraph, stores results in PostgreSQL, and publishes events to Kafka.

## Stack

- Python
- FastAPI
- LangGraph
- PostgreSQL
- Kafka
- Docker Compose
- Kubernetes
- GitLab CI

## Endpoints

- `GET /` returns a basic health response.
- `POST /process` uppercases the input text, saves it to PostgreSQL, and sends an event to Kafka.

## Local run

```powershell
py -m venv .venv
.\.venv\Scripts\python -m pip install ".[dev]"
.\.venv\Scripts\python -m pytest
.\.venv\Scripts\uvicorn app.main:app --reload
```

## Docker Compose

Make sure Docker Desktop is running, then start the full stack:

```powershell
docker compose up --build
```

The API is exposed on `http://localhost:8001` by default.
If you need a different host port, start it with `APP_HOST_PORT=8010 docker compose up --build`.

## Configuration

- `DATABASE_URL` defaults to `postgresql://user:password@postgres:5432/petdb`
- `KAFKA_BOOTSTRAP_SERVERS` defaults to `kafka:29092`

## Kubernetes

Apply the manifests with:

```powershell
kubectl apply -f k8s/
```
