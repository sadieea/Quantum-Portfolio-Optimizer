import os
from typing import Optional
from pydantic import validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost/quantum_portfolio"
    DATABASE_URL_SYNC: str = "postgresql://postgres:password@localhost/quantum_portfolio"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # JWT
    SECRET_KEY: str = "quantum-portfolio-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # File Upload
    UPLOAD_DIR: str = "data/uploads"
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    
    # Quantum Computing
    QISKIT_BACKEND: str = "aer_simulator"
    QAOA_MAX_ITERATIONS: int = 100
    QAOA_DEFAULT_SHOTS: int = 1024
    
    # Optimization
    CLASSICAL_SOLVER: str = "ECOS"
    QUBO_SAMPLER: str = "neal"
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Quantum Portfolio Optimizer"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI + Quantum Hybrid Engine for Smarter Asset Allocation"
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8080"]
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str]) -> str:
        if isinstance(v, str):
            return v
        return "sqlite:///./quantum_portfolio.db"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()