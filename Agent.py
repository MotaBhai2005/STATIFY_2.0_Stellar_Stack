from langgraph.graph import StateGraph, END
from schema2 import AgentState

from schema2 import DataFetcherOutput, AnalystOutput, RiskAuditorOutput

def data_fetcher_node(state: AgentState):
    # Fetch data and return updates
    output = DataFetcherOutput(stock_data={}, technical_data={}, news="")
    return output.model_dump()

def technical_analyst_node(state: AgentState):
    # Perform technical analysis and return updates
    output = AnalystOutput(recommendation="Hold", rag_context="")
    return output.model_dump()

def risk_auditor_node(state: AgentState):
    # Verify/audit recommendations and return updates
    output = RiskAuditorOutput(
        needs_more_data=False,
        contradiction_reason=None,
        final_report="Audit passed.",
        retry_count=state.get("retry_count", 0)
    )
    return output.model_dump()
    
# Define the conditional routing function
def should_loop(state: AgentState):
    if state.get("needs_more_data") and state.get("retry_count", 0) < 3:
        return "loop"
    return "done"
# Build the Graph
graph = StateGraph(AgentState)

# Add nodes
graph.add_node("data_fetcher", data_fetcher_node)
graph.add_node("technical_analyst", technical_analyst_node)
graph.add_node("risk_auditor", risk_auditor_node)

# Add normal edges
graph.set_entry_point("data_fetcher")
graph.add_edge("data_fetcher", "technical_analyst")
graph.add_edge("technical_analyst", "risk_auditor")

# Add CONDITIONAL edge (the loop)
graph.add_conditional_edges(
    "risk_auditor",          # from this node
    should_loop,             # a function that checks state
    {
        "loop": "data_fetcher",   # if True → go back
        "done": END               # if False → finish
    }
)

app = graph.compile()