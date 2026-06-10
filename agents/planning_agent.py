from prompts.planner_prompt import PLANNING_PROMPT
from llm_initializer import llm
from schemas import ResearchPlanner

structured_llm = llm.with_structured_output(ResearchPlanner)

def planning_agent (query : str):
    response = structured_llm.invoke(
        f"""
        Planning Prompt : {PLANNING_PROMPT}
        User Query : {query}
        """
    )
    return response
