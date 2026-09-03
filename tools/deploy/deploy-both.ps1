# Deploy to Both GitHub Pages and Azure Storage
param(
    [string]$CommitMessage = "Principal Overhaul: Implemented Architect's Split UI, Cinematic Animations, and L67 Refinement",
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Dual Deployment Script (v4)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Step 1: Deploy to GitHub Pages (Actions publishes <repo>/site)
Write-Host "STEP 1: GitHub Push" -ForegroundColor Yellow
Push-Location $repoRoot
try {
    git add .
    $status = git status --porcelain
    if ($status) {
        git commit -m "$CommitMessage"
    }
    git push origin main
}
finally {
    Pop-Location
}

# Step 2: Deploy to Azure Storage ($web static site)
Write-Host ""
Write-Host "STEP 2: Azure Push" -ForegroundColor Yellow
if ($Force) {
    powershell.exe -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "deploy-azure.ps1") -Force
}
else {
    powershell.exe -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "deploy-azure.ps1")
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deployment Completed Successfully" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
