from langchain_community.tools import( 
    ArxivQueryRun,
    WikipediaQueryRun,
)
from langchain_community.utilities import (
    ArxivAPIWrapper,
    WikipediaAPIWrapper,
)
from langchain_community.tools.tavily_search import TavilySearchResults

# wikipedia
wikipedia = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(),
    top_k_results=2,
    doc_content_chars_max=4000,
)

#ArcXiv 

arxiv = ArxivQueryRun(
    arxiv_wrapper = ArxivAPIWrapper(
    top_k_results=2,
    doc_content_chars_max=4000,
    )
)

# Tavily

tavily = TavilySearchResults(
    max_results=3,
)

# All tolls
tools = [
  wikipedia,
  arxiv,
  tavily,
]
