#!/bin/bash
set -e
LOCATION="eastus"
RESOURCE_GROUP="rg-06-mcp-and-enterprise-tooling-dev"

az group create --name \ --location \ --output none
echo "Deploying Infrastructure for 06-mcp-and-enterprise-tooling..."
az deployment group create --resource-group \ --template-file ../infra/main.bicep --parameters environment=dev
echo "Deployment Complete."
