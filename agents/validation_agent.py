from prompts.validation_prompt import VALIDATION_PROMPT
from llm_initializer import llm
from schemas import ValidatedSearchResult , SearchResult
from typing import List
structured_output = llm.with_structured_output(ValidatedSearchResult)

def validation_agent(search_results : List[SearchResult]):
    validated_results=[]

    for result in search_results:
        validation = structured_output.invoke(
            f"""
            {VALIDATION_PROMPT}

            Topic:
            {result.topic}

            Title:
            {result.title}

            Source:
            {result.source}

            Content:
            {result.content}
            """
        )
        if validation.is_valid:
            validated_results.append(validation)
    print(
    f"Validated: {len(validated_results)} / {len(search_results)}"
)
    return validated_results
            
