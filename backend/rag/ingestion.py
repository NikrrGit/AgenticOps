from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


DOCUMENTS_PATH = Path("knowledge/documents")

def load_documents() -> list[Document]:

    documents = []

    for file_path in DOCUMENTS_PATH.glob('*.md'):
        text = file_path.read_text(encoding='utf-8')

    documents.append(
        Document(
            page_content=text,
            metadta={
                'source': str(file_path),
            },
        )
    )

    return documents

# Split the document
def split_documents(
        documents : list[Document],
) -> list[Document] :
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap= 50, 
    )

return splitter.spli_documenst(document)
