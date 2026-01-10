# Microsoft Architecture Diagrams (PNG + Visio)

This bundle contains **official Microsoft Architecture Center / Microsoft Learn** diagrams in:
- **Visio (.vsdx)** (directly downloaded from `arch-center.azureedge.net`)
- **High-resolution PNG** (exported from the Visio files)

## Where files are
- `vsdx/` -> original Visio files
- `png_hi/` -> exported PNGs (some diagrams have multiple pages: `*-0.png`, `*-1.png`, ...)

## Diagram index (with official sources)

### 1) Protect APIs with Application Gateway + API Management
- Source page: https://learn.microsoft.com/en-us/azure/architecture/web-apps/api-management/api-management-application-gateway
- Visio: `vsdx/protect-apis.vsdx`
- PNG: `png_hi/protect-apis-*.png`

### 2) Internal APIM behind Application Gateway (Function backend example)
- Source page: https://learn.microsoft.com/en-us/azure/architecture/example-scenario/integration/app-gateway-internal-api-management-function
- Visio: `vsdx/app-gateway-internal-api-management-function.vsdx`
- PNG: `png_hi/app-gateway-internal-api-management-function-*.png`

### 3) Integrate API Management with a legacy API in on-premises
- Source page: https://learn.microsoft.com/en-us/azure/architecture/example-scenario/apps/apim-api-scenario
- Visio: `vsdx/architecture-apim-api-scenario.vsdx`
- PNG: `png_hi/architecture-apim-api-scenario.png`

### 4) Basic Microsoft Foundry chat reference architecture (POC)
- Source page: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/architecture/basic-microsoft-foundry-chat
- Visio: `vsdx/openai-end-to-end-basic.vsdx`
- PNG: `png_hi/openai-end-to-end-basic-*.png`

### 5) Baseline Microsoft Foundry chat reference architecture (production)
- Source page: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-chat
- Visio: `vsdx/baseline-microsoft-foundry.vsdx`
- PNG: `png_hi/baseline-microsoft-foundry-*.png`

### 6) Baseline Microsoft Foundry chat in an Azure landing zone
- Source page: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-landing-zone
- Visio: `vsdx/baseline-microsoft-foundry-landing-zone.vsdx`
- PNG: `png_hi/baseline-microsoft-foundry-landing-zone-*.png`

### 7) Landing zone networking view (from the same Foundry landing zone guidance)
- Source page: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-landing-zone
- Visio: `vsdx/baseline-landing-zone-networking.vsdx`
- PNG: `png_hi/baseline-landing-zone-networking-*.png`

### 8) Landing zone egress routing view (from the same Foundry landing zone guidance)
- Source page: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-landing-zone
- Visio: `vsdx/baseline-landing-zone-networking-egress.vsdx`
- PNG: `png_hi/baseline-landing-zone-networking-egress-*.png`

### 9) Gateway custom authentication pattern for Azure OpenAI in Foundry Models
- Source page: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/azure-openai-gateway-custom-authentication
- Visio: `vsdx/azure-openai-authentication.vsdx`
- PNG: `png_hi/azure-openai-authentication-*.png`

## Notes
- PNGs were produced by exporting VSDX -> PDF -> PNG in a headless Linux environment. Layout stays faithful to the Visio.
- If you need **a single PNG per diagram**, use the `*-0.png` page in `png_hi/` (most diagrams are page 0).
