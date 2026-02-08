# Azure Storage Deployment Script (Simplified)
# This script uploads your website to Azure Storage Account

param(
    [string]$StorageAccount = "porfolioupendrakumar",
    [string]$Container = "`$web",
    [switch]$Force
)

$ErrorActionPreference = "Stop"

Write-Host "Starting Simplified Deployment..." -ForegroundColor Green

# 1. Prepare files
$sourceDir = Get-Location
$tempDir = Join-Path $env:TEMP "portfolio-deploy-$(Get-Date -Format 'yyyyMMddHHmmss')"
New-Item -ItemType Directory -Path $tempDir -Force | Out-Null

$excludePatterns = @(
    '.git', '.github', '.venv', '.claude', 'node_modules', 'site_backups',
    '*.md', '*.py', '*.ps1',
    'appliedailearner.github.io', 'azure-landing-zones-project', 'azure-projects',
    'portfolio-deploy', 'portfolio-template', 'master prompts'
)

Write-Host "Copying files..."
Get-ChildItem -Path $sourceDir -Recurse | ForEach-Object {
    $relativePath = $_.FullName.Substring($sourceDir.Path.Length + 1)
    $shouldExclude = $false
    foreach ($pattern in $excludePatterns) {
        if ($relativePath -like "*$pattern*") { $shouldExclude = $true; break }
    }
    
    if (-not $shouldExclude) {
        $destPath = Join-Path $tempDir $relativePath
        if ($_.PSIsContainer) {
            New-Item -ItemType Directory -Path $destPath -Force | Out-Null
        }
        else {
            $destDir = Split-Path $destPath -Parent
            if (-not (Test-Path $destDir)) { New-Item -ItemType Directory -Path $destDir -Force | Out-Null }
            Copy-Item $_.FullName -Destination $destPath -Force
        }
    }
}

# 2. Upload
Write-Host "Uploading to Azure..."
$uploadArgs = @(
    "storage", "blob", "upload-batch",
    "--account-name", $StorageAccount,
    "--destination", $Container,
    "--source", $tempDir,
    "--overwrite"
)
az $uploadArgs

Write-Host "Done."
Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue
