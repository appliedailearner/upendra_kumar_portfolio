#!/bin/bash
set -e
LOCATION="eastus"
RESOURCE_GROUP="rg-07-secure-reference-architecture-dev"

az group create --name \ --location \ --output none
echo "Deploying Infrastructure for 07-secure-reference-architecture..."
az deployment group create --resource-group \ --template-file ../infra/main.bicep --parameters environment=dev
echo "Deployment Complete."
