from langchain_community.tools import DuckDuckGoSearchResults


web_search = DuckDuckGoSearchResults(output_format = "list")

def search_web(query : str):
    return web_search.invoke(query)
    

