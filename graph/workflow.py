from langgraph.graph import StateGraph , START , END
from graph.state import ResearchState
from graph.nodes import planner_node , searching_node , validation_node , summariser_node , writer_node , reviewer_node

graph_builder = StateGraph(ResearchState)


graph_builder.add_node("planner",planner_node)
graph_builder.add_node("search", searching_node)
graph_builder.add_node("validator", validation_node)
graph_builder.add_node("summariser", summariser_node)
graph_builder.add_node("writer", writer_node)
graph_builder.add_node("reviewer", reviewer_node)


graph_builder.add_edge(START, "planner")
graph_builder.add_edge("planner", "search")
graph_builder.add_edge("search", "validator")
graph_builder.add_edge("validator", "summariser")
graph_builder.add_edge("summariser", "writer")
graph_builder.add_edge("writer", "reviewer")
def review_router(state: ResearchState):
    if state["review"].approved:
        # print("APPROVED")
        return "approved"

    if state["rewrite_attempts"] >= 3:
        # print("MAX ATTEMPTS REACHED")
        return "approved"

    # print("REWRITING")
    return "rewrite"

graph_builder.add_conditional_edges(
    "reviewer",
    review_router,
    {
        "approved" : END,
        "rewrite" : "writer"
    }
)
graph = graph_builder.compile()