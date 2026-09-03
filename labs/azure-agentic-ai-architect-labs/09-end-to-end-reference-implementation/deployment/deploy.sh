#!/bin/bash
# Azure Agentic AI Reference Implementation Deployment Script
# This script deploys the complete infrastructure and application via Bicep

set -e

echo "========================================"
echo "Azure Agentic AI Deployment (Bicep/Native)"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
ENVIRONMENT=${1:-dev}
REGION=${2:-eastus}
PROJECT_NAME="agentic-ai"
WORKDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESOURCE_GROUP="rg-${PROJECT_NAME}-${ENVIRONMENT}"

echo -e "${YELLOW}Configuration:${NC}"
echo "  Environment: $ENVIRONMENT"
echo "  Region: $REGION"
echo "  Project: $PROJECT_NAME"
echo "  Target RG: $RESOURCE_GROUP"
echo ""

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"
command -v az >/dev/null 2>&1 || { echo -e "${RED}Azure CLI is required but not installed.${NC}"; exit 1; }

echo -e "${GREEN}✓ Prerequisites OK${NC}"
echo ""

# Authenticate with Azure
echo -e "${YELLOW}Checking Azure authentication...${NC}"
if ! az account show > /dev/null 2>&1; then
    echo -e "${YELLOW}Not logged in. Initiating Azure login...${NC}"
    az login --use-device-code
fi

# Get current user's principal ID for Key Vault access
echo -e "${YELLOW}Retrieving user principal ID...${NC}"
PRINCIPAL_ID=$(az ad signed-in-user show --query id -o tsv)

if [ -z "$PRINCIPAL_ID" ]; then
    echo -e "${RED}Failed to retrieve principal ID. Please check your login status.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Authentication successful (Principal ID: $PRINCIPAL_ID)${NC}"
echo ""

# Create Resource Group
echo -e "${YELLOW}Creating resource group ($RESOURCE_GROUP)...${NC}"
az group create --name "$RESOURCE_GROUP" --location "$REGION"

echo -e "${GREEN}✓ Resource group ready${NC}"
echo ""

# Deploy Bicep
echo -e "${YELLOW}Deploying infrastructure via Bicep...${NC}"
echo -e "${YELLOW}This may take 5-10 minutes. Please wait...${NC}"

# Dry-run validation check flag
VALIDATE_ONLY=${VALIDATE_ONLY:-false}

if [ "$VALIDATE_ONLY" = true ]; then
    echo -e "${YELLOW}Running in validation mode (az deployment group validate)...${NC}"
    az deployment group validate \
      --resource-group "$RESOURCE_GROUP" \
      --template-file "$WORKDIR/../infra/main.bicep" \
      --parameters environment="$ENVIRONMENT" projectName="$PROJECT_NAME" principalId="$PRINCIPAL_ID"
    echo -e "${GREEN}✓ Bicep validation completed without errors.${NC}"
    exit 0
fi

# Actual deployment
DEPLOYMENT_NAME="ai-agent-${ENVIRONMENT}-$(date +%s)"

az deployment group create \
  --name "$DEPLOYMENT_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --template-file "$WORKDIR/../infra/main.bicep" \
  --parameters environment="$ENVIRONMENT" projectName="$PROJECT_NAME" principalId="$PRINCIPAL_ID" \
  --query "properties.outputs"

echo -e "${GREEN}✓ Infrastructure deployed successfully${NC}"
echo ""

echo -e "${GREEN}Deployment Complete${NC}"
echo ""
echo "Next Steps:"
echo "  1. Check the Azure Portal for the output endpoints in the Resource Group deployments tab."
echo "  2. Configure your .env file with the generated endpoints."
echo "  3. Deploy the Python application (Phase 2)."
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}For more details, see DEPLOYMENT-GUIDE.md${NC}"
echo -e "${GREEN}========================================${NC}"
