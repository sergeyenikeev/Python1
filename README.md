# Pet Project

A demonstration project using FastAPI, LangGraph, PostgreSQL, Kafka, Docker, and Kubernetes.

## Tech Stack
- Python
- FastAPI
- LangGraph
- Uvicorn
- Docker
- Kubernetes
- PostgreSQL
- Kafka
- UV (package manager)
- GitLab CI

## Features
- REST API with FastAPI for text processing
- LangGraph workflow for text transformation
- PostgreSQL integration for data persistence
- Kafka messaging for event publishing
- Comprehensive logging throughout the application
- Unit and integration tests with pytest
- Docker containerization
- Kubernetes deployment manifests
- GitLab CI/CD pipeline

## Setup

1. Install UV: `pip install uv`
2. Install dependencies: `uv pip install -r pyproject.toml`
3. Run with Docker Compose: `docker-compose up --build`

## API

- POST /process: Process text with LangGraph, save to DB, send to Kafka
- GET /: Health check endpoint

## Testing

Run unit and integration tests:
```
pytest
```

## Logging

The application uses Python's logging module with INFO level. Logs are output to console.

## Kubernetes

Apply manifests: `kubectl apply -f k8s/`