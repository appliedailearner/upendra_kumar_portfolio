# Simplified Azure Deployment
param([string]$StorageAccount = "porfolioupendrakumar", [string]$Container = "`$web", [switch]$Force)
$ErrorActionPreference = "Stop"

Write-Host "Deploying to $StorageAccount..." -ForegroundColor Cyan

# Prepare
$sourceDir = Get-Location
$tempDir = Join-Path $env:TEMP "portfolio-deploy-$(Get-Date -Format 'yyyyMMddHHmmss')"
New-Item -ItemType Directory -Path $tempDir -Force | Out-Null

$exclude = @('.git', '.github', '.venv', 'node_modules', 'site_backups', '*.md', '*.py', '*.ps1', 'appliedailearner.github.io', 'azure-landing-zones-project', 'azure-projects', 'portfolio-deploy', 'portfolio-template', 'master prompts')

Get-ChildItem -Path $sourceDir -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
    $rel = $_.FullName.Substring($sourceDir.Path.Length + 1)
    $skip = $false
    foreach ($p in $exclude) { if ($rel -like "*$p*") { $skip = $true; break } }
    
    if (-not $skip) {
        $dest = Join-Path $tempDir $rel
        if ($_.PSIsContainer) { New-Item -ItemType Directory -Path $dest -Force | Out-Null }
        else {
            $d = Split-Path $dest -Parent
            if (-not (Test-Path $d)) { New-Item -ItemType Directory -Path $d -Force | Out-Null }
            Copy-Item $_.FullName -Destination $dest -Force
        }
    }
}

# Upload Assets (Long Cache - 1 Year)
Write-Host "Uploading assets (images, css, js)..."
az storage blob upload-batch --account-name $StorageAccount --destination $Container --source $tempDir --pattern "*" --content-cache-control "public, max-age=31536000" --overwrite

# Upload HTML (Short Cache - 1 Hour)
Write-Host "Uploading HTML files..."
az storage blob upload-batch --account-name $StorageAccount --destination $Container --source $tempDir --pattern "*.html" --content-cache-control "public, max-age=3600" --overwrite

# Upload PDFs (Correct Content-Type)
Write-Host "Uploading PDF files with correct headers..."
az storage blob upload-batch --account-name $StorageAccount --destination $Container --source $tempDir --pattern "*.pdf" --content-type "application/pdf" --content-cache-control "public, max-age=31536000" --overwrite

if ($LASTEXITCODE -eq 0) { 
    Write-Host "Success!" -ForegroundColor Green 
    Write-Host "URL: https://$StorageAccount.z29.web.core.windows.net/"
}
else { 
    Write-Host "Failed!" -ForegroundColor Red 
}

Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue
