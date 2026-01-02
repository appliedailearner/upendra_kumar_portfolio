$status = git status --porcelain
if ($status) {
    Write-Host "Changes detected. Deploying..."
    git add .
    git commit -m "Final deployment check"
    git push origin main
}
else {
    Write-Host "No changes detected locally. Pushing to ensure remote is up to date..."
    git push origin main
}
