"""Application Configuration Module.

Handles application-level configuration and settings.
"""

from pydantic_settings import BaseSettings
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application settings."""

    # Azure Configuration
    azure_subscription_id: str
    azure_resource_group: str
    azure_location: str = "eastus"

    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4"
    openai_api_version: str = "2024-02-01"

    # Semantic Kernel Configuration
    semantic_kernel_model: str = "gpt-4"
    semantic_kernel_temperature: float = 0.7
    semantic_kernel_max_tokens: int = 2048

    # Application Configuration
    app_name: str = "Azure Agentic AI"
    app_version: str = "1.0.0"
    debug: bool = False
    log_level: str = "INFO"

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 4

    # Database Configuration
    database_url: Optional[str] = None
    database_echo: bool = False

    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = False


def get_settings() -> Settings:
    """Get application settings.

    Returns:
        Application settings instance
    """
    return Settings()
