from typing import TypedDict
from langgraph.graph import StateGraph

# 1. State schema for sequence processing
class AgentState(TypedDict):
    name:str
    age:int
    final:str


# 2. First processing node
def first_node(state: AgentState) -> AgentState:
    """
    This node:
     Greets the use by name 
    """

    print("State BEFORE first_node:", state)

    name = state["name"]
    state["final"] = f"Hello {name}!"

    print("State AFTER first_node:", state)

    return state

# 3. Second processing node
def second_node(state: AgentState) -> AgentState:
    """
    This node:
     Adds age information to the greeting
    """

    print("State BEFORE second_node:", state)

    age = state["age"]
    state["final"] += f" You are {age} years old."

    print("State AFTER second_node:", state)

    return state

def build_graph():
    graph= StateGraph(AgentState)

    graph.add_node("first", first_node)
    graph.add_node("second", second_node)

    graph.set_entry_point("first")
    graph.add_edge("first", "second")
    graph.set_finish_point("second")

    return graph.compile()

def main():
    app = build_graph()

    # 4. Invoke the graph
    initial_state = {
        "name": "Alice",
        "age": 30,
        "final": ""
    }

    answer = app.invoke(initial_state)

    print("Full state:", answer)
    print("Just final message:", answer["final"])

if __name__ == "__main__":
    main()