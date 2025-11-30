from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
import json

class Settings(BaseSettings):
    env: str = "development"
    server_host: str = "0.0.0.0"
    server_port: int = 5000
    allowed_origins: List[str] = ["*"]
    granian_workers: int = 2
    db_url: str
    echo_sql: bool = False
    log_level: str = "INFO"  # Default to INFO level logging

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="APP_", case_sensitive=False
    )

    @field_validator("allowed_origins", mode="before")
    def _parse_allowed_origins(cls, v):
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            s = v.strip()
            if s == "*":
                return ["*"]
            try:
                parsed = json.loads(s)
                if isinstance(parsed, list):
                    return parsed
            except Exception:
                pass
            return [item.strip() for item in s.split(",") if item.strip()]
        return ["*"]

settings = Settings()
