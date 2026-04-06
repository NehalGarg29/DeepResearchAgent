from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    OPENAI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    CHROMA_PATH: str = "./data/chroma_db"
    SQLITE_URL: str = "sqlite:///./data/research_agent.db"
    LOG_LEVEL: str = "INFO"
    MODEL_NAME: str = "llama-3.3-70b-versatile"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    MAX_TOKENS_PER_RESEARCH: int = 20000
    MAX_QUERY_RETRIEVALS: int = 5

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
