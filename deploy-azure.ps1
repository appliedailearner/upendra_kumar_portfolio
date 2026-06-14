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

$publishRules = @(
    @{
        Path = "assets"
        Recurse = $true
        Extensions = @(".css", ".js", ".json", ".xml", ".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".ico", ".pdf", ".zip", ".mp4", ".webm", ".csv", ".xlsx", ".pptx")
    },
    @{
        Path = "blog"
        Recurse = $false
        Extensions = @(".html")
    },
    @{
        Path = "blog\assets"
        Recurse = $true
        Extensions = @(".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".pdf", ".pptx", ".zip")
    },
    @{
        Path = "css"
        Recurse = $true
        Extensions = @(".css", ".woff", ".woff2", ".ttf", ".eot")
    },
    @{
        Path = "docs"
        Recurse = $true
        Extensions = @(".html", ".pdf", ".pptx")
    },
    @{
        Path = "images"
        Recurse = $true
        Extensions = @(".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".ico", ".mp4", ".webm")
    },
    @{
        Path = "js"
        Recurse = $true
        Extensions = @(".js", ".mjs", ".json")
    },
    @{
        Path = "pages"
        Recurse = $true
        Extensions = @(".html")
    },
    @{
        Path = "presentations"
        Recurse = $true
        Extensions = @(".html")
    },
    @{
        Path = "Azure HA DR"
        Recurse = $true
        Extensions = @(".html", ".png", ".jpg", ".jpeg", ".webp", ".svg", ".json", ".js", ".csv")
    },
    @{
        Path = "azurewebapp"
        Recurse = $true
        Extensions = @(".html", ".png", ".jpg", ".jpeg", ".webp", ".svg", ".mp4")
    }
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

    $relativePath = $FullPath.Substring($sourceDir.Length).TrimStart([System.IO.Path]::DirectorySeparatorChar)
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

foreach ($rule in $publishRules) {
    $fullDir = Join-Path $sourceDir $rule.Path
    if (-not (Test-Path $fullDir -PathType Container)) {
        continue
    }

    $childItems = if ($rule.Recurse) {
        Get-ChildItem -LiteralPath $fullDir -Recurse -File -ErrorAction SilentlyContinue
    }
    else {
        Get-ChildItem -LiteralPath $fullDir -File -ErrorAction SilentlyContinue
    }

    $childItems | ForEach-Object {
        $relativePath = $_.FullName.Substring($sourceDir.Length).TrimStart([System.IO.Path]::DirectorySeparatorChar)
        $normalizedRelativePath = "\" + ($relativePath -replace "/", "\") + "\"
        $extension = $_.Extension.ToLowerInvariant()

        if ($rule.Extensions -notcontains $extension) {
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
