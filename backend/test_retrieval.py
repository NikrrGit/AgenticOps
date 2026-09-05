from backend.rag.vector_store import get_vector_store

vector_store = get_vector_store()

results = vector_store.similarity_search(
    "Whats is Memory of Lamguage Models?",
    k=4,
)

for i, document in enumerate(results, start=1):
    print(f"\n--- Result {i} ---")

    print("Source:", document.metadata.get("source"))

    print("Content:")
    print(document.page_content)
