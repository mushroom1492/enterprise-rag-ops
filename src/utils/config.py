from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    # LLM Settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    MODEL_NAME: str = "gpt-4o-mini"
    
    # RAG Settings
    DATA_DIR: str = "data"
    CHROMA_PERSIST_DIR: str = "chroma_db"
    
    # Observability (LangSmith)
    LANGCHAIN_TRACING_V2: str = "true"
    LANGCHAIN_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY", "")
    LANGCHAIN_PROJECT: str = "enterprise-rag-ops"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
