import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

async def sync_crm_contact(contact_data: Dict[str, Any]) -> Dict[str, str]:
    """Sync contact data to external CRM via API Mediation Layer.
    
    This function demonstrates modifying external state safely.
    It expects the 'contact_data' payload determined by the Worker Agent.
    """
    logger.info(f"crm-integration-tool invoked for contact: {contact_data.get('email')}")
    
    # In the reference architecture, this call hits an Azure APIM endpoint
    # that routes to an Azure Function, checking OAuth scopes before hitting Dynamics/Salesforce.
    
    return {
        "status": "success",
        "message": "Contact synchronized successfully through APIM Mediation Gateway.",
        "crm_id": "CRM-8849-ZZ"
    }
