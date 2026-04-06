from app.config import settings
from app.utils.token_counter import count_tokens
from loguru import logger

class ConstraintManager:
    def __init__(self, max_tokens: int = settings.MAX_TOKENS_PER_RESEARCH, max_retrievals: int = settings.MAX_QUERY_RETRIEVALS):
        self.max_tokens = max_tokens
        self.max_retrievals = max_retrievals
        self.used_tokens = 0
        self.retrieval_count = 0

    def add_token_count(self, text: str):
        tokens = count_tokens(text)
        self.used_tokens += tokens
        logger.info(f"Used {tokens} tokens. Total: {self.used_tokens}/{self.max_tokens}")
        return self.is_budget_exceeded()

    def add_retrieval(self):
        self.retrieval_count += 1
        logger.info(f"Retrieval count: {self.retrieval_count}/{self.max_retrievals}")
        return self.is_retrieval_exceeded()

    def is_budget_exceeded(self) -> bool:
        return self.used_tokens >= self.max_tokens

    def is_retrieval_exceeded(self) -> bool:
        return self.retrieval_count >= self.max_retrievals

    def get_status(self):
        return {
            "used_tokens": self.used_tokens,
            "max_tokens": self.max_tokens,
            "retrieval_count": self.retrieval_count,
            "max_retrievals": self.max_retrievals,
            "budget_exceeded": self.is_budget_exceeded(),
            "retrieval_exceeded": self.is_retrieval_exceeded()
        }
