import tiktoken
from app.config import settings

def count_tokens(text: str, model_name: str = settings.MODEL_NAME) -> int:
    """Count the number of tokens in a string."""
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    
    return len(encoding.encode(text))
