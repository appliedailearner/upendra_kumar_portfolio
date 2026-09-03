import os
import logging
from typing import Dict, Any, List
from azure.identity.aio import DefaultAzureCredential
from azure.search.documents.aio import SearchClient

logger = logging.getLogger(__name__)

async def hybrid_search(query: str, user_principal_id: str = None) -> List[Dict[str, Any]]:
    """Query the Azure AI Search Hybrid Index with Data-plane RBAC.
    
    This function demonstrates the L67 pattern for secure RAG.
    Instead of using an API key that bypasses document-level security,
    it uses DefaultAzureCredential. In a real integration, the user's
    Entra ID token or a delegated permission would be used to ensure
    the executing agent can only retrieve documents the end-user
    is authorized to see.
    """
    search_endpoint = os.environ.get("AZURE_SEARCH_ENDPOINT")
    index_name = os.environ.get("AZURE_SEARCH_INDEX", "enterprise-kb")
    
    if not search_endpoint:
        logger.warning("AZURE_SEARCH_ENDPOINT not set. Returning mock RAG data.")
        return [_mock_security_policy(), _mock_architecture_doc()]

    try:
        # L67 Architecture Requirement: Zero-Trust Keyless Auth
        # Using DefaultAzureCredential ensures we respect RBAC policies
        # attached to the Managed Identity or the authenticated user flow.
        credential = DefaultAzureCredential()
        
        async with SearchClient(endpoint=search_endpoint, index_name=index_name, credential=credential) as client:
            # Execute a hybrid search query (vector + keyword)
            # Placeholder for actual vectorization logic inside the tool
            
            # Simulated filter applying user principal ID for document-level security
            filter_str = f"authorized_users/any(u: u eq '{user_principal_id}')" if user_principal_id else None
            
            results = await client.search(
                search_text=query,
                filter=filter_str,
                top=3
            )
            
            docs = []
            async for result in results:
                docs.append({
                    "id": result.get("id", "unknown"),
                    "title": result.get("title", "Untitled Document"),
                    "content": result.get("content", ""),
                    "score": result.get("@search.score", 0.0)
                })
                
            return docs
            
    except Exception as e:
        logger.error(f"Error executing secure AI Search query: {e}")
        return [{"error": "Search failed or unauthorized."}]

def _mock_security_policy() -> Dict[str, Any]:
    return {
         "id": "sec-001",
         "title": "Agentic AI Security Baseline",
         "content": "All AI tools must operate behind an Azure APIM mediation layer.",
         "score": 0.95
    }

def _mock_architecture_doc() -> Dict[str, Any]:
    return {
         "id": "arch-042",
         "title": "Microsoft Foundry Golden Path",
         "content": "Implement Coordinator/Worker agents to handle complex enterprise tasks securely.",
         "score": 0.88
    }
