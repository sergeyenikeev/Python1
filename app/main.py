"""
Pet Project API - A demonstration of FastAPI with LangGraph, PostgreSQL, and Kafka integration.

This module contains the main FastAPI application with endpoints for processing text
using LangGraph workflows, saving results to PostgreSQL, and sending messages to Kafka.
"""

import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.langgraph_workflow import run_workflow
from app.database import save_to_db
from app.kafka_producer import send_to_kafka

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Pet Project API",
    version="1.0.0",
    description="A pet project demonstrating FastAPI, LangGraph, PostgreSQL, and Kafka."
)

class InputData(BaseModel):
    """Input data model for text processing requests."""
    text: str

@app.post("/process")
async def process_text(data: InputData):
    """
    Process input text using LangGraph workflow, save to database, and send to Kafka.

    Args:
        data (InputData): The input data containing the text to process.

    Returns:
        dict: A dictionary with the processed result.

    Raises:
        HTTPException: If an error occurs during processing.
    """
    logger.info(f"Received request to process text: {data.text[:50]}...")
    try:
        # Run LangGraph workflow
        logger.info("Running LangGraph workflow...")
        result = run_workflow(data.text)
        logger.info(f"Workflow result: {result[:50]}...")

        # Save to PostgreSQL
        logger.info("Saving to PostgreSQL...")
        save_to_db(data.text, result)

        # Send to Kafka
        logger.info("Sending to Kafka...")
        send_to_kafka("processed_topic", {"input": data.text, "output": result})

        logger.info("Processing completed successfully.")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error during processing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """
    Root endpoint to check if the API is running.

    Returns:
        dict: A welcome message.
    """
    logger.info("Root endpoint accessed.")
    return {"message": "Pet Project API is running"}