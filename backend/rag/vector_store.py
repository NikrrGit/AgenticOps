from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = 'knowledge_base'

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

client = QdrantClient(
    url=QDRANT_URL
)

def create_vector_store(docuements):
    vector_store=QdrantVectorStorer.from_docuement(
        docuement=docuements,
        embedding=embeddings,
        url=QDRANT_URL,
        collection_name=COLLECTION_NAME,
    )

return vector_store