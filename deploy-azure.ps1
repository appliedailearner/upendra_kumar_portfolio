# Targeted Azure Deployment
param(
    [string]$StorageAccount = "porfolioupendrakumar",
    [string]$Container = "`$web",
    [switch]$Force,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

Write-Host "Deploying to $StorageAccount..." -ForegroundColor Cyan

$sourceDir = (Get-Location).Path
$tempDir = Join-Path $env:TEMP "portfolio-deploy-$(Get-Date -Format 'yyyyMMddHHmmss')"
New-Item -ItemType Directory -Path $tempDir -Force | Out-Null

$rootFiles = @(
    ".nojekyll",
    "CNAME",
    "404.html",
    "index.html",
    "blog.html",
    "blog_445826f.html",
    "resume.html",
    "resume_backup.html",
    "Upendra_Kumar_CV.html",
    "robots.txt",
    "sitemap.xml",
    "feed.xml",
    "status.json"
)

$contentDirs = @(
    "assets",
    "blog",
    "css",
    "docs",
    "images",
    "js",
    "pages",
    "presentations",
    "Azure HA DR",
    "azurewebapp"
)

$allowedExtensions = @(
    ".html", ".css", ".js", ".mjs", ".json", ".xml",
    ".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".ico",
    ".woff", ".woff2", ".ttf", ".eot",
    ".pdf", ".zip", ".mp4", ".webm",
    ".csv", ".xlsx", ".pptx", ".docx"
)

$excludedPathFragments = @(
    "\.claude\",
    "\.copilot\",
    "\.github\",
    "\.git\",
    "\.vscode\",
    "\node_modules\",
    "\docx_content\",
    "\github-copilot-agent-skills\"
)

function Copy-ItemPreservingRelativePath {
    param(
        [Parameter(Mandatory = $true)][string]$FullPath
    )

    $relativePath = [System.IO.Path]::GetRelativePath($sourceDir, $FullPath)
    $destinationPath = Join-Path $tempDir $relativePath
    $destinationParent = Split-Path $destinationPath -Parent

    if (-not (Test-Path $destinationParent)) {
        New-Item -ItemType Directory -Path $destinationParent -Force | Out-Null
    }

    Copy-Item -LiteralPath $FullPath -Destination $destinationPath -Force
}

foreach ($file in $rootFiles) {
    $fullPath = Join-Path $sourceDir $file
    if (Test-Path $fullPath -PathType Leaf) {
        Copy-ItemPreservingRelativePath -FullPath $fullPath
    }
}

foreach ($dir in $contentDirs) {
    $fullDir = Join-Path $sourceDir $dir
    if (-not (Test-Path $fullDir -PathType Container)) {
        continue
    }

    Get-ChildItem -LiteralPath $fullDir -Recurse -File -ErrorAction SilentlyContinue | ForEach-Object {
        $relativePath = [System.IO.Path]::GetRelativePath($sourceDir, $_.FullName)
        $normalizedRelativePath = "\" + ($relativePath -replace "/", "\") + "\"
        $extension = $_.Extension.ToLowerInvariant()

        if ($allowedExtensions -notcontains $extension) {
            return
        }

        foreach ($fragment in $excludedPathFragments) {
            if ($normalizedRelativePath -like "*$fragment*") {
                return
            }
        }

        Copy-ItemPreservingRelativePath -FullPath $_.FullName
    }
}

$copiedFiles = Get-ChildItem -LiteralPath $tempDir -Recurse -File | Sort-Object FullName

Write-Host ("Prepared {0} files for deployment." -f $copiedFiles.Count) -ForegroundColor DarkCyan

if ($DryRun) {
    $copiedFiles |
        Select-Object @{Name = "RelativePath"; Expression = { [System.IO.Path]::GetRelativePath($tempDir, $_.FullName) }} |
        Format-Table -AutoSize

    Remove-Item -LiteralPath $tempDir -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "Dry run complete. No files were uploaded." -ForegroundColor Yellow
    exit 0
}

Write-Host "Uploading assets (images, css, js, downloads)..." -ForegroundColor Cyan
az storage blob upload-batch `
    --account-name $StorageAccount `
    --destination $Container `
    --source $tempDir `
    --pattern "*" `
    --content-cache-control "public, max-age=31536000" `
    --overwrite

Write-Host "Uploading HTML files..." -ForegroundColor Cyan
az storage blob upload-batch `
    --account-name $StorageAccount `
    --destination $Container `
    --source $tempDir `
    --pattern "*.html" `
    --content-cache-control "public, max-age=3600" `
    --overwrite

Write-Host "Uploading PDF files with correct headers..." -ForegroundColor Cyan
az storage blob upload-batch `
    --account-name $StorageAccount `
    --destination $Container `
    --source $tempDir `
    --pattern "*.pdf" `
    --content-type "application/pdf" `
    --content-cache-control "public, max-age=31536000" `
    --overwrite

if ($LASTEXITCODE -eq 0) {
    Write-Host "Success!" -ForegroundColor Green
    Write-Host "URL: https://$StorageAccount.z29.web.core.windows.net/"
}
else {
    Write-Host "Failed!" -ForegroundColor Red
    exit $LASTEXITCODE
}

Remove-Item -LiteralPath $tempDir -Recurse -Force -ErrorAction SilentlyContinue
