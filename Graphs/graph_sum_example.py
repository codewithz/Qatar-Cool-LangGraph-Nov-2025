from typing import List
from typing_extensions import TypedDict
from langgraph.graph import StateGraph

# 1. State schema for multiple inputs
class AgentState(TypedDict):
    values: List[int]
    name: str
    result: str

# 2. Processing node
def process_values(state: AgentState) -> AgentState:
    """
    This node:
    - Sums up the integers in `values`
    - Builds a message including the user's name and the sum
    - Stores it in `result`
    """
    print("State BEFORE:", state)

    total = sum(state["values"])
    name = state["name"]

    state["result"] = f"Hi there {name}, your sum is equal to {total}"

    print("State AFTER:", state)

    return state

def main():
    # 3. Build the graph
    graph = StateGraph(AgentState)
    graph.add_node("processor", process_values)
    graph.set_entry_point("processor")
    graph.set_finish_point("processor")

    app = graph.compile()

    # 4. Invoke the graph
    initial_state = {
        "values": [1, 2, 3, 4],
        "name": "Steve",
        "result": ""
    }

    answer = app.invoke(initial_state)

    print("Full state:", answer)
    print("Just result:", answer["result"])

if __name__ == "__main__":
    main()

