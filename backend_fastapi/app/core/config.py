from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # OCR.Space API
    OCR_SPACE_API_KEY: str
    OCR_CONFIDENCE_THRESHOLD: float = 0.5

    # Search settings
    MAX_SEARCH_RESULTS: int = 3
    SEARCH_TIMEOUT: int = 15

    # Gemini API
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-2.5-flash-lite"

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()