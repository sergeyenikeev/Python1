"""
LangGraph Workflow Module

This module defines a simple LangGraph workflow for processing text.
The workflow converts input text to uppercase.
"""

import logging
from langgraph.graph import StateGraph, END
from typing import TypedDict

logger = logging.getLogger(__name__)

class State(TypedDict):
    """State dictionary for the LangGraph workflow."""
    text: str

def process_text(state: State) -> State:
    """
    Process the text in the state by converting it to uppercase.

    Args:
        state (State): The current state containing the text.

    Returns:
        State: The updated state with processed text.
    """
    logger.info("Processing text to uppercase.")
    state["text"] = state["text"].upper()
    return state

def run_workflow(input_text: str) -> str:
    """
    Run the LangGraph workflow on the input text.

    Args:
        input_text (str): The text to process.

    Returns:
        str: The processed text.
    """
    logger.info(f"Starting workflow for input: {input_text[:50]}...")
    graph = StateGraph(State)
    graph.add_node("process", process_text)
    graph.set_entry_point("process")
    graph.add_edge("process", END)

    app = graph.compile()
    result = app.invoke({"text": input_text})
    logger.info(f"Workflow completed with result: {result['text'][:50]}...")
    return result["text"]