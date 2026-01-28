
Add-Type -AssemblyName System.IO.Compression.FileSystem
$docxPath = "C:\MyResumePortfolio\blog\UKLifeLabs_GPT41_UK_South_Complete_Blog_and_Appendices.docx"
$outputPath = "C:\MyResumePortfolio\blog\temp_extracted_gpt.txt"

try {
    $zip = [System.IO.Compression.ZipFile]::OpenRead($docxPath)
    $entry = $zip.GetEntry("word/document.xml")
    if ($null -eq $entry) {
        Write-Error "Could not find word/document.xml in the DOCX."
        exit 1
    }
    $stream = $entry.Open()
    $reader = New-Object System.IO.StreamReader($stream)
    $xmlContent = $reader.ReadToEnd()
    $reader.Close()
    $stream.Close()
    $zip.Dispose()

    # Simple XML tag removal
    $textContent = $xmlContent -replace '<[^>]+>', ' '
    # Clean up multiple spaces
    $textContent = $textContent -replace '\s+', ' '
    
    $textContent | Out-File -FilePath $outputPath -Encoding utf8
    Write-Host "Extraction successful. Saved to $outputPath"
} catch {
    Write-Error "An error occurred: $_"
    exit 1
}
