import requests
import base64
import zlib
import os

def generate_kroki_mermaid(mermaid_text, filename):
    compressed = zlib.compress(mermaid_text.encode('utf-8'), 9)
    encoded = base64.urlsafe_b64encode(compressed).decode('utf-8')
    url = f"https://kroki.io/mermaid/svg/{encoded}"
    
    response = requests.get(url)
    if response.status_code == 200:
        filepath = os.path.join(r"C:\MyResumePortfolio\images", filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"Successfully generated {filename}")
    else:
        print(f"Failed to generate {filename}: {response.text}")

diagram_1 = """
graph LR
    classDef default fill:#0f172a,stroke:#38bdf8,stroke-width:2px,color:#f8fafc,rx:8px,ry:8px
    classDef onprem fill:#1e1e1e,stroke:#a855f7,stroke-width:2px,color:#f8fafc,rx:8px,ry:8px
    classDef azure fill:#0078D4,stroke:#38bdf8,stroke-width:2px,color:#ffffff,rx:8px,ry:8px
    classDef endpoint fill:#10b981,stroke:#059669,stroke-width:2px,color:#ffffff,rx:8px,ry:8px

    subgraph OnPrem[On-Premises Network]
        App[fa:fa-server On-Prem App]:::onprem
        DNS[fa:fa-sitemap On-Prem DNS Server]:::onprem
    end

    subgraph AzureCloud[Azure Private Network]
        subgraph VNet[Hub Virtual Network]
            Resolver[fa:fa-cloud Azure DNS Private Resolver]:::azure
            PrivZone[fa:fa-globe Private DNS Zone]:::azure
        end
        PE[fa:fa-network-wired Private Endpoint IP]:::endpoint
        Service[fa:fa-database Azure AI Service]:::azure
    end

    App -->|1. Resolves| DNS
    DNS -->|2. Forwards| Resolver
    Resolver -->|3. Queries| PrivZone
    PrivZone -.->|4. Returns IP| Resolver
    Resolver -.-> DNS
    DNS -.->|5. 10.1.1.5| App

    App ==>|6. Traffic Routes| PE
    PE ==>|7. Private Link| Service
"""

generate_kroki_mermaid(diagram_1, "diagram_hybrid_dns_msft.svg")
