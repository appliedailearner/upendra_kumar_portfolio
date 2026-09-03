"""Unit tests for AgenticAIAgent."""

import pytest
from unittest.mock import Mock, patch, MagicMock


class TestAgenticAIAgent:
    """Test suite for AgenticAIAgent class."""

    def test_agent_initialization(self, mock_env_vars):
        """Test agent can be initialized with Azure credentials."""
        from app.agent import AgenticAIAgent
        
        with patch('app.agent.sk.Kernel'):
            agent = AgenticAIAgent(
                openai_endpoint=mock_env_vars['OPENAI_ENDPOINT'],
                openai_key=mock_env_vars['OPENAI_KEY'],
                search_endpoint=mock_env_vars['SEARCH_ENDPOINT'],
                search_key=mock_env_vars['SEARCH_KEY'],
            )
            assert agent is not None
            assert agent.openai_endpoint == mock_env_vars['OPENAI_ENDPOINT']

    def test_agent_initialization_with_search_index(self, mock_env_vars):
        """Test agent initialization with custom search index name."""
        from app.agent import AgenticAIAgent
        
        with patch('app.agent.sk.Kernel'):
            custom_index = "my-custom-index"
            agent = AgenticAIAgent(
                openai_endpoint=mock_env_vars['OPENAI_ENDPOINT'],
                openai_key=mock_env_vars['OPENAI_KEY'],
                search_endpoint=mock_env_vars['SEARCH_ENDPOINT'],
                search_key=mock_env_vars['SEARCH_KEY'],
                search_index=custom_index,
            )
            assert agent.search_index == custom_index

    @pytest.mark.asyncio
    async def test_process_query(self, mock_agent):
        """Test agent can process a query."""
        mock_agent.kernel.invoke_async = Mock(return_value="Test response")
        
        result = await mock_agent.process_query("What is Azure OpenAI?")
        
        assert result is not None
        assert "timestamp" in result

    @pytest.mark.asyncio
    async def test_process_query_error_handling(self, mock_agent):
        """Test agent handles errors gracefully."""
        mock_agent.kernel.invoke_async = Mock(side_effect=Exception("API Error"))
        
        result = await mock_agent.process_query("Test query")
        
        assert "error" in result
        assert "API Error" in result["error"]

    @pytest.mark.asyncio
    async def test_add_to_memory(self, mock_agent):
        """Test agent can add content to memory."""
        mock_agent.kernel.memory.save_reference_async = Mock()
        
        await mock_agent.add_to_memory(
            collection_id="test-collection",
            content="Test content",
            metadata={"url": "http://example.com"}
        )
        
        mock_agent.kernel.memory.save_reference_async.assert_called_once()

    def test_build_prompt(self, mock_agent):
        """Test prompt building with context."""
        user_query = "How to deploy on Azure?"
        context = "Azure is a cloud platform."
        
        prompt = mock_agent._build_prompt(user_query, context)
        
        assert user_query in prompt
        assert context in prompt
        assert "Azure AI architect" in prompt

    @pytest.mark.asyncio
    async def test_retrieve_context(self, mock_agent):
        """Test context retrieval from search."""
        result = await mock_agent._retrieve_context("test query")
        
        assert isinstance(result, dict)
        assert "documents" in result
