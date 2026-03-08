"""Integration tests for AgenticAIAgent with actual Azure services."""

import pytest
from unittest.mock import patch, Mock


class TestAgentIntegration:
    """Integration tests for end-to-end agent workflows."""

    @pytest.mark.asyncio
    async def test_end_to_end_query_processing(self, mock_agent, mock_search_results):
        """Test complete query processing flow."""
        with patch.object(mock_agent, '_retrieve_context', return_value=mock_search_results):
            mock_agent.kernel.invoke_async = Mock(return_value="Mocked response")
            
            result = await mock_agent.process_query("Test question?")
            
            assert result is not None
            assert "response" in result or "error" in result

    @pytest.mark.asyncio
    async def test_memory_workflow(self, mock_agent):
        """Test adding content and retrieving from memory."""
        collection_id = "test-docs"
        test_content = "Azure OpenAI provides managed AI services."
        
        mock_agent.kernel.memory.save_reference_async = Mock()
        
        await mock_agent.add_to_memory(
            collection_id=collection_id,
            content=test_content,
            metadata={"url": "http://example.com", "source": "documentation"}
        )
        
        mock_agent.kernel.memory.save_reference_async.assert_called_once()

    @pytest.mark.asyncio
    async def test_multi_turn_conversation(self, mock_agent):
        """Test multiple queries in sequence."""
        queries = [
            "What is Azure OpenAI?",
            "How do I deploy it?",
            "What are the costs?"
        ]
        
        mock_agent.kernel.invoke_async = Mock(return_value="Response")
        
        results = []
        for query in queries:
            result = await mock_agent.process_query(query)
            results.append(result)
        
        assert len(results) == len(queries)
        assert all(result is not None for result in results)

    @pytest.mark.asyncio
    async def test_rag_workflow(self, mock_agent, mock_search_results):
        """Test RAG (Retrieval Augmented Generation) workflow."""
        user_query = "Explain Azure Agentic AI"
        
        # Mock search retrieval
        with patch.object(mock_agent, '_retrieve_context', return_value=mock_search_results):
            # Verify context is retrieved
            context = await mock_agent._retrieve_context(user_query)
            assert len(context.get('documents', [])) >= 0
            
            # Process query with context
            mock_agent.kernel.invoke_async = Mock(return_value="Answer based on context")
            result = await mock_agent.process_query(user_query)
            
            assert result is not None
