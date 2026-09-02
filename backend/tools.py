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
    api_wrappper=WikipediaAPIWrapper,
    top_k_results=2,
    doc_content_chars_max=4000,
)

#ArcXiv 

arxiv = ArxivQueryRun(
    arxiv_wrapper = ArxivAPIWrapper(
    top_k_results=2,
    doc_content_chars_mnax=4000,
    )
)