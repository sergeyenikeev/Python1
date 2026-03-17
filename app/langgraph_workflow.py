from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from typing import TypedDict

class State(TypedDict):
    text: str

def process_text(state: State) -> State:
    state["text"] = state["text"].upper()
    return state

def run_workflow(input_text: str) -> str:
    graph = StateGraph(State)
    graph.add_node("process", process_text)
    graph.set_entry_point("process")
    graph.add_edge("process", END)
    
    app = graph.compile()
    result = app.invoke({"text": input_text})
    return result["text"]