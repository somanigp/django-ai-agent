from langchain_tavily import TavilySearch
from django.conf import settings

def get_web_search_tool():
    """Return a web search tool which helps give answers for information as needed."""
    return TavilySearch(
        api_key=settings.TAVILY_API_KEY,
        max_results=5  
    )
