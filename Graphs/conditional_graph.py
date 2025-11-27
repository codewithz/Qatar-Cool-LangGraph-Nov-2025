from typing import TypedDict
from langgraph.graph import StateGraph,START,END

# 1. State schema for conditional processing
class AgentState(TypedDict):
    number1:int
    operation:str
    number2:int
    finalNumber:int

# 2. Processing nodes
def adder(state:AgentState) -> AgentState:
    """
    This node:
     Adds number1 and number2 if operation is 'add'
    """

    print("State BEFORE adder:", state)

    if state["operation"] == "add":
        state["finalNumber"] = state["number1"] + state["number2"]

    print("State AFTER adder:", state)

    return state

def subtractor(state:AgentState) -> AgentState:
    """
    This node:
     Subtracts number2 from number1 if operation is 'subtract'
    """

    print("State BEFORE subtractor:", state)

    if state["operation"] == "subtract":
        state["finalNumber"] = state["number1"] - state["number2"]

    print("State AFTER subtractor:", state)

    return state
# 3. Decision node
def decide_next_node(state:AgentState) -> str:
    """
    This decision node:
     Chooses the next node based on the operation
    """

    if state["operation"] == "add":
        return "add"
    elif state["operation"] == "subtract":
        return "subtract"
    else:
        raise ValueError("Unsupported operation")
# 4. Build the graph  
def build_graph():
    """
    Builds and compiles a simple StateGraph that models a conditional routing workflow.
    The graph contains three logical nodes:
    - "router": a passthrough node used to decide which operation to perform next.
    - "adder": a node representing an addition operation/handler.
    - "subtractor": a node representing a subtraction operation/handler.
    Edges and routing:
    - START -> "router"
    - "router" has conditional outgoing edges determined by decide_next_node:
        - when decide_next_node(state) yields "add" -> "adder"
        - when decide_next_node(state) yields "subtract" -> "subtractor"
    - "adder" -> END
    - "subtractor" -> END
    Returns:
        The compiled graph object (the result of graph.compile()), ready for use by
        the surrounding runtime. The decide_next_node callback is expected to accept
        the current state and return a key matching one of the conditional mappings
        (e.g., "add" or "subtract"). Node handlers (adder, subtractor, router) should
        be callable with the AgentState type used by this StateGraph.
    """
    graph= StateGraph(AgentState)

    graph.add_node("adder", adder)
    graph.add_node("subtractor", subtractor)
    graph.add_node("router",lambda state:state)

    graph.add_edge(START, "router")
    graph.add_conditional_edges("router", decide_next_node,{"add":"adder","subtract":"subtractor"});

    graph.add_edge("adder", END)
    graph.add_edge("subtractor", END)

    return graph.compile()

def main():
    app = build_graph()

    # 4. Invoke the graph
    initial_state = {
        "number1": 10,
        "operation": "subtract",
        "number2": 5,
        "finalNumber": 0
    }

    answer = app.invoke(initial_state)

    print("Full state:", answer)
    print("Just finalNumber:", answer["finalNumber"])

if __name__ == "__main__":
    main()
