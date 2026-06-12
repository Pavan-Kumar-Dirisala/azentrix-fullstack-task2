from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

search = DuckDuckGoSearchAPIWrapper(
    max_results=10
)

def search_web(query: str):
    return search.results(
        query,
        max_results=10
    )