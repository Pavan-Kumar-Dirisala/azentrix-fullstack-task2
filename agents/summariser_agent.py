from collections import defaultdict
from typing import List
from llm_initializer import llm
from prompts.summarizer_prompt import SUMMARISER_PROMPT
from schemas import TopicSummary , ValidatedSearchResult

structured_output = llm.with_structured_output(TopicSummary)

def summariser_agent(search_results : List[ValidatedSearchResult]):
    grouped_result = defaultdict(list)
    for result in search_results :
        grouped_result[result.topic].append(result)

    summaries=[]
    for topic,results in grouped_result.items():
        contents=[]
        sources=[]
        for result in results:
            contents.append(result.content)
            sources.append(result.source)
        combined_content = "\n\n".join(contents)
        generated_summary = structured_output.invoke(
            f"""
            Summariser Prompt : {SUMMARISER_PROMPT}
            Topic : {topic}
            Content : {combined_content}
            """
        )
        summary = TopicSummary(
            topic=generated_summary.topic,
            summary=generated_summary.summary,
            sources=list(set(sources))
        )
        summaries.append(summary)
    return summaries
