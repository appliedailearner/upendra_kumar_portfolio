import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

async def lookup_sales_data(customer_id: str) -> Dict[str, Any]:
    """Retrieve mock sales data for a customer.
    
    This simulates an external tool call to an ERP/CRM system.
    In the L67 reference architecture, this would go through the
    API Mediation Layer (APIM) rather than hitting the DB directly.
    """
    logger.info(f"sales-lookup-tool invoked for customer: {customer_id}")
    
    # Mock data return
    return {
        "customer_id": customer_id,
        "ytd_sales": 1250000.00,
        "currency": "USD",
        "last_order_date": "2023-11-15",
        "account_status": "Active (Tier 1)"
    }
