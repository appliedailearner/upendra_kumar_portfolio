# Quick Start: 10-Minute Setup

Get the Azure Agentic AI Architect Labs running on your machine in 10 minutes.

## Prerequisites

Before starting, ensure you have:

- **Python 3.9+** - [Install here](https://www.python.org/downloads/)
- **Azure subscription** - [Free account](https://azure.microsoft.com/free/)
- **Azure CLI** - [Install here](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
- **Git** - [Install here](https://git-scm.com/downloads)
- **VS Code** (optional but recommended) - [Install here](https://code.visualstudio.com/)

## 1. Clone the Repository (1 minute)

```bash
git clone https://github.com/appliedailearner/azure-agentic-ai-architect-labs.git
cd azure-agentic-ai-architect-labs
```

## 2. Set Up Python Environment (2 minutes)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Configure Azure Credentials (2 minutes)

```bash
# Login to Azure
az login

# Set your subscription
az account set --subscription "YOUR_SUBSCRIPTION_ID"

# Verify you're logged in
az account show
```

## 4. Deploy the Golden Path Solution (5 minutes)

```bash
cd 09-end-to-end-reference-implementation/deployment

# Copy environment template
cp .env.example .env

# Edit .env with your Azure details
# Required variables:
# - AZURE_SUBSCRIPTION_ID
# - AZURE_RESOURCE_GROUP
# - AZURE_LOCATION (e.g., eastus, westeurope)
# - ENVIRONMENT (dev, prod)

# Deploy using Bicep
./deploy.sh

# Wait for deployment to complete (~5 minutes)
```

## 5. Verify Deployment (1 minute)

```bash
# Validate all resources were created
./verify-deployment.sh

# Expected output:
# ✓ Foundry Agent Service: RUNNING
# ✓ Azure AI Search: RUNNING
# ✓ APIM Gateway: RUNNING
# ✓ Application Insights: RUNNING
```

## Next Steps

### Option A: Explore the Golden Path (20-30 minutes)
Learn how the solution works:

```bash
cd ..
jupyter notebook notebooks/end-to-end-walkthrough.ipynb
```

### Option B: Run the Agent (10 minutes)
Interact with the deployed agent:

```bash
python app/agent-service.py

# You'll see a prompt:
# Agent ready. Ask a question or type 'exit' to quit:
# > What are the top products in our catalog?
```

### Option C: Follow the Full Curriculum (20+ hours)
Start with Module 1:

```bash
cd ../../../01-foundry-foundations
cat README.md
```

## Troubleshooting

### Issue: "Python 3.9+ not found"
```bash
# Check Python version
python --version

# If you have multiple Python versions:
python3.9 -m venv venv
```

### Issue: "Azure CLI not authenticated"
```bash
# Re-authenticate
az login --use-device-code
az account set --subscription YOUR_SUBSCRIPTION_ID
```

### Issue: "Deployment failed"
```bash
# Check deployment status
az deployment group list --resource-group YOUR_RG

# View detailed error
az deployment group show --resource-group YOUR_RG --name main
```

### Issue: "Module not found" errors
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

## Common Questions

**Q: How much will this cost?**
A: ~$10-20/day for the full stack. See [cost-and-finops.md](./09-end-to-end-reference-implementation/cost-and-finops.md) for details.

**Q: Can I use a different Azure region?**
A: Yes! Edit `.env` and set `AZURE_LOCATION` to any supported region.

**Q: How do I clean up resources?**
A: Run `./cleanup.sh` to delete all Azure resources.

**Q: What if I want to customize the solution?**
A: See [GOLDEN-PATH.md](./09-end-to-end-reference-implementation/GOLDEN-PATH.md) for customization guide.

## Resources

- **Full Documentation**: [README.md](./README.md)
- **Golden Path Guide**: [GOLDEN-PATH.md](./09-end-to-end-reference-implementation/GOLDEN-PATH.md)
- **Architecture Overview**: [ARCHITECTURE.md](./ARCHITECTURE.md)
- **Module 1**: [01-foundry-foundations](./01-foundry-foundations/README.md)
- **Troubleshooting**: [docs/TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md)

## Support

Stuck? Here's what to do:

1. Check [Troubleshooting](#troubleshooting) section above
2. See [docs/FAQ.md](./docs/FAQ.md) for common questions
3. Check [Module Prerequisites](./01-foundry-foundations/prerequisites.md)
4. Open a [GitHub Issue](https://github.com/appliedailearner/azure-agentic-ai-architect-labs/issues)

---

**Estimated time to running agent: 10-15 minutes**

Once deployment completes, you'll have a production-grade Agentic AI solution with evaluation frameworks, observability, and secure architecture.

Ready to dive deeper? Head to [GOLDEN-PATH.md](./09-end-to-end-reference-implementation/GOLDEN-PATH.md) for the complete walkthrough!
