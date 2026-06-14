# Deployment Guide: Azure Agentic AI Reference Implementation

## Overview

This guide provides step-by-step instructions to deploy the complete Azure Agentic AI end-to-end reference implementation, including infrastructure setup, application deployment, and CI/CD configuration.

**Time to Deploy**: 45-60 minutes (first deployment)
**Prerequisites**: Azure CLI, Terraform, Python 3.9+, Git

## Prerequisites

### Required Tools

- **Azure CLI** ([Install](https://docs.microsoft.com/cli/azure/install-azure-cli))
- **Terraform** 1.5+ ([Install](https://www.terraform.io/downloads.html))
- **Python** 3.9+ ([Install](https://www.python.org/downloads/))
- **Git** ([Install](https://git-scm.com/downloads))

### Azure Permissions

Your Azure account must have:
- `Subscription Contributor` or `Owner` role
- Permissions to create Azure AI Foundry resources
- Permissions to manage Key Vault secrets

### Environment Setup

```bash
# Clone the repository
git clone https://github.com/appliedailearner/azure-agentic-ai-architect-labs.git
cd azure-agentic-ai-architect-labs/09-end-to-end-reference-implementation

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 1: Infrastructure Deployment

### 1.1 Authenticate with Azure

```bash
az login --use-device-code
```

Select your subscription:

```bash
az account set --subscription "<your-subscription-id>"
```

### 1.2 Deploy Infrastructure with Terraform

```bash
cd deployment
bash deploy.sh dev eastus
```

The script will:
1. Validate Terraform configuration
2. Create a deployment plan
3. Prompt for confirmation
4. Deploy all infrastructure resources
5. Output connection endpoints

### 1.3 Capture Deployment Outputs

After successful deployment, note the following outputs:

```
OpenAI Endpoint: https://<name>.openai.azure.com/
Search Endpoint: https://<name>.search.windows.net
Key Vault URI: https://<name>.vault.azure.net/
Resource Group: rg-agentic-ai-dev
```

## Step 2: Application Configuration

### 2.1 Create Environment Configuration

Create a `.env` file in the project root:

```bash
cat > .env << 'EOF'
# Azure OpenAI Configuration
OPENAI_ENDPOINT=https://<your-name>.openai.azure.com/
OPENAI_KEY=<your-openai-api-key>
OPENAI_MODEL=gpt-4

# Azure Search Configuration
SEARCH_ENDPOINT=https://<your-name>.search.windows.net
SEARCH_KEY=<your-search-api-key>
SEARCH_INDEX=agentic-ai-docs

# Cosmos DB Configuration (optional)
COSMOS_ENDPOINT=https://<your-name>.documents.azure.com:443/
COSMOS_KEY=<your-cosmos-key>
COSMOS_DATABASE=agentic-ai-db

# Environment
ENVIRONMENT=dev
EOF
```

### 2.2 Retrieve Secrets from Key Vault

```bash
# Get OpenAI key from Key Vault
az keyvault secret show \
  --vault-name kv-agentic-ai-dev \
  --name openai-api-key \
  --query value -o tsv

# Get Search key from Key Vault
az keyvault secret show \
  --vault-name kv-agentic-ai-dev \
  --name search-api-key \
  --query value -o tsv
```

## Step 3: Application Deployment

### 3.1 Verify Agent Implementation

```bash
cd app
python -m pytest tests/test_agent.py -v
```

### 3.2 Run Agent Application

```bash
# Interactive mode
python agent.py

# Or with specific query
python agent.py --query "How do I deploy on Azure?"
```

### 3.3 Test End-to-End Flow

```bash
# Run integration tests
python -m pytest tests/test_integration.py -v
```

## Step 4: CI/CD Pipeline Setup

### 4.1 GitHub Actions Configuration

The repository includes GitHub Actions workflows for:
- Infrastructure validation and testing
- Python application testing
- Automated deployment on merge to main

Workflows are located in: `.github/workflows/`

### 4.2 Enable GitHub Actions

1. Go to your GitHub repository
2. Navigate to **Settings** > **Actions** > **General**
3. Enable **Actions** and **Workflows**
4. Configure secrets:
   - `AZURE_SUBSCRIPTION_ID`
   - `AZURE_CREDENTIALS` (service principal)
   - `OPENAI_API_KEY`

### 4.3 Deploy Service Principal for CI/CD

```bash
# Create service principal
az ad sp create-for-rbac \
  --name "agentic-ai-cicd" \
  --role contributor \
  --scopes /subscriptions/<subscription-id>

# Add the output as GitHub secret: AZURE_CREDENTIALS
```

## Step 5: Validation and Testing

### 5.1 Verify Infrastructure

```bash
# List deployed resources
az resource list --resource-group rg-agentic-ai-dev

# Check Azure Search index
az search admin-key show \
  --resource-group rg-agentic-ai-dev \
  --service-name search-agentic-ai-dev
```

### 5.2 Test Agent Functionality

```bash
# Health check endpoint
curl https://<agent-endpoint>/health

# Query the agent
curl -X POST https://<agent-endpoint>/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Azure Agentic AI?"}'
```

### 5.3 Load Testing

```bash
# Run load tests
python tests/load_test.py \
  --endpoint https://<agent-endpoint> \
  --queries 100 \
  --concurrent 10
```

## Step 6: Monitoring and Maintenance

### 6.1 Configure Monitoring

```bash
# Enable Azure Monitor for resources
az monitor diagnostic-settings create \
  --resource /subscriptions/<id>/resourceGroups/rg-agentic-ai-dev/providers/Microsoft.CognitiveServices/accounts/<name> \
  --name agentic-ai-monitoring \
  --workspace <workspace-id>
```

### 6.2 View Logs

```bash
# Stream logs from Key Vault
az keyvault logging update \
  --vault-name kv-agentic-ai-dev \
  --enable-for-deployment true \
  --enable-for-template-deployment true
```

## Troubleshooting

### Issue: "Insufficient quota for deployment"

**Solution**: Check Azure limits and request increases

```bash
az compute vm usage list --location eastus
```

### Issue: "Azure Search index not found"

**Solution**: Populate the search index

```bash
python -c "from app.search import populate_index; populate_index()"
```

### Issue: "OpenAI quota exceeded"

**Solution**: Check deployment quota and adjust model

```bash
az cognitiveservices account list --resource-group rg-agentic-ai-dev
```

## Cost Optimization

### Development Environment

For development, use lower-tier resources:

```bash
bash deploy.sh dev eastus --search-sku basic --cosmosdb-throughput 400
```

### Production Environment

For production, use high-availability settings:

```bash
bash deploy.sh prod eastus --search-sku standard3 --cosmosdb-throughput 4000
```

## Cleanup

To remove all resources and avoid charges:

```bash
# Destroy Terraform infrastructure
cd infra
terraform destroy -var="environment=dev"

# Alternatively, delete resource group
az group delete --name rg-agentic-ai-dev --yes
```

## Next Steps

1. **Customize the agent**: Modify `app/agent.py` for your use case
2. **Add more tools**: Implement custom agent tools in `app/tools/`
3. **Scale the deployment**: Use load balancers and auto-scaling
4. **Integrate with your systems**: Connect to internal databases and APIs
5. **Deploy to production**: Use separate Terraform workspaces for prod

## Additional Resources

- [Azure AI Foundry Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [Semantic Kernel Documentation](https://learn.microsoft.com/en-us/semantic-kernel/)
- [Terraform Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest)
- [Azure OpenAI Best Practices](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/)

## Support

For issues or questions:
1. Check the [GitHub Issues](https://github.com/appliedailearner/azure-agentic-ai-architect-labs/issues)
2. Review module-specific READMEs
3. Consult Azure documentation
4. Open a GitHub Discussion
