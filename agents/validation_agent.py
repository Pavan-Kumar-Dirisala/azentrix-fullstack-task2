from schemas import ValidatedSearchResult, SearchResult
from typing import List
import re

def extract_keywords(text:str):
    words=re.findall(r"\b[a-zA-Z]{3,}\b",text.lower())

    stopwords={
        "the","and","for","with","that",
        "this","from","into","about",
        "what","when","where","which",
        "their","have","will","would"
    }

    return {
        word
        for word in words
        if word not in stopwords
    }

def validation_agent(search_results:List[SearchResult]):

    validated_results=[]

    for result in search_results:

        if not result.content:
            continue

        if len(result.content.strip())<80:
            continue

        topic_keywords=extract_keywords(
            result.topic
        )

        content_keywords=extract_keywords(
            result.title+" "+result.content
        )

        overlap=topic_keywords & content_keywords

        if len(overlap)<1:
            continue

        validated_results.append(
            ValidatedSearchResult(
                topic=result.topic,
                title=result.title,
                source=result.source,
                content=result.content,
                is_valid=True,
                validation_reason=f"Keyword overlap: {', '.join(overlap)}"
            )
        )

    print(
        f"Validated: {len(validated_results)} / {len(search_results)}"
    )

    return validated_results