"""
Unit tests for LangGraph workflow.
"""

import pytest
from app.langgraph_workflow import process_text, run_workflow, State

def test_process_text():
    """Test the process_text function."""
    state = {"text": "hello world"}
    result = process_text(state)
    assert result["text"] == "HELLO WORLD"

def test_run_workflow():
    """Test the run_workflow function."""
    input_text = "test input"
    result = run_workflow(input_text)
    assert result == "TEST INPUT"