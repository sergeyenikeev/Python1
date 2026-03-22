"""FastAPI entrypoint for the text processing workflow."""

import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.database import save_to_db
from app.kafka_producer import send_to_kafka
from app.langgraph_workflow import run_workflow
from app.redis_cache import get_cached_result, inspect_cache, set_cached_result

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PROCESSED_TOPIC = "processed_topic"

app = FastAPI(
    title="Pet Project API",
    version="1.0.0",
    description="Demo project with FastAPI, LangGraph, PostgreSQL, Kafka, and Redis.",
)


class InputData(BaseModel):
    """Request model for text processing."""

    text: str


@app.post("/process")
async def process_text(data: InputData) -> dict[str, str]:
    """Run the workflow, persist the result, and publish an event."""
    logger.info("Received text processing request: %s", data.text[:50])
    try:
        result = get_cached_result(data.text)
        if result is None:
            result = run_workflow(data.text)
            set_cached_result(data.text, result)

        save_to_db(data.text, result)
        send_to_kafka(PROCESSED_TOPIC, {"input": data.text, "output": result})
    except Exception as exc:
        logger.exception("Text processing request failed.")
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    logger.info("Text processing request completed successfully.")
    return {"result": result}


@app.get("/cache")
async def cache_inspect(text: str) -> dict[str, object]:
    """Return cached result metadata for the provided text."""
    info = inspect_cache(text)
    if "error" in info:
        raise HTTPException(status_code=503, detail=info["error"])
    return info


@app.get("/")
async def root() -> dict[str, str]:
    """Lightweight health endpoint."""
    logger.info("Health endpoint requested.")
    return {"message": "Pet Project API is running"}
