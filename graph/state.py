from typing import TypedDict, List
from schemas import ResearchPlanner, SearchResult, ValidatedSearchResult, TopicSummary, ReviewResult, ResearchReport
class ResearchState(TypedDict):
    query: str
    plan: ResearchPlanner
    search_results: List[SearchResult]
    validated_results: List[ValidatedSearchResult]
    topic_summary: List[TopicSummary]
    report: ResearchReport
    review: ReviewResult
    rewrite_attempts: int