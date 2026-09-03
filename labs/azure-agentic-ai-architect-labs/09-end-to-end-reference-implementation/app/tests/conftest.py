"""Pytest configuration and fixtures for agent tests."""

import os
import pytest
from unittest.mock import Mock, AsyncMock, patch


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Mock Azure environment variables."""
    env_vars = {
        'OPENAI_ENDPOINT': 'https://test-openai.openai.azure.com/',
        'OPENAI_KEY': 'test-key-12345',
        'SEARCH_ENDPOINT': 'https://test-search.search.windows.net',
        'SEARCH_KEY': 'test-search-key',
        'COSMOS_ENDPOINT': 'https://test-cosmos.documents.azure.com:443/',
        'COSMOS_KEY': 'test-cosmos-key',
        'ENVIRONMENT': 'test',
    }
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    return env_vars


@pytest.fixture
def mock_agent(mock_env_vars):
    """Mock agent instance for testing."""
    with patch('app.agent.AzureChatCompletion'):
        from app.agent import AgenticAIAgent
        agent = AgenticAIAgent(
            openai_endpoint=mock_env_vars['OPENAI_ENDPOINT'],
            openai_key=mock_env_vars['OPENAI_KEY'],
            search_endpoint=mock_env_vars['SEARCH_ENDPOINT'],
            search_key=mock_env_vars['SEARCH_KEY'],
        )
    return agent


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response."""
    return {
        'id': 'chatcmpl-test123',
        'object': 'text_completion',
        'created': 1234567890,
        'model': 'gpt-4',
        'choices': [
            {
                'text': 'This is a test response from the agent.',
                'index': 0,
                'finish_reason': 'stop'
            }
        ]
    }


@pytest.fixture
def mock_search_results():
    """Mock Azure Search results."""
    return {
        'value': [
            {
                '@search.score': 0.95,
                'id': 'doc-1',
                'content': 'Azure OpenAI is a managed service for deploying AI models.',
            },
            {
                '@search.score': 0.87,
                'id': 'doc-2',
                'content': 'Semantic Kernel provides orchestration for AI agents.',
            }
        ]
    }


@pytest.mark.asyncio
async def test_async_agent():
    """Test async agent functionality."""
    pass
