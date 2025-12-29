# Azure Storage Deployment Script
# This script uploads your website to Azure Storage Account

param(
    [string]$StorageAccount = "porfolioupendrakumar",
    [string]$Container = "`$web"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Azure Storage Deployment Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Azure CLI is installed
Write-Host "Checking Azure CLI installation..." -ForegroundColor Yellow
try {
    $azVersion = az version --output json | ConvertFrom-Json
    Write-Host "✓ Azure CLI installed: $($azVersion.'azure-cli')" -ForegroundColor Green
} catch {
    Write-Host "✗ Azure CLI not found!" -ForegroundColor Red
    Write-Host "Please install Azure CLI from: https://aka.ms/installazurecliwindows" -ForegroundColor Yellow
    exit 1
}

# Check if logged in
Write-Host "Checking Azure login status..." -ForegroundColor Yellow
try {
    $account = az account show --output json 2>$null | ConvertFrom-Json
    if ($null -eq $account) {
        throw "Not logged in"
    }
    Write-Host "✓ Logged in as: $($account.user.name)" -ForegroundColor Green
    Write-Host "  Subscription: $($account.name)" -ForegroundColor Gray
} catch {
    Write-Host "✗ Not logged in to Azure!" -ForegroundColor Red
    Write-Host "Running 'az login'..." -ForegroundColor Yellow
    az login
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Login failed!" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "Deployment Configuration:" -ForegroundColor Cyan
Write-Host "  Storage Account: $StorageAccount" -ForegroundColor White
Write-Host "  Container: $Container" -ForegroundColor White
Write-Host "  Source Directory: $(Get-Location)" -ForegroundColor White
Write-Host ""

# Confirm deployment
$confirm = Read-Host "Proceed with deployment? (Y/N)"
if ($confirm -ne 'Y' -and $confirm -ne 'y') {
    Write-Host "Deployment cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Starting deployment..." -ForegroundColor Yellow

# Get the current directory
$sourceDir = Get-Location

# Files and directories to exclude
$excludePatterns = @(
    '.git',
    '.github',
    '.venv',
    '.claude',
    'node_modules',
    'site_backups',
    '*.md',
    '*.py',
    '*.ps1',
    '*.zip',
    'appliedailearner.github.io',
    'azure-landing-zones-project',
    'azure-projects',
    'portfolio-deploy',
    'portfolio-template',
    'master prompts'
)

# Create a temporary directory for deployment
$tempDir = Join-Path $env:TEMP "portfolio-deploy-$(Get-Date -Format 'yyyyMMddHHmmss')"
New-Item -ItemType Directory -Path $tempDir -Force | Out-Null

Write-Host "Preparing files for deployment..." -ForegroundColor Yellow

# Copy files to temp directory, excluding unwanted items
Get-ChildItem -Path $sourceDir -Recurse | ForEach-Object {
    $relativePath = $_.FullName.Substring($sourceDir.Path.Length + 1)
    
    # Check if path should be excluded
    $shouldExclude = $false
    foreach ($pattern in $excludePatterns) {
        if ($relativePath -like "*$pattern*") {
            $shouldExclude = $true
            break
        }
    }
    
    if (-not $shouldExclude) {
        $destPath = Join-Path $tempDir $relativePath
        if ($_.PSIsContainer) {
            New-Item -ItemType Directory -Path $destPath -Force | Out-Null
        } else {
            $destDir = Split-Path $destPath -Parent
            if (-not (Test-Path $destDir)) {
                New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            }
            Copy-Item $_.FullName -Destination $destPath -Force
        }
    }
}

Write-Host "✓ Files prepared in temporary directory" -ForegroundColor Green

# Upload to Azure Storage
Write-Host ""
Write-Host "Uploading to Azure Storage..." -ForegroundColor Yellow

try {
    # Delete existing files in the container (optional - comment out to keep old files)
    # az storage blob delete-batch --account-name $StorageAccount --source $Container --pattern "*"
    
    # Upload all files
    az storage blob upload-batch `
        --account-name $StorageAccount `
        --destination $Container `
        --source $tempDir `
        --overwrite `
        --output table
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✓ Deployment successful!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Your website is now available at:" -ForegroundColor Cyan
        Write-Host "  https://$StorageAccount.z29.web.core.windows.net/" -ForegroundColor White
    } else {
        throw "Upload failed"
    }
} catch {
    Write-Host "✗ Deployment failed!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
} finally {
    # Clean up temp directory
    Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deployment Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
