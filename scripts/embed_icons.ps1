
$iconPaths = @{
    "icon-afw-uae"     = "C:/MyResumePortfolio/blog/assets/Azure_Public_Service_Icons/Icons/networking/10084-icon-service-Firewalls.svg"
    "icon-bastion-uae" = "C:/MyResumePortfolio/blog/assets/Azure_Public_Service_Icons/Icons/networking/02422-icon-service-Bastions.svg"
    "icon-vpn-uae"     = "C:/MyResumePortfolio/blog/assets/Azure_Public_Service_Icons/Icons/networking/10063-icon-service-Virtual-Network-Gateways.svg"
    "icon-dns-uae"     = "C:/MyResumePortfolio/blog/assets/Azure_Public_Service_Icons/Icons/networking/02882-icon-service-DNS-Private-Resolver.svg"
    "icon-afw-ukc"     = "C:/MyResumePortfolio/blog/assets/Azure_Public_Service_Icons/Icons/networking/10084-icon-service-Firewalls.svg"
    "icon-sentinel"    = "C:/MyResumePortfolio/blog/assets/Azure_Public_Service_Icons/Icons/security/10248-icon-service-Azure-Sentinel.svg"
    "icon-defender"    = "C:/MyResumePortfolio/blog/assets/Azure_Public_Service_Icons/Icons/security/10241-icon-service-Microsoft-Defender-for-Cloud.svg"
    "icon-policy"      = "C:/MyResumePortfolio/blog/assets/Azure_Public_Service_Icons/Icons/management + governance/10316-icon-service-Policy.svg"
    "icon-agw-uae"     = "C:/MyResumePortfolio/blog/assets/Azure_Public_Service_Icons/Icons/networking/10076-icon-service-Application-Gateways.svg"
    "icon-apim-uae"    = "C:/MyResumePortfolio/blog/assets/Azure_Public_Service_Icons/Icons/ai + machine learning/03173-icon-service-Cognitive-Services-Decisions.svg"
    "icon-app-uae"     = "C:/MyResumePortfolio/blog/assets/Azure_Public_Service_Icons/Icons/app services/10035-icon-service-App-Services.svg"
    "icon-oai-uae"     = "C:/MyResumePortfolio/blog/assets/Azure_Public_Service_Icons/Icons/ai + machine learning/03438-icon-service-Azure-OpenAI.svg"
    "icon-srch-uae"    = "C:/MyResumePortfolio/blog/assets/Azure_Public_Service_Icons/Icons/ai + machine learning/03321-icon-service-Serverless-Search.svg"
    "icon-di-uae"      = "C:/MyResumePortfolio/blog/assets/Azure_Public_Service_Icons/Icons/ai + machine learning/00819-icon-service-Form-Recognizers.svg"
    "icon-st-uae"      = "C:/MyResumePortfolio/blog/assets/Azure_Public_Service_Icons/Icons/storage/10086-icon-service-Storage-Accounts.svg"
    "icon-agw-ukc"     = "C:/MyResumePortfolio/blog/assets/Azure_Public_Service_Icons/Icons/networking/10076-icon-service-Application-Gateways.svg"
    "icon-app-ukc"     = "C:/MyResumePortfolio/blog/assets/Azure_Public_Service_Icons/Icons/app services/10035-icon-service-App-Services.svg"
    "icon-tm-global"   = "C:/MyResumePortfolio/blog/assets/Azure_Public_Service_Icons/Icons/networking/10065-icon-service-Traffic-Manager-Profiles.svg"
}

$xmlFile = "C:/MyResumePortfolio/docs/Azure_AI_Platform_Architecture.drawio"
$xmlContent = Get-Content $xmlFile -Raw

foreach ($id in $iconPaths.Keys) {
    $path = $iconPaths[$id]
    if (Test-Path $path) {
        $bytes = [System.IO.File]::ReadAllBytes($path)
        $base64 = [Convert]::ToBase64String($bytes)
        $dataUri = "data:image/svg+xml;base64,$base64"
        
        # Pattern to find the correct cell and then the image parameter within the style string
        # Looks for: id="ID" followed by anything until image= then grabs the path until ; or "
        $pattern = "(id=`"$id`".*?image=)([^;`"]*)"
        $xmlContent = [regex]::Replace($xmlContent, $pattern, "`${1}$dataUri", [System.Text.RegularExpressions.RegexOptions]::Singleline)
    }
    else {
        Write-Host "Warning: Icon not found at $path"
    }
}

$xmlContent | Set-Content $xmlFile -NoNewline
Write-Host "Diagram successfully upgraded with embedded A++ icons."
