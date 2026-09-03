"""Agent Orchestrator.

Manages multiple agents and their coordination.
"""

from typing import Any, Dict, List, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class AgentRole(Enum):
    """Enumeration of agent roles."""

    PLANNER = "planner"
    EXECUTOR = "executor"
    VALIDATOR = "validator"
    REPORTER = "reporter"


class AgentOrchestrator:
    """Orchestrates multiple agents for coordinated execution."""

    def __init__(self, name: str = "Orchestrator") -> None:
        """Initialize the orchestrator.

        Args:
            name: Orchestrator name
        """
        self.name = name
        self.agents: Dict[str, Dict[str, Any]] = {}
        self.execution_history: List[Dict[str, Any]] = []

    def register_agent(
        self, agent_id: str, agent: Any, role: AgentRole
    ) -> None:
        """Register an agent with the orchestrator.

        Args:
            agent_id: Unique agent identifier
            agent: Agent instance
            role: Agent role
        """
        self.agents[agent_id] = {"agent": agent, "role": role}
        logger.info(f"Registered agent {agent_id} with role {role.value}")

    async def execute_sequential(
        self, agent_ids: List[str], **kwargs: Any
    ) -> Dict[str, Any]:
        """Execute agents sequentially.

        Args:
            agent_ids: List of agent IDs to execute
            **kwargs: Execution parameters

        Returns:
            Dictionary with execution results
        """
        results = {}
        for agent_id in agent_ids:
            if agent_id in self.agents:
                agent = self.agents[agent_id]["agent"]
                try:
                    result = await agent.execute(**kwargs)
                    results[agent_id] = result
                    self.execution_history.append(
                        {"agent_id": agent_id, "result": result}
                    )
                except Exception as e:
                    logger.error(f"Error executing {agent_id}: {e}")
                    results[agent_id] = {"status": "error", "error": str(e)}
        return results

    def get_execution_history(
        self,
    ) -> List[Dict[str, Any]]:
        """Get execution history.

        Returns:
            List of execution records
        """
        return self.execution_history
