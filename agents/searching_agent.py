from schemas import SearchResult , ResearchPlanner
from tools.search_tool import search_web

def searching_agent(plan : ResearchPlanner):
    search_results=[]

    for topic in plan.subtopics:
        search_output = search_web(topic)
        for result in search_output[:3]:
            search_results.append(
                SearchResult(
                    topic=topic,
                    title=result.get("title", ""),
                    source=result.get("link", ""),
                    content=result.get("snippet", "")
                )
            )
    return search_results
