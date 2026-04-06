import chromadb
from chromadb.utils import embedding_functions
from app.config import settings
from typing import List, Dict, Any
import uuid
from loguru import logger

class MemoryManager:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.CHROMA_PATH)
        
        # Use Local Embeddings (Free & No API Key required)
        logger.info("Using Local Embeddings (Default ONNX Runtime).")
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()

        self.collection = self.client.get_or_create_collection(
            name="research_memory",
            embedding_function=self.embedding_fn
        )

    def add_document(self, content: str, metadata: Dict[str, Any] = None):
        """Add a single piece of research content to memory."""
        doc_id = str(uuid.uuid4())
        self.collection.add(
            documents=[content],
            metadatas=[metadata or {}],
            ids=[doc_id]
        )
        return doc_id

    def search(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant content in memory."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        formatted_results = []
        if results['documents'] and len(results['documents']) > 0:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                    "distance": results['distances'][0][i] if 'distances' in results and results['distances'] else None
                })
        return formatted_results

memory_manager = MemoryManager()
