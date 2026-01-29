import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Use SQLite for local development (no PostgreSQL required)
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./hr_analysis.db"
    )
    BACKEND_HOST: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8000"))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    UPLOAD_DIR: str = "uploads"
    REPORT_DIR: str = "reports"
    
    class Config:
        env_file = ".env"


settings = Settings()
