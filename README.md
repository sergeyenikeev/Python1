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

## Setup

1. Install UV: `pip install uv`
2. Install dependencies: `uv pip install -r pyproject.toml`
3. Run with Docker Compose: `docker-compose up --build`

## API

- POST /process: Process text with LangGraph, save to DB, send to Kafka

## Kubernetes

Apply manifests: `kubectl apply -f k8s/`