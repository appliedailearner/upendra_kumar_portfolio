# Model Context Protocol (MCP) - Complete Documentation Package

**Project**: Azure Landing Zones - Financial Services  
**Component**: Model Context Protocol (MCP) Integration  
**Version**: 1.0.0  
**Last Updated**: December 2025

---

## 1. Overview & Design Decisions

### What is MCP?

Model Context Protocol (MCP) is an open protocol that standardizes how applications provide context to Large Language Models (LLMs). It enables AI models to securely access data, tools, and services while maintaining governance and compliance.

### Architecture Decision

**Deployment Model**: Containerized MCP Servers on Azure Kubernetes Service (AKS)

**Rationale**:
- Scalability and high availability
- Integration with existing Azure services
- Secure communication via private endpoints
- Compliance with Financial Services regulations

---

## 2. Architecture Overview

### System Design

```
AI Applications (Azure OpenAI, Copilot Studio)
    ↓
MCP Client SDK
    ↓
API Management (Authentication, Rate Limiting)
    ↓
MCP Server Cluster (AKS)
    ├── Financial Data MCP Server
    ├── Customer Context MCP Server
    ├── Compliance MCP Server
    └── Document Retrieval MCP Server
    ↓
Backend Data Sources
    ├── Azure SQL Database
    ├── Cosmos DB
    ├── Azure AI Search
    └── On-Premises Systems (via ExpressRoute)
```

### Key Components

**MCP Servers**:
1. **Financial Data Server**: Real-time access to transaction data, account balances
2. **Customer Context Server**: Customer profiles, preferences, interaction history
3. **Compliance Server**: Regulatory rules, compliance checks, audit trails
4. **Document Retrieval Server**: Policy documents, procedures, knowledge base

**Supporting Infrastructure**:
- Azure Kubernetes Service (AKS) for hosting
- Azure API Management for gateway
- Azure Key Vault for secrets
- Azure Monitor for observability
- Azure SQL Database for metadata

---

## 3. MCP Server Implementation

### Financial Data MCP Server

**Capabilities**:
```json
{
  "name": "financial-data-server",
  "version": "1.0.0",
  "capabilities": {
    "resources": [
      {
        "uri": "account://balance/{accountId}",
        "name": "Account Balance",
        "description": "Retrieve current account balance"
      },
      {
        "uri": "transaction://history/{accountId}",
        "name": "Transaction History",
        "description": "Get transaction history for account"
      }
    ],
    "tools": [
      {
        "name": "calculate_interest",
        "description": "Calculate interest for given principal and rate",
        "inputSchema": {
          "type": "object",
          "properties": {
            "principal": {"type": "number"},
            "rate": {"type": "number"},
            "term": {"type": "number"}
          }
        }
      }
    ]
  }
}
```

**Implementation** (Python):
```python
from mcp.server import Server, Resource, Tool
from mcp.types import TextContent
import asyncio

app = Server("financial-data-server")

@app.resource("account://balance/{account_id}")
async def get_account_balance(account_id: str) -> Resource:
    # Fetch from Azure SQL Database
    balance = await fetch_balance_from_db(account_id)
    return Resource(
        uri=f"account://balance/{account_id}",
        name=f"Balance for {account_id}",
        mimeType="application/json",
        text=json.dumps({"balance": balance, "currency": "USD"})
    )

@app.tool("calculate_interest")
async def calculate_interest(principal: float, rate: float, term: int) -> list[TextContent]:
    interest = principal * (rate / 100) * term
    return [TextContent(
        type="text",
        text=f"Interest: ${interest:.2f}"
    )]

if __name__ == "__main__":
    asyncio.run(app.run())
```

---

## 4. Security & Compliance

### Authentication & Authorization

**OAuth 2.0 Flow**:
1. AI application requests access token from Azure AD
2. Token includes scopes for specific MCP resources
3. MCP server validates token via APIM
4. Fine-grained access control based on user roles

**Authorization Matrix**:
| Role | Financial Data | Customer Context | Compliance | Documents |
|------|---------------|------------------|------------|-----------|
| Customer Service Agent | Read (own customers) | Read/Write | Read | Read |
| Financial Advisor | Read | Read | Read | Read |
| Compliance Officer | Read | Read | Read/Write | Read/Write |
| System Admin | Full | Full | Full | Full |

### Data Protection

**Encryption**:
- TLS 1.3 for all MCP communications
- Data at rest encrypted with CMK
- Sensitive fields masked in logs

**Audit Logging**:
```json
{
  "timestamp": "2025-12-19T19:30:00Z",
  "user": "agent@contoso.com",
  "action": "resource.read",
  "resource": "account://balance/123456",
  "result": "success",
  "ip_address": "10.100.1.50",
  "correlation_id": "abc-123-def-456"
}
```

---

## 5. Bill of Materials

### Monthly Costs

| Resource | Configuration | Monthly Cost (USD) |
|----------|--------------|-------------------|
| AKS Cluster | 3 nodes, Standard_D4s_v5 | $360 |
| Azure SQL Database | S3 (100 DTU) | $150 |
| API Management | Developer tier | $50 |
| Azure Monitor | 20 GB/month | $46 |
| Key Vault | Standard | $5 |
| **Total Monthly** | | **$611** |

---

## 6. Deployment Configuration

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: financial-data-mcp-server
  namespace: mcp-servers
spec:
  replicas: 3
  selector:
    matchLabels:
      app: financial-data-mcp
  template:
    metadata:
      labels:
        app: financial-data-mcp
    spec:
      containers:
      - name: mcp-server
        image: acrprodeus2ai01.azurecr.io/mcp-financial-data:1.0.0
        ports:
        - containerPort: 8080
        env:
        - name: AZURE_SQL_CONNECTION_STRING
          valueFrom:
            secretKeyRef:
              name: mcp-secrets
              key: sql-connection-string
        - name: AZURE_KEY_VAULT_URL
          value: "https://kv-prod-eus2-mcp-01.vault.azure.net"
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: financial-data-mcp-service
  namespace: mcp-servers
spec:
  selector:
    app: financial-data-mcp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: ClusterIP
```

---

## 7. Integration with Azure OpenAI

### Client Configuration

```python
from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Initialize MCP client
server_params = StdioServerParameters(
    command="docker",
    args=["run", "-i", "mcp-financial-data-server"],
    env={"API_KEY": get_secret_from_keyvault("mcp-api-key")}
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        
        # List available resources
        resources = await session.list_resources()
        
        # Read account balance
        balance = await session.read_resource("account://balance/123456")
        
        # Use with Azure OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a financial advisor."},
                {"role": "user", "content": f"What's my account balance? Context: {balance}"}
            ]
        )
```

---

## 8. Monitoring & Operations

### Key Metrics

| Metric | Target | Alert Threshold |
|--------|--------|----------------|
| Request Latency (P95) | < 200ms | > 500ms |
| Error Rate | < 0.1% | > 1% |
| Availability | 99.9% | < 99.5% |
| Concurrent Connections | < 1000 | > 1500 |

### Dashboards

**MCP Server Dashboard**:
- Request volume by server
- Latency distribution
- Error rates and types
- Resource utilization (CPU, memory)
- Active connections

**Security Dashboard**:
- Authentication failures
- Authorization denials
- Suspicious access patterns
- Audit log summary

---

## 9. Operational Procedures

### Common Tasks

**Deploy New MCP Server**:
```bash
# Build container image
docker build -t acrprodeus2ai01.azurecr.io/mcp-new-server:1.0.0 .

# Push to ACR
az acr login --name acrprodeus2ai01
docker push acrprodeus2ai01.azurecr.io/mcp-new-server:1.0.0

# Deploy to AKS
kubectl apply -f mcp-new-server-deployment.yaml
kubectl rollout status deployment/mcp-new-server -n mcp-servers
```

**Scale MCP Server**:
```bash
kubectl scale deployment financial-data-mcp-server --replicas=5 -n mcp-servers
```

**View Logs**:
```bash
kubectl logs -f deployment/financial-data-mcp-server -n mcp-servers
```

### Troubleshooting

**Issue**: High latency on MCP requests  
**Solution**:
1. Check backend database performance
2. Review MCP server resource utilization
3. Verify network connectivity
4. Check for slow queries

**Issue**: Authentication failures  
**Solution**:
1. Validate Azure AD token
2. Check APIM policies
3. Verify Key Vault access
4. Review audit logs

---

## 10. Support & Handover

### Support Contacts
- **L1 Support**: mcp-support@contoso.com (8/5)
- **L2 Support**: ai-platform-ops@contoso.com (24/7)
- **L3 Engineering**: mcp-engineering@contoso.com (8/5)

### Known Issues
| Issue | Workaround | Target Fix |
|-------|------------|------------|
| Occasional timeout on large datasets | Implement pagination | Q1 2026 |
| Memory leak in long-running sessions | Restart pods daily | Q1 2026 |

---

## References
- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Azure OpenAI + MCP Integration](https://learn.microsoft.com/azure/ai-services/openai/)

---

**Document Owner**: AI Platform Architect  
**Status**: Production Ready  
**Last Review**: December 2025  
**Next Review**: March 2026
