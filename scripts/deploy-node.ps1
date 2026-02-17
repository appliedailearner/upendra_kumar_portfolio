# Deploy-LatencyProbe-Node.ps1
# Deploys a Node.js Function App to fix python runtime issues
# Prerequisite: az login

$ResourceGroup = "rg-portfolio-latency"
$Location = "centralindia"
$Suffix = (Get-Random -Minimum 1000 -Maximum 9999)
$StorageName = "stprobe" + $Suffix
$FunctionAppName = "func-portfolio-latency-node-" + $Suffix

Write-Host "🚀 Starting Fresh Node.js Deployment..." -ForegroundColor Cyan

# 1. Create Resource Group (Idempotent)
az group create --name $ResourceGroup --location $Location

# 2. Create Storage Account
Write-Host "Creating Storage Account: $StorageName..."
az storage account create --name $StorageName --resource-group $ResourceGroup --location $Location --sku Standard_LRS --kind StorageV2 --allow-blob-public-access true

# 3. Create Function App (Node.js 18)
Write-Host "Creating Function App: $FunctionAppName..."
# Using Node 18 LTS
az functionapp create --resource-group $ResourceGroup --consumption-plan-location $Location --runtime node --runtime-version 18 --functions-version 4 --name $FunctionAppName --storage-account $StorageName --os-type Linux

# 4. Configure App Settings
$TargetUrl = "https://$StorageName.blob.core.windows.net/"
az functionapp config appsettings set --name $FunctionAppName --resource-group $ResourceGroup --settings "TARGET_STORAGE_URL=$TargetUrl" "SCM_DO_BUILD_DURING_DEPLOYMENT=true" "WEBSITE_NODE_DEFAULT_VERSION=18"

# 5. Output Results
Write-Host "✅ Deployment Complete!" -ForegroundColor Green
Write-Host "NEW_APP_NAME=$FunctionAppName"
Write-Host "NEW_ENDPOINT=https://$FunctionAppName.azurewebsites.net/api/latency-probe"
