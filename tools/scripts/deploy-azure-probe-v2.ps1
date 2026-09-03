# Deploy-LatencyProbe-v2.ps1
# Deploys a FRESH Storage Account and Function App to fix corruption issues
# Prerequisite: az login

$ResourceGroup = "rg-portfolio-latency"
$Location = "centralindia"
$Suffix = (Get-Random -Minimum 1000 -Maximum 9999)
$StorageName = "stprobe" + $Suffix
$FunctionAppName = "func-portfolio-latency-py-" + $Suffix

Write-Host "🚀 Starting Fresh Deployment (Recovery Mode)..." -ForegroundColor Cyan

# 1. Create Resource Group (Idempotent)
Write-Host "Checking Resource Group: $ResourceGroup..."
az group create --name $ResourceGroup --location $Location

# 2. Create Storage Account (New Unique Name)
Write-Host "Creating FRESH Storage Account: $StorageName..."
az storage account create --name $StorageName --resource-group $ResourceGroup --location $Location --sku Standard_LRS --kind StorageV2 --allow-blob-public-access true

# 3. Create Function App (Python 3.11)
Write-Host "Creating FRESH Function App: $FunctionAppName..."
# Note: osc-type Linux is required for Python Consumption
az functionapp create --resource-group $ResourceGroup --consumption-plan-location $Location --runtime python --runtime-version 3.11 --functions-version 4 --name $FunctionAppName --storage-account $StorageName --os-type Linux

# 4. Configure App Settings
$TargetUrl = "https://$StorageName.blob.core.windows.net/"
az functionapp config appsettings set --name $FunctionAppName --resource-group $ResourceGroup --settings "TARGET_STORAGE_URL=$TargetUrl" "SCM_DO_BUILD_DURING_DEPLOYMENT=true" "ENABLE_ORYX_BUILD=true"

# 5. Output Results for Agent to Parse
Write-Host "✅ Deployment Complete!" -ForegroundColor Green
Write-Host "NEW_APP_NAME=$FunctionAppName"
Write-Host "NEW_ENDPOINT=https://$FunctionAppName.azurewebsites.net/api/latency-probe"
