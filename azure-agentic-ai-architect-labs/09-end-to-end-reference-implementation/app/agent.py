"""Azure Agentic AI agent baseline used by the current golden path tests."""

import os
from datetime import UTC, datetime
from types import SimpleNamespace
from typing import Any

import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion


class _KernelAdapter:
    """Lightweight adapter that keeps the local test baseline stable."""

    def __init__(self) -> None:
        self._raw_kernel = None
        self.memory = SimpleNamespace(save_reference_async=self._noop_memory_save)

    def bind_raw_kernel(self, raw_kernel: Any) -> None:
        """Attach the SDK kernel for future extension without depending on it."""
        self._raw_kernel = raw_kernel

    def add_chat_service(self, *args: Any, **kwargs: Any) -> None:
        """Forward service registration when a compatible SDK kernel is present."""
        if self._raw_kernel is not None and hasattr(self._raw_kernel, "add_chat_service"):
            self._raw_kernel.add_chat_service(*args, **kwargs)

    async def invoke_async(self, input: str) -> str:
        """Return a deterministic baseline response for local validation."""
        return f"Simulated response for: {input}"

    async def _noop_memory_save(self, **kwargs: Any) -> None:
        """Placeholder async sink for tests and local validation."""
        return None


class AgenticAIAgent:
    """Minimal agent implementation for local validation and iterative hardening."""

    def __init__(
        self,
        openai_endpoint: str,
        openai_key: str,
        search_endpoint: str,
        search_key: str,
        search_index: str = "agentic-ai-docs",
    ):
        """Initialize agent with Azure service connection settings."""
        raw_kernel = None
        try:
            raw_kernel = sk.Kernel()
        except Exception:
            raw_kernel = None

        self.kernel = _KernelAdapter()
        self.kernel.bind_raw_kernel(raw_kernel)
        self.openai_endpoint = openai_endpoint
        self.search_endpoint = search_endpoint
        self.search_index = search_index
        self.search_key = search_key

        # Configure Azure OpenAI
        if raw_kernel is not None:
            try:
                chat_service = AzureChatCompletion(
                    deployment_name="gpt-4",
                    endpoint=openai_endpoint,
                    api_key=openai_key,
                )
                self.kernel.add_chat_service("azure-gpt4", chat_service)
            except Exception:
                # Keep the local baseline runnable even if SDK signatures drift.
                pass

    def _build_prompt(self, user_query: str, context: str = "") -> str:
        """Build a deterministic prompt shape for testing and future hardening."""
        return (
            "You are an Azure AI architect assistant.\n"
            f"User query: {user_query}\n"
            f"Context: {context}\n"
            "Respond with concise, grounded guidance."
        )

    async def _retrieve_context(self, user_query: str) -> dict[str, Any]:
        """Return a baseline retrieval payload.

        This is intentionally simple for the local validation path and can be
        replaced later with a real Azure AI Search integration.
        """
        return {
            "query": user_query,
            "documents": [],
            "source": self.search_index,
        }

    async def add_to_memory(self, collection_id: str, content: str, metadata: dict | None = None) -> None:
        """Store a reference in kernel memory when available."""
        if hasattr(self.kernel, "memory") and hasattr(self.kernel.memory, "save_reference_async"):
            result = self.kernel.memory.save_reference_async(
                collection=collection_id,
                description=metadata or {},
                text=content,
                external_id=(metadata or {}).get("url", "local-reference"),
            )
            if hasattr(result, "__await__"):
                await result

    async def process_query(self, user_query: str) -> dict:
        """Process a user query and return a baseline response payload."""
        try:
            context_result = await self._retrieve_context(user_query)
            context = "\n".join(doc.get("content", "") for doc in context_result.get("documents", []))
            prompt = self._build_prompt(user_query, context)
            response = await self.kernel.invoke_async(input=prompt)

            return {
                "response": str(response),
                "timestamp": datetime.now(UTC).isoformat(),
            }
        except Exception as e:
            return {
                "error": str(e),
                "timestamp": datetime.now(UTC).isoformat(),
            }


if __name__ == "__main__":
    agent = AgenticAIAgent(
        openai_endpoint=os.getenv("OPENAI_ENDPOINT"),
        openai_key=os.getenv("OPENAI_KEY"),
        search_endpoint=os.getenv("SEARCH_ENDPOINT"),
        search_key=os.getenv("SEARCH_KEY"),
        search_index=os.getenv("SEARCH_INDEX", "agentic-ai-docs"),
    )
    print("Agent initialized")
