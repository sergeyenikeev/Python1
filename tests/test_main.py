"""
Интеграционные тесты для приложения FastAPI.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

@patch('app.main.run_workflow')
@patch('app.main.save_to_db')
@patch('app.main.send_to_kafka')
def test_process_text_endpoint(mock_send, mock_save, mock_run):
    """Тестирование endpoint /process."""
    mock_run.return_value = "PROCESSED TEXT"

    response = client.post("/process", json={"text": "hello"})

    assert response.status_code == 200
    assert response.json() == {"result": "PROCESSED TEXT"}

    mock_run.assert_called_once_with("hello")
    mock_save.assert_called_once_with("hello", "PROCESSED TEXT")
    mock_send.assert_called_once_with("processed_topic", {"input": "hello", "output": "PROCESSED TEXT"})

def test_root_endpoint():
    """Тестирование корневого endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Pet Project API is running"}