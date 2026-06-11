from graph.state import ResearchState
from agents.planning_agent import planning_agent
from agents.searching_agent import searching_agent
from agents.validation_agent import validation_agent
from agents.summariser_agent import summariser_agent
from agents.writer_agent import writer_agent
from agents.reviewer_agent import reviewer_agent

def planner_node(state : ResearchState):
    plan = planning_agent(state["query"])
    # print("Planning is Done ")
    return {"plan" : plan}

def searching_node(state: ResearchState):
    search_result = searching_agent(state["plan"])
    # print("Searching is done")
    return {"search_results" : search_result}

def validation_node(state : ResearchState):
    validated_result = validation_agent(state["search_results"])
    # print("Validation is done")
    return {"validated_results" : validated_result}

def summariser_node(state: ResearchState):
    summary = summariser_agent(state["validated_results"])
    # print("Summarisation is done")
    return {"topic_summary" : summary}

def writer_node(state: ResearchState):
    feedback = ""
    if "review" in state:
        feedback = state["review"].feedback
    report = writer_agent(
        summaries=state["topic_summary"],
        feedback=feedback
    )
    # print(
    #     f"Writer Attempt: {state.get('rewrite_attempts',0)+1}"
    # )
    # print("Writing is done")
    return {
        "report": report,
        "rewrite_attempts": state.get(
            "rewrite_attempts",
            0
        ) + 1
    }

def reviewer_node(state : ResearchState):
    review = reviewer_agent(state["report"])
    # print("Reviewing is done")
    return {"review" : review}