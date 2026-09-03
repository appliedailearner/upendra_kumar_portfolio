$analyticsSnippet = "<!-- Cloudflare Web Analytics --><script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{`"token`": `"0b89fb05ee3844079b659405bc3f5428`"}'></script><!-- End Cloudflare Web Analytics -->"

# Get all HTML files, excluding backups and venv
$files = Get-ChildItem -Path "c:\MyResumePortfolio" -Recurse -Filter *.html | 
Where-Object { $_.FullName -notmatch "\\.venv\\" -and $_.FullName -notmatch "\\site_backups\\" -and $_.FullName -notmatch "\\node_modules\\" }

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    
    # Check if already exists
    if ($content -match "0b89fb05ee3844079b659405bc3f5428") {
        Write-Host "Skipping $($file.Name) - Already has analytics."
        continue
    }

    # Inject before </body>
    if ($content -match "</body>") {
        $newContent = $content -replace "</body>", "$analyticsSnippet`n</body>"
        Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8
        Write-Host "Updated $($file.Name)"
    }
    else {
        Write-Warning "Could not find </body> in $($file.Name)"
    }
}
