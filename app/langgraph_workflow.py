"""
Модуль рабочего процесса LangGraph

Этот модуль определяет простой рабочий процесс LangGraph для обработки текста.
Рабочий процесс преобразует входной текст в верхний регистр.
"""

import logging
from langgraph.graph import StateGraph, END
from typing import TypedDict

logger = logging.getLogger(__name__)

class State(TypedDict):
    """Словарь состояния для рабочего процесса LangGraph."""
    text: str

def process_text(state: State) -> State:
    """
    Обработать текст в состоянии, преобразовав его в верхний регистр.

    Args:
        state (State): Текущее состояние, содержащее текст.

    Returns:
        State: Обновленное состояние с обработанным текстом.
    """
    logger.info("Обработка текста в верхний регистр.")
    state["text"] = state["text"].upper()
    return state

def run_workflow(input_text: str) -> str:
    """
    Запустить рабочий процесс LangGraph на входном тексте.

    Args:
        input_text (str): Текст для обработки.

    Returns:
        str: Обработанный текст.
    """
    logger.info(f"Запуск рабочего процесса для входных данных: {input_text[:50]}...")
    graph = StateGraph(State)
    graph.add_node("process", process_text)
    graph.set_entry_point("process")
    graph.add_edge("process", END)

    app = graph.compile()
    result = app.invoke({"text": input_text})
    logger.info(f"Рабочий процесс завершен с результатом: {result['text'][:50]}...")
    return result["text"]