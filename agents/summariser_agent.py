from collections import defaultdict
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed

from llm_initializer import llm_mini
from prompts.summarizer_prompt import SUMMARISER_PROMPT
from schemas import TopicSummary, ValidatedSearchResult

structured_output = llm_mini.with_structured_output(
    TopicSummary
)

def summarise_topic(topic, results):

    contents = []
    sources = []

    for result in results:
        contents.append(result.content)
        sources.append(result.source)

    combined_content = "\n\n".join(contents)

    generated_summary = structured_output.invoke(
        f"""
        Summariser Prompt:
        {SUMMARISER_PROMPT}

        Topic:
        {topic}

        Content:
        {combined_content}
        """
    )

    print(f"Summarised: {topic}")

    return TopicSummary(
        topic=generated_summary.topic,
        summary=generated_summary.summary,
        sources=list(set(sources))
    )


def summariser_agent(
    search_results: List[ValidatedSearchResult]
):

    grouped_result = defaultdict(list)

    for result in search_results:
        grouped_result[result.topic].append(result)

    summaries = []

    max_workers = min(
        len(grouped_result),
        8
    )

    with ThreadPoolExecutor(
        max_workers=max_workers
    ) as executor:

        futures = [
            executor.submit(
                summarise_topic,
                topic,
                results
            )
            for topic, results
            in grouped_result.items()
        ]

        for future in as_completed(futures):
            summaries.append(
                future.result()
            )

    return summaries