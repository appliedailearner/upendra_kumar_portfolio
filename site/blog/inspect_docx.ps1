
Add-Type -AssemblyName System.IO.Compression.FileSystem
$docxPath = "C:\MyResumePortfolio\blog\UKLifeLabs_GPT41_UK_South_Complete_Blog_and_Appendices.docx"

try {
    $zip = [System.IO.Compression.ZipFile]::OpenRead($docxPath)
    $zip.Entries | Select-Object -ExpandProperty FullName
    $zip.Dispose()
}
catch {
    Write-Error "Error reading zip: $_"
}
