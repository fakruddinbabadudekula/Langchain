from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

# -----------------------
# 1. Define the state
# -----------------------
from typing import TypedDict

class GraphState(TypedDict):
    value: int


# -----------------------
# 2. Define nodes
# -----------------------
def double_node(state: GraphState) -> GraphState:
    return {"value": state["value"] * 2}

def add_ten_node(state: GraphState) -> GraphState:
    return {"value": state["value"] + 10}


# -----------------------
# 3. Build graph
# -----------------------
builder = StateGraph(GraphState)

builder.add_node("double", double_node)
builder.add_node("add_ten", add_ten_node)

builder.set_entry_point("double")
builder.add_edge("double", "add_ten")
builder.add_edge("add_ten", END)


# Create SQLite connection
# sqlite3.ProgrammingError: SQLite objects created in a thread can only be used in that same thread. The object was created in thread id 8948 and this is thread id 3776.
# so pass the check_same_thread=False
conn = sqlite3.connect("checkpoints.db",check_same_thread=False)

# Create a checkpointer
checkpointer = SqliteSaver(conn)

# Compile the graph with checkpointing
graph = builder.compile(checkpointer=checkpointer)
# First run
result1 = graph.invoke(
    {"value": 5},
    config={"configurable": {"thread_id": "session-1"}}
)
print("Run 1 result:", result1)


# to delete 
# checkpointer.delete_thread("session-1")


# to access
# checkpointer.list(None) return the generater object on checkpoints