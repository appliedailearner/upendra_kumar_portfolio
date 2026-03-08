#!/bin/bash
set -e
LOCATION="eastus"
RESOURCE_GROUP="rg-08-observability-and-evaluation-dev"

az group create --name \ --location \ --output none
echo "Deploying Infrastructure for 08-observability-and-evaluation..."
az deployment group create --resource-group \ --template-file ../infra/main.bicep --parameters environment=dev
echo "Deployment Complete."
