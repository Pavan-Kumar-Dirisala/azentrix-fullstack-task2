from pydantic import BaseModel , Field
from typing import List

class ResearchPlanner(BaseModel):
    goal: str = Field(description="Main research objective derived from the user's query")

    subtopics: List[str] = Field(description="List of key subtopics that should be researched")

class SearchResult(BaseModel):
    topic: str = Field(description="Research subtopic for which the search result was retrieved")
    title : str = Field(description="Title of the source or article")
    source : str = Field(description = "Source URL or website name")
    content : str = Field(description = "Relevant extracted content from the source")


class TopicSummary(BaseModel):
    topic: str = Field(description="Research topic being summarized")
    summary: str = Field(description="Concise summary of findings for the topic")


class ReviewResult(BaseModel):
    overall_score: int = Field(description="Overall quality score of the report from 0 to 100")
    approved: bool = Field(description="Whether the report meets the quality threshold")
    feedback: str = Field(description="Reviewer's feedback and improvement suggestions")

class ResearchReport(BaseModel):
    title: str = Field(description="Title of the research report")
    executive_summary: str = Field(description="Brief summary of the entire research report")
    report: str = Field(description="Complete research report containing introduction, findings, analysis, conclusion and references")

class ValidatedSearchResult(BaseModel):
    topic: str = Field(description="Research subtopic associated with the search result")
    title: str = Field(description="Title of the source or article")
    source: str = Field(description="Source URL or website name")
    content: str = Field(description="Validated content from the source")
    is_valid: bool = Field(description="Whether the search result passed validation")
    validation_reason: str = Field(description="Reason for accepting or rejecting the source")