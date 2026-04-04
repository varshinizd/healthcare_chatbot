from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    GEMINI_API_KEY: str = "your-gemini-api-key-here"
    GEMINI_PRO_MODEL: str = "gemini-1.5-pro"
    GEMINI_FLASH_MODEL: str = "gemini-1.5-flash"
    MAX_HISTORY_TURNS: int = 10
    SESSION_TIMEOUT_MINUTES: int = 30
    RATE_LIMIT: str = "20/minute"
    EMBEDDING_MODEL: str = "models/embedding-001"
    RAG_TOP_K: int = 3
    MIN_CONFIDENCE_SCORE: float = 0.75
    DATABASE_URL: str = "sqlite:///./medibot.db"
    LOG_FILE: str = "logs/chat_log.jsonl"
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    APP_VERSION: str = "1.0.0"
    APP_NAME: str = "MediBot AI"
    DEBUG: bool = False
    CHROMA_PERSIST_DIR: str = "./data/embeddings"
    CHROMA_COLLECTION_NAME: str = "medical_kb"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
