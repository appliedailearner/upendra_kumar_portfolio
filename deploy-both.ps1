# Deploy to Both GitHub Pages and Azure Storage
# This script deploys your website to both platforms

param(
    [string]$CommitMessage = "Update portfolio website"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Dual Deployment Script" -ForegroundColor Cyan
Write-Host "GitHub Pages + Azure Storage" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Deploy to GitHub Pages
Write-Host "STEP 1: Deploying to GitHub Pages" -ForegroundColor Yellow
Write-Host "-----------------------------------" -ForegroundColor Gray

# Check for changes
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "Changes detected. Committing..." -ForegroundColor Yellow
    
    git add .
    git commit -m $CommitMessage
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Changes committed" -ForegroundColor Green
    } else {
        Write-Host "✗ Commit failed!" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "No changes to commit" -ForegroundColor Gray
}

Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Pushed to GitHub successfully" -ForegroundColor Green
    Write-Host "  GitHub Actions will deploy to: https://portfolio.upendrakumar.com" -ForegroundColor Gray
} else {
    Write-Host "✗ Push failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 2: Deploy to Azure Storage
Write-Host "STEP 2: Deploying to Azure Storage" -ForegroundColor Yellow
Write-Host "-----------------------------------" -ForegroundColor Gray

& "$PSScriptRoot\deploy-azure.ps1"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "All Deployments Complete!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Your website is now available at:" -ForegroundColor White
    Write-Host "  1. https://portfolio.upendrakumar.com (GitHub Pages)" -ForegroundColor Cyan
    Write-Host "  2. https://portfolioupendrakumar.z29.web.core.windows.net (Azure Storage)" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host "✗ Azure deployment failed!" -ForegroundColor Red
    exit 1
}
