"""Load local knowledge-base files and index them in Qdrant."""

from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.rag.vector_store import COLLECTION_NAME, create_vector_store


DOCUMENTS_PATH = Path("knowledge_base")


def load_documents(documents_path: Path = DOCUMENTS_PATH) -> list[Document]:
    """Load PDF and Markdown files while retaining their source metadata."""
    if not documents_path.exists():
        raise FileNotFoundError(f"Knowledge-base directory does not exist: {documents_path}")

    documents: list[Document] = []
    for file_path in sorted(documents_path.iterdir()):
        if file_path.suffix.lower() == ".pdf":
            documents.extend(PyPDFLoader(str(file_path)).load())
        elif file_path.suffix.lower() == ".md":
            documents.append(
                Document(
                    page_content=file_path.read_text(encoding="utf-8"),
                    metadata={"source": str(file_path)},
                )
            )

    return documents


def split_documents(documents: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(documents)


def ingest_documents(documents_path: Path = DOCUMENTS_PATH) -> int:
    """Upsert all supported files in the knowledge base and return chunk count."""
    chunks = split_documents(load_documents(documents_path))
    if not chunks:
        return 0

    ids = [
        str(
            uuid5(
                NAMESPACE_URL,
                f"{chunk.metadata.get('source', '')}:{chunk.metadata.get('page', '')}:{chunk.page_content}",
            )
        )
        for chunk in chunks
    ]

    create_vector_store(chunks, ids=ids)

    return len(chunks)


if __name__ == "__main__":
    chunk_count = ingest_documents()
    print(f"Indexed {chunk_count} chunks into '{COLLECTION_NAME}'.")
