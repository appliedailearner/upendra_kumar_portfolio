$ErrorActionPreference = "Stop"

Write-Host "Azure Agentic AI repo validation" -ForegroundColor Cyan

$moduleRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$requiredFiles = @(
    "README.md",
    "requirements.txt",
    ".env.example",
    "DEPLOYMENT-GUIDE.md",
    "app\agent.py",
    "app\tests\test_agent.py",
    "infra\main.bicep"
)

foreach ($file in $requiredFiles) {
    $fullPath = Join-Path $moduleRoot $file
    if (-not (Test-Path $fullPath)) {
        throw "Missing required file: $file"
    }
}

Write-Host "Required files found." -ForegroundColor Green

$pythonPath = Join-Path $moduleRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $pythonPath)) {
    $pythonPath = "python"
}

Push-Location $moduleRoot
try {
    $env:PYTHONPATH = $moduleRoot
    & $pythonPath -m pytest .\app\tests -q
    if ($LASTEXITCODE -ne 0) {
        throw "Pytest validation failed."
    }
}
finally {
    Pop-Location
}

Write-Host ""
Write-Host "Support boundary:" -ForegroundColor Yellow
Write-Host "- Module 09 is the current runnable baseline."
Write-Host "- The broader repo is still being standardized."
Write-Host "- Treat Azure deployment as a baseline for iteration, not a finished enterprise landing zone."
