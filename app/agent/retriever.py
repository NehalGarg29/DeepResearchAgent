from app.memory.chroma_store import memory_manager
from typing import List, Dict, Any

class Retriever:
    def __init__(self, limit: int = 5):
        self.limit = limit

    def retrieve(self, query: str) -> List[Dict[str, Any]]:
        """Retrieve relevant context for a query."""
        results = memory_manager.search(query, n_results=self.limit)
        return results

retriever = Retriever()
