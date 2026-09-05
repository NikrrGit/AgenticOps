import os

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_PATH = "qdrant_data"
COLLECTION_NAME = 'knowledge_base'

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
connection_options = {"url": QDRANT_URL} if QDRANT_URL else {"path": QDRANT_PATH}

def create_vector_store(documents, ids=None):
    vector_store = QdrantVectorStore.from_documents(
        documents=documents,
        ids=ids,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        **connection_options,
    )
    return vector_store

def get_vector_store():
    return QdrantVectorStore.from_existing_collection(
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        **connection_options,
    )
