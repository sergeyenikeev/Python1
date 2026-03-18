"""Integration tests for the FastAPI application."""

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@patch("app.main.get_cached_result")
@patch("app.main.run_workflow")
@patch("app.main.set_cached_result")
@patch("app.main.save_to_db")
@patch("app.main.send_to_kafka")
def test_process_text_endpoint(mock_send, mock_save, mock_set_cache, mock_run, mock_get_cache):
    """Cache miss should run the workflow and populate Redis."""
    mock_get_cache.return_value = None
    mock_run.return_value = "PROCESSED TEXT"

    response = client.post("/process", json={"text": "hello"})

    assert response.status_code == 200
    assert response.json() == {"result": "PROCESSED TEXT"}
    mock_get_cache.assert_called_once_with("hello")
    mock_run.assert_called_once_with("hello")
    mock_set_cache.assert_called_once_with("hello", "PROCESSED TEXT")
    mock_save.assert_called_once_with("hello", "PROCESSED TEXT")
    mock_send.assert_called_once_with("processed_topic", {"input": "hello", "output": "PROCESSED TEXT"})


@patch("app.main.get_cached_result")
@patch("app.main.run_workflow")
@patch("app.main.set_cached_result")
@patch("app.main.save_to_db")
@patch("app.main.send_to_kafka")
def test_process_text_endpoint_uses_redis_cache(mock_send, mock_save, mock_set_cache, mock_run, mock_get_cache):
    """Cache hit should skip the workflow and reuse the cached result."""
    mock_get_cache.return_value = "CACHED TEXT"

    response = client.post("/process", json={"text": "hello"})

    assert response.status_code == 200
    assert response.json() == {"result": "CACHED TEXT"}
    mock_get_cache.assert_called_once_with("hello")
    mock_run.assert_not_called()
    mock_set_cache.assert_not_called()
    mock_save.assert_called_once_with("hello", "CACHED TEXT")
    mock_send.assert_called_once_with("processed_topic", {"input": "hello", "output": "CACHED TEXT"})


def test_root_endpoint():
    """Root endpoint should return a health response."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Pet Project API is running"}
