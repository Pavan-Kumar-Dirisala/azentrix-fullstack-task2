from prompts.reviewer_prompt import REVIEWER_PROMPT
from llm_initializer import llm
from schemas import ResearchReport , ReviewResult

structured_output = llm.with_structured_output(ReviewResult)

def reviewer_agent(report : ResearchReport):
    review = structured_output.invoke(
        f"""
        {REVIEWER_PROMPT}

        Title:
        {report.title}

        Executive Summary:
        {report.executive_summary}

        Report:
        {report.report}

        References:
        {report.references}
        """
    )

    return review