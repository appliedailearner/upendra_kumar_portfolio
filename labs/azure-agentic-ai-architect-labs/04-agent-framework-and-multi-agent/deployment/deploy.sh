#!/bin/bash
set -e
LOCATION="eastus"
RESOURCE_GROUP="rg-04-agent-framework-and-multi-agent-dev"

az group create --name \ --location \ --output none
echo "Deploying Infrastructure for 04-agent-framework-and-multi-agent..."
az deployment group create --resource-group \ --template-file ../infra/main.bicep --parameters environment=dev
echo "Deployment Complete."
