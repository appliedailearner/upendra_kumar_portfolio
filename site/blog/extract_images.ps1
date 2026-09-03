
Add-Type -AssemblyName System.IO.Compression.FileSystem
$docxPath = "C:\MyResumePortfolio\blog\UKLifeLabs_GPT41_UK_South_Complete_Blog_and_Appendices.docx"
$destDir = "C:\MyResumePortfolio\blog\temp_images"

# Clean/Create destination
if (Test-Path $destDir) { Remove-Item $destDir -Recurse -Force }
New-Item -ItemType Directory -Path $destDir | Out-Null

try {
    $zip = [System.IO.Compression.ZipFile]::OpenRead($docxPath)
    
    # Filter for media files
    $mediaEntries = $zip.Entries | Where-Object { $_.FullName -like "word/media/*" }
    
    foreach ($entry in $mediaEntries) {
        $fileName = $entry.Name
        $targetPath = Join-Path $destDir $fileName
        [System.IO.Compression.ZipFileExtensions]::ExtractToFile($entry, $targetPath, $true)
        Write-Host "Extracted: $fileName"
    }
    
    $zip.Dispose()
    Write-Host "Extraction complete. Images are in $destDir"
    
    # List extracted files for verification
    Get-ChildItem $destDir
} catch {
    Write-Error "Error extracting images: $_"
    exit 1
}
