from langchain_community.tools import( 
    ArxivQueryRun,
    WikipediaQueryRun,
)
from langchain_community.utilities import (
    ArxivAPIWrapper,
    WikipediaAPIWrapper,
)
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool

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

@tool
def retrieve_knowledge(query : str) -> str:
    """
    Search the knowledge base for the information relavent to users question
    Use this tool when the answer may be found in user's document
    """

    # Loading the embedding model is only needed for knowledge-base searches.
    # Keeping this import local lets the web-search tools work without the
    # optional RAG dependencies installed.
    from backend.rag.vector_store import get_vector_store

    vector_store = get_vector_store()

    documents = vector_store.similarity_search(
        query,
        k=4,
    )

    if not documents:
        return "No relevant information was found in knowledge base"

    context = []

    for document in documents:

        context.append(
            f"Source:{document.metadata.get('source', 'unknown')}\n"
            f"Content:{document.page_content}"
        )

    return "\n\n---\n\n".join(context)


# All tools
tools = [
    wikipedia,
    arxiv,
    tavily,
    retrieve_knowledge,
]
