#!/bin/bash
set -e
LOCATION="eastus"
RESOURCE_GROUP="rg-02-foundry-agent-service-dev"

az group create --name \ --location \ --output none
echo "Deploying Infrastructure for 02-foundry-agent-service..."
az deployment group create --resource-group \ --template-file ../infra/main.bicep --parameters environment=dev
echo "Deployment Complete."
