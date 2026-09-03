"""Azure Agentic AI Application Package.

Main package for the end-to-end reference implementation.
"""

__version__ = "1.0.0"
__author__ = "Azure AI Architect Labs"

from .config import Settings, get_settings
from .agents import SemanticKernelAgent, ConfigurationAgent, AgentOrchestrator

__all__ = [
    "Settings",
    "get_settings",
    "SemanticKernelAgent",
    "ConfigurationAgent",
    "AgentOrchestrator",
]
