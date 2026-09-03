#!/bin/bash
set -e
LOCATION="eastus"
RESOURCE_GROUP="rg-03-semantic-kernel-track-dev"

az group create --name \ --location \ --output none
echo "Deploying Infrastructure for 03-semantic-kernel-track..."
az deployment group create --resource-group \ --template-file ../infra/main.bicep --parameters environment=dev
echo "Deployment Complete."
