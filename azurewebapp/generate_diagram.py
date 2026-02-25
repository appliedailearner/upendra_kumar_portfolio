import json, zlib, base64
from urllib.parse import quote

diagram_type = "mermaid"
diagram_code = """graph TD
    classDef azure fill:#0072C6,stroke:#fff,stroke-width:2px,color:#fff,rx:5,ry:5;
    classDef vnet fill:#E3F2FD,stroke:#90CAF9,stroke-width:2px,stroke-dasharray: 5 5;
    classDef user fill:#333,stroke:#fff,stroke-width:2px,color:#fff,rx:20,ry:20;

    Client([Users / Internet Clients]):::user

    subgraph VNET [Virtual Network: vnet-ictsi-sea-01]
        APIM[Azure API Management<br/>(External/Internal VNet Mode)]:::azure
        PE[Azure Private Endpoint<br/>IP: 10.50.10.x]:::azure
    end

    subgraph PAAS [Azure PaaS Services]
        AppServer[Azure App Service Web App<br/>Public Access: Disabled]:::azure
    end

    DNS[Private DNS Zone<br/>privatelink.azurewebsites.net]:::azure

    Client -->|HTTPS Request| APIM
    APIM -->|Routes to Private IP| PE
    PE -->|Private Link| AppServer

    APIM -.->|Resolves Backend Name| DNS
    DNS -.->|Returns 10.50.10.x| APIM

    class VNET vnet;
"""

encoded = quote(diagram_code, safe='')
c = zlib.compressobj(9, zlib.DEFLATED, -15)
raw_deflate = c.compress(encoded.encode('utf-8')) + c.flush()
data = base64.b64encode(raw_deflate).decode()

payload = json.dumps({"type": diagram_type, "compressed": True, "data": data})
url = f"https://app.diagrams.net/?pv=0&grid=0#create={quote(payload, safe='')}"

html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Azure Architecture Diagram</title>
<style>
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    margin: 0;
    background: #f8f9fa;
  }}
  .card {{
    text-align: center;
    background: white;
    border-radius: 12px;
    padding: 40px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  }}
  .card h2 {{
    margin: 0 0 8px;
    color: #1a1a1a;
  }}
  .card p {{
    margin: 0 0 24px;
    color: #666;
  }}
  .btn {{
    display: inline-block;
    padding: 14px 32px;
    background: #4285f4;
    color: white;
    text-decoration: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 500;
    transition: background 0.2s;
  }}
  .btn:hover {{
    background: #3367d6;
  }}
</style>
</head>
<body>
  <div class="card">
    <h2>Architecture Diagram Ready</h2>
    <p>Click below to open the App Service Private-Only architecture diagram in draw.io</p>
    <a class="btn" href="{url}" target="_blank" rel="noopener noreferrer">
      Open Diagram in draw.io
    </a>
  </div>
</body>
</html>"""

with open("C:\\MyResumePortfolio\\azurewebapp\\architecture_diagram.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("HTML artifact created at C:\\MyResumePortfolio\\azurewebapp\\architecture_diagram.html")
