# Deploy-LatencyProbe.ps1
# Deploys a Storage Account (Target) and a Function App (Probe)
# Prerequisite: az login

$ResourceGroup = "rg-portfolio-latency"
$Location = "centralindia"
$StorageName = "stlatencyprobe" + (Get-Random -Minimum 1000 -Maximum 9999)
$FunctionAppName = "func-portfolio-latency-" + (Get-Random -Minimum 1000 -Maximum 9999)

Write-Host "🚀 Starting Deployment..." -ForegroundColor Cyan

# 1. Create Resource Group
Write-Host "Creating Resource Group: $ResourceGroup..."
az group create --name $ResourceGroup --location $Location

# 2. Create Storage Account (The Ping Target)
Write-Host "Creating Storage Account: $StorageName..."
az storage account create --name $StorageName --resource-group $ResourceGroup --location $Location --sku Standard_LRS --kind StorageV2 --allow-blob-public-access true

# 3. Create Function App
Write-Host "Creating Function App: $FunctionAppName..."
az functionapp create --resource-group $ResourceGroup --consumption-plan-location $Location --runtime node --runtime-version 18 --functions-version 4 --name $FunctionAppName --storage-account $StorageName

# 4. Configure App Settings (Target URL)
$TargetUrl = "https://$StorageName.blob.core.windows.net/"
az functionapp config appsettings set --name $FunctionAppName --resource-group $ResourceGroup --settings "TARGET_STORAGE_URL=$TargetUrl"

# 5. Output Results
Write-Host "✅ Deployment Complete!" -ForegroundColor Green
Write-Host "--------------------------------------------------"
Write-Host "Function App Name: $FunctionAppName"
Write-Host "Target Storage: $StorageName"
Write-Host "API Endpoint: https://$FunctionAppName.azurewebsites.net/api/latency-probe"
Write-Host "--------------------------------------------------"
Write-Host "👉 ACTION REQUIRED: Deploy the code in 'api/latency-probe' to this Function App."
Write-Host "    Command: cd api; func azure functionapp publish $FunctionAppName"
