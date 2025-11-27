import random
from typing import List,TypedDict
from langgraph.graph import StateGraph,START,END


# 1. State schema for looping processing
class AgentState(TypedDict):
    name:str
    number:List[int]
    counter:int

# 2. Processing node

def greeting_node(state: AgentState) -> AgentState:
    """
    This node:
    Initialize the name and the counter 
    """

    print("State BEFORE greeting_node:", state)

    state["name"]=f"Hi there {state['name']}"
    state["counter"] = 0
    print(f"{state['name']}, let's start adding random numbers to your list!")
    print("State AFTER greeting_node:", state)

    return state

def random_node(state:AgentState) -> AgentState:
    """
    This node:
    Generate a rando number and increment the counter
    """

    print("State BEFORE random_node:", state)

    new_value = random.randint(1,10)
    state["number"].append(new_value)
    state["counter"] += 1
    print(f"Added {new_value} to the list.")
    print(f"Counter is now {state['counter']}.")
    print("State AFTER random_node:", state)

    return state

def should_continue(state:AgentState) -> str:
    """
    Decide whether to loop again or exit.

    Must return one of the keys in the mapping passed to add_conditional_edges:
    - "loop"  -> go back to 'random'
    - "exit"  -> go to END
    """

    if state["counter"] < 5:
        print("Continuing the loop.")
        print("Counter VALUE:", state["counter"])
        return "loop"
    else:
        print("Exiting the loop.Counter Value is ",state["counter"])
        return "exit"
    
# 3. Build the graph
def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("greeting", greeting_node)
    graph.add_node("random", random_node)

    # Greeting -> Random [First Random Call]
    graph.add_edge("greeting", "random")

    #From Random , decide whether to loop or exit

    graph.add_conditional_edges(
        "random",  # source node
          should_continue, #Router/ conditional function 
          {
              "loop": "random",  # Loop back to 'random'
                "exit": END       # Exit to END
          })
    
    graph.set_entry_point("greeting")

    return graph.compile()

def main():
    app = build_graph()

    # 4. Invoke the graph
    initial_state = {
        "name": "Bob",
        "number": [],
        "counter": -100
    }

    final_state = app.invoke(initial_state)

    print("Final state:", final_state)

if __name__ == "__main__":
    main()
