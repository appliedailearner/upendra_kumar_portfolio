"""Configuration Agent.

Manages agent configuration and settings.
"""

from typing import Any, Dict, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class AgentConfig:
    """Agent configuration."""

    name: str
    description: str
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 2048
    timeout: int = 30
    retry_count: int = 3


class ConfigurationAgent:
    """Agent for managing configuration."""

    def __init__(self) -> None:
        """Initialize configuration agent."""
        self.configs: Dict[str, AgentConfig] = {}

    def register_config(self, config: AgentConfig) -> None:
        """Register an agent configuration.

        Args:
            config: Agent configuration to register
        """
        self.configs[config.name] = config
        logger.info(f"Registered config for {config.name}")

    def get_config(self, name: str) -> Optional[AgentConfig]:
        """Get configuration by name.

        Args:
            name: Configuration name

        Returns:
            Agent configuration or None
        """
        return self.configs.get(name)

    def update_config(
        self, name: str, **kwargs: Any
    ) -> Optional[AgentConfig]:
        """Update configuration.

        Args:
            name: Configuration name
            **kwargs: Fields to update

        Returns:
            Updated configuration or None
        """
        config = self.configs.get(name)
        if config:
            for key, value in kwargs.items():
                if hasattr(config, key):
                    setattr(config, key, value)
            logger.info(f"Updated config for {name}")
        return config
