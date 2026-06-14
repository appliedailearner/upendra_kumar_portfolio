#!/bin/bash
set -e
LOCATION="eastus"
RESOURCE_GROUP="rg-05-rag-with-azure-ai-search-dev"

az group create --name \ --location \ --output none
echo "Deploying Infrastructure for 05-rag-with-azure-ai-search..."
az deployment group create --resource-group \ --template-file ../infra/main.bicep --parameters environment=dev
echo "Deployment Complete."
