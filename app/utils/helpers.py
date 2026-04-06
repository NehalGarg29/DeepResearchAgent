import os
from app.memory.chroma_store import memory_manager
from loguru import logger

def index_seed_docs():
    """Index documents from the seed_docs directory."""
    seed_dir = "app/data/seed_docs"
    if not os.path.exists(seed_dir):
        logger.warning(f"Seed directory {seed_dir} not found.")
        return

    for filename in os.listdir(seed_dir):
        if filename.endswith(".md") or filename.endswith(".txt"):
            file_path = os.path.join(seed_dir, filename)
            with open(file_path, 'r') as f:
                content = f.read()
                doc_id = memory_manager.add_document(
                    content=content,
                    metadata={"source": filename, "type": "seed_doc"}
                )
                logger.info(f"Indexed {filename} with ID: {doc_id}")

if __name__ == "__main__":
    index_seed_docs()
