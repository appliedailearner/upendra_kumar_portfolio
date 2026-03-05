# Deploy to Both GitHub Pages and Azure Storage
param(
    [string]$CommitMessage = "Mobile UX Remediation: Fixed transparency and z-index collisions",
    [switch]$Force
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Dual Deployment Script (v3)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Step 1: Deploy to GitHub Pages
Write-Host "STEP 1: GitHub Push" -ForegroundColor Yellow
git add .
$status = git status --porcelain
if ($status) {
    git commit -m "$CommitMessage"
}
git push origin main

# Step 2: Deploy to Azure Storage
Write-Host ""
Write-Host "STEP 2: Azure Push" -ForegroundColor Yellow
if ($Force) {
    powershell.exe -ExecutionPolicy Bypass -File .\deploy-azure.ps1 -Force
}
else {
    powershell.exe -ExecutionPolicy Bypass -File .\deploy-azure.ps1
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deployment Completed Successfully" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
