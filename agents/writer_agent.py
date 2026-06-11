from prompts.writer_prompt import WRITER_PROMPT
from llm_initializer import llm
from schemas import ResearchReport , TopicSummary
from typing import List

structured_output = llm.with_structured_output(ResearchReport)

def writer_agent(summaries : List[TopicSummary], feedback : str =""):
    formatted_summaries = []
    all_sources=[]
    for summary in summaries:
        formatted_summaries.append(
            f"""
            topic : {summary.topic}
            summary :{summary.summary}
            """
    )
        all_sources.extend(summary.sources)
    formatted_content = "\n\n".join(formatted_summaries)
    formatted_sources = "\n".join(list(set(all_sources)))
    generated_report = structured_output.invoke(
        f"""
            Writer Prompt : {WRITER_PROMPT}

            Topic Summaries: {formatted_content}

            Sources: {formatted_sources}


            Reviewer Feedback:

            The previous report was rejected.

            You MUST address all reviewer criticisms before generating the revised report and have to make sure it will get the better feedback next time.

            Required Improvements:
            {feedback}

            Failure to address these issues will result in another rejection.
        """
    )
    report = ResearchReport(
        title=generated_report.title,
        executive_summary=generated_report.executive_summary,
        report=generated_report.report,
        references=list(set(all_sources))
    )
    return report