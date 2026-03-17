"""
Юнит-тесты для рабочего процесса LangGraph.
"""

import pytest
from app.langgraph_workflow import process_text, run_workflow, State

def test_process_text():
    """Тестирование функции process_text."""
    state = {"text": "hello world"}
    result = process_text(state)
    assert result["text"] == "HELLO WORLD"

def test_run_workflow():
    """Тестирование функции run_workflow."""
    input_text = "test input"
    result = run_workflow(input_text)
    assert result == "TEST INPUT"