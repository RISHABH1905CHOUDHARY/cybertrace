"""Application configuration settings using Pydantic Settings."""

from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    APP_NAME: str = "CrimeTrace AI Backend"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"

    # Security & JWT
    SECRET_KEY: str = "crimetrace-super-secret-jwt-signing-key-change-in-production-min32chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./crimetrace.db"
    SYNC_DATABASE_URL: str = "sqlite:///./crimetrace.db"
    USE_POSTGIS: bool = False

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "*",
    ]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        return ["*"]

    # ML & Forecasting Configuration
    ML_MODEL_ENABLED: bool = False
    ML_SERVICE_STUB_MODE: bool = True
    ML_MODEL_PATH: str = "app/ml/weights/withdrawal_predictor.onnx"

    # Risk Engine Defaults
    RISK_SEARCH_RADIUS_KM: float = 5.0
    HIGH_RISK_THRESHOLD: float = 65.0
    CRITICAL_RISK_THRESHOLD: float = 85.0


settings = Settings()
