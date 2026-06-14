
import os
import base64
import re
import xml.etree.ElementTree as ET

# Configuration
icon_root = r"C:\MyResumePortfolio\blog\assets\Azure_Public_Service_Icons\Icons"
output_path = r"C:\MyResumePortfolio\docs\Azure_Enterprise_AI_Architecture.drawio"

# 100% Precise Mapping
icon_map = {
    "icon-users": "10230-icon-service-Users.svg",
    "icon-tm": "10065-icon-service-Traffic-Manager-Profiles.svg",
    "icon-agw": "10076-icon-service-Application-Gateways.svg",
    "icon-apim": "10042-icon-service-API-Management-Services.svg",
    "icon-app": "10035-icon-service-App-Services.svg",
    "icon-oai": "03438-icon-service-Azure-OpenAI.svg",
    "icon-srch": "10044-icon-service-Cognitive-Search.svg",
    "icon-di": "00819-icon-service-Form-Recognizers.svg",
    "icon-st": "10086-icon-service-Storage-Accounts.svg",
    "icon-kv": "10245-icon-service-Key-Vaults.svg",
    "icon-monitor": "00001-icon-service-Monitor.svg",
    "icon-log": "00009-icon-service-Log-Analytics-Workspaces.svg",
    "icon-insights": "00012-icon-service-Application-Insights.svg",
    "icon-dns-zone": "10064-icon-service-DNS-Zones.svg",
    "icon-afw": "10084-icon-service-Firewalls.svg",
    "icon-bastion": "02422-icon-service-Bastions.svg",
    "icon-vpn": "10063-icon-service-Virtual-Network-Gateways.svg",
    "icon-dns-res": "02882-icon-service-DNS-Private-Resolver.svg",
    "icon-policy": "10316-icon-service-Policy.svg",
    "icon-defender": "10241-icon-service-Microsoft-Defender-for-Cloud.svg",
    "icon-cost": "00004-icon-service-Cost-Management-and-Billing.svg",
    "icon-pe": "02579-icon-service-Private-Endpoints.svg"
}

def find_icon_path(filename):
    for root, dirs, files in os.walk(icon_root):
        if filename in files:
            return os.path.join(root, filename)
    return None

def get_base64_svg(file_path, icon_id):
    with open(file_path, "rb") as svg_file:
        content = svg_file.read().decode('utf-8')
        # Rename IDs to prevent clashing (e.g., id="abc" -> id="icon123_abc")
        # Find all id="xyz"
        ids = re.findall(r'id="([^"]+)"', content)
        for old_id in ids:
            new_id = f"{icon_id}_{old_id}"
            content = content.replace(f'id="{old_id}"', f'id="{new_id}"')
            content = content.replace(f'url(#{old_id})', f'url(#{new_id})')
            content = content.replace(f'href="#{old_id}"', f'href="#{new_id}"')
            content = content.replace(f'xlink:href="#{old_id}"', f'xlink:href="#{new_id}"')
        
        encoded_string = base64.b64encode(content.encode('utf-8')).decode('utf-8')
        return f"data:image/svg+xml;base64,{encoded_string}"

# Generator Logic
def generate_xml():
    mxfile = ET.Element("mxfile", host="app.diagrams.net", agent="Antigravity-L67", version="21.0.0", type="local")
    diagram = ET.SubElement(mxfile, "diagram", id="enterprise-ai-rag", name="Enterprise AI Architecture")
    mxGraphModel = ET.SubElement(diagram, "mxGraphModel", dx="1422", dy="798", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth="1169", pageHeight="1654", math="0", shadow="0")
    root = ET.SubElement(mxGraphModel, "root")
    
    # Base cells
    ET.SubElement(root, "mxCell", id="0")
    ET.SubElement(root, "mxCell", id="1", parent="0")

    # Layout CONSTANTS
    PAGE_WIDTH = 1100
    COL_LEFT = 300
    COL_RIGHT = 800
    LAYER_SPACING = 160
    ICON_SIZE = 60
    
    # Layer Definitions (Y-Coordinates)
    LAYERS = {
        "USERS": 50,
        "TM": 180,
        "AGW": 330,
        "APIM": 480,
        "APP": 630,
        "AI": 780,
        "DATA": 930,
        "SHARED": 1080,
        "HUB": 1230,
        "GOV": 1380
    }

    def add_rect(id, value, style, x, y, w, h, parent="1"):
        cell = ET.SubElement(root, "mxCell", id=id, value=value, style=style, vertex="1", parent=parent)
        ET.SubElement(cell, "mxGeometry", x=str(x), y=str(y), width=str(w), height=str(h), attrib={"as": "geometry"})
        return cell

    def add_icon(id, value, icon_alias, x, y, parent="1"):
        full_path = find_icon_path(icon_map.get(icon_alias, ""))
        b64 = get_base64_svg(full_path, id) if full_path else ""
        style = f"shape=image;html=1;labelBackgroundColor=none;align=center;verticalAlign=top;verticalLabelPosition=bottom;image={b64};pointerEvents=1;aspect=fixed;"
        cell = ET.SubElement(root, "mxCell", id=id, value=value, style=style, vertex="1", parent=parent)
        ET.SubElement(cell, "mxGeometry", x=str(x), y=str(y), width=str(ICON_SIZE), height=str(ICON_SIZE), attrib={"as": "geometry"})
        return cell

    def add_edge(id, source, target, value="", style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeWidth=2;"):
        edge = ET.SubElement(root, "mxCell", id=id, value=value, style=style, edge="1", parent="1", source=source, target=target)
        ET.SubElement(edge, "mxGeometry", relative="1", attrib={"as": "geometry"})
        return edge

    # --- CONTAINERS (Landing Zones) ---
    # Management Group
    add_rect("mg-ent", "<b>Management Group: Enterprise-AI</b>", "swimlane;whiteSpace=wrap;html=1;dashed=1;dashPattern=1 4;fillColor=#F3F2F1;strokeColor=#605E5C;startSize=30", 20, 20, PAGE_WIDTH, 1500)
    
    # Subscriptions
    # Connectivity
    add_rect("sub-conn", "<b>Subscription: Connectivity</b>", "swimlane;fillColor=#FFFFFF;strokeColor=#0078D4;startSize=25", 40, LAYERS["HUB"]-40, PAGE_WIDTH-40, 200, "mg-ent")
    # Security & Governance
    add_rect("sub-sec", "<b>Subscription: Security</b>", "swimlane;fillColor=#FFFFFF;strokeColor=#0078D4;startSize=25", 40, LAYERS["GOV"]-40, PAGE_WIDTH-40, 140, "mg-ent")
    # Shared Services
    add_rect("sub-shared", "<b>Subscription: Shared Services</b>", "swimlane;fillColor=#FFFFFF;strokeColor=#0078D4;startSize=25", 40, LAYERS["SHARED"]-40, PAGE_WIDTH-40, 140, "mg-ent")
    # Production
    add_rect("sub-prod", "<b>Subscription: Production AI</b>", "swimlane;fillColor=#FFFFFF;strokeColor=#D83B01;startSize=25", 40, LAYERS["AGW"]-40, PAGE_WIDTH-40, 680, "mg-ent")

    # --- REGIONS ---
    # UAE North (Primary)
    add_rect("region-uae", "<b>Region: UAE North (Primary)</b>", "swimlane;fillColor=#E5F0FF;strokeColor=#0078D4", 20, 40, 480, 600, "sub-prod")
    # UK Central (Secondary)
    add_rect("region-ukc", "<b>Region: UK Central (Secondary)</b>", "swimlane;fillColor=#FFF4CE;strokeColor=#D83B01", 520, 40, 480, 600, "sub-prod")

    # --- LAYER 1: USERS ---
    add_icon("icon-usr", "External Users", "icon-users", PAGE_WIDTH//2 - 25, LAYERS["USERS"])

    # --- LAYER 2: GLOBAL ROUTING ---
    add_icon("icon-tm-glb", "Azure Traffic Manager", "icon-tm", PAGE_WIDTH//2 - 25, LAYERS["TM"])
    
    # --- LAYER 3: APP GATEWAY ---
    add_icon("icon-agw-uae", "App Gateway + WAF", "icon-agw", 100, LAYERS["AGW"] - LAYERS["AGW"] + 60, "region-uae")
    add_icon("icon-agw-ukc", "App Gateway + WAF", "icon-agw", 100, LAYERS["AGW"] - LAYERS["AGW"] + 60, "region-ukc")

    # --- LAYER 4: AI GATEWAY (APIM) ---
    add_icon("icon-apim-uae", "AI Gateway (APIM)", "icon-apim", 100, LAYERS["APIM"] - LAYERS["AGW"] + 60, "region-uae")
    add_icon("icon-apim-ukc", "AI Gateway (APIM)", "icon-apim", 100, LAYERS["APIM"] - LAYERS["AGW"] + 60, "region-ukc")

    # --- LAYER 5: AI ORCHESTRATOR ---
    add_icon("icon-app-uae", "AI Orchestrator", "icon-app", 100, LAYERS["APP"] - LAYERS["AGW"] + 60, "region-uae")
    add_icon("icon-app-ukc", "AI Orchestrator", "icon-app", 100, LAYERS["APP"] - LAYERS["AGW"] + 60, "region-ukc")

    # --- LAYER 6: AI PLATFORM ---
    # Group in UAE
    add_rect("grp-ai-uae", "AI Services", "group", 240, LAYERS["AI"] - LAYERS["AGW"] + 60, 200, 150, "region-uae")
    add_icon("icon-oai-uae", "OpenAI (GPT-4o)", "icon-oai", 10, 10, "grp-ai-uae")
    add_icon("icon-srch-uae", "AI Search", "icon-srch", 10, 80, "grp-ai-uae")
    add_icon("icon-di-uae", "Doc Intelligence", "icon-di", 120, 45, "grp-ai-uae")
    
    # Private Endpoints in UAE
    add_icon("pe-oai-uae", "", "icon-pe", 100, LAYERS["AI"] - LAYERS["AGW"] + 60, "region-uae")
    add_icon("pe-srch-uae", "", "icon-pe", 100, LAYERS["AI"] - LAYERS["AGW"] + 130, "region-uae")
    add_icon("pe-st-uae", "", "icon-pe", 100, LAYERS["DATA"] - LAYERS["AGW"] + 60, "region-uae")

    # Group in UKC
    add_rect("grp-ai-ukc", "AI Services", "group", 240, LAYERS["AI"] - LAYERS["AGW"] + 60, 200, 150, "region-ukc")
    add_icon("icon-oai-ukc", "OpenAI (DR)", "icon-oai", 10, 10, "grp-ai-ukc")
    add_icon("icon-srch-ukc", "AI Search (DR)", "icon-srch", 10, 80, "grp-ai-ukc")

    # --- LAYER 7: DATA ---
    add_icon("icon-st-uae", "Knowledge Base (Blob)", "icon-st", 240, LAYERS["DATA"] - LAYERS["AGW"] + 60, "region-uae")
    add_icon("icon-st-ukc", "Knowledge Base (Replica)", "icon-st", 240, LAYERS["DATA"] - LAYERS["AGW"] + 60, "region-ukc")
    
    # Private Endpoints in UKC
    add_icon("pe-oai-ukc", "", "icon-pe", 100, LAYERS["AI"] - LAYERS["AGW"] + 60, "region-ukc")
    add_icon("pe-srch-ukc", "", "icon-pe", 100, LAYERS["AI"] - LAYERS["AGW"] + 130, "region-ukc")
    add_icon("pe-st-ukc-pe", "", "icon-pe", 100, LAYERS["DATA"] - LAYERS["AGW"] + 60, "region-ukc")

    # --- LAYER 8: SHARED SERVICES ---
    add_icon("icon-kv-sh", "Key Vault", "icon-kv", 100, 50, "sub-shared")
    add_icon("icon-mon-sh", "Monitor", "icon-monitor", 250, 50, "sub-shared")
    add_icon("icon-log-sh", "Log Analytics", "icon-log", 400, 50, "sub-shared")
    add_icon("icon-appins-sh", "App Insights", "icon-insights", 550, 50, "sub-shared")
    add_icon("icon-dnsz-sh", "Private DNS Zones", "icon-dns-zone", 750, 50, "sub-shared")

    # --- LAYER 9: CONNECTIVITY HUB ---
    add_rect("vnet-hub", "<b>VNet: Hub (10.0.0.0/16)</b>", "swimlane;fillColor=#E5F0FF;strokeColor=#0078D4", 40, 40, PAGE_WIDTH-80, 140, "sub-conn")
    add_icon("icon-afw-h", "Firewall", "icon-afw", 100, 50, "vnet-hub")
    add_icon("icon-bst-h", "Bastion", "icon-bastion", 300, 50, "vnet-hub")
    add_icon("icon-vpn-h", "VPN/ER Gateway", "icon-vpn", 500, 50, "vnet-hub")
    add_icon("icon-dnsr-h", "DNS Private Resolver", "icon-dns-res", 750, 50, "vnet-hub")

    # --- LAYER 10: GOVERNANCE ---
    add_icon("icon-pol-g", "Azure Policy", "icon-policy", 100, 50, "sub-sec")
    add_icon("icon-def-g", "Defender for Cloud", "icon-defender", 300, 50, "sub-sec")
    add_icon("icon-cost-g", "Cost Management", "icon-cost", 500, 50, "sub-sec")
    add_rect("lbl-rbac", "RBAC / Role Assignments", "text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;", 750, 60, 180, 30, "sub-sec")

    # --- EDGES (RAG Flow) ---
    add_edge("e1", "icon-usr", "icon-tm-glb", "HTTPS Request")
    add_edge("e2-p", "icon-tm-glb", "icon-agw-uae", "Primary Route", "edgeStyle=orthogonalEdgeStyle;rounded=1;strokeWidth=3;strokeColor=#107C41;fontColor=#107C41;")
    add_edge("e2-s", "icon-tm-glb", "icon-agw-ukc", "Failover", "edgeStyle=orthogonalEdgeStyle;rounded=1;strokeWidth=2;strokeColor=#D83B01;dashed=1;fontColor=#D83B01;")
    
    add_edge("e3-uae", "icon-agw-uae", "icon-apim-uae")
    add_edge("e4-uae", "icon-apim-uae", "icon-app-uae")
    add_edge("e5-uae", "icon-app-uae", "icon-srch-uae", "1. Retrieval")
    add_edge("e6-uae", "icon-app-uae", "icon-oai-uae", "2. Inference")
    
    # Document Ingestion Flow
    add_edge("e7-uae", "icon-st-uae", "icon-di-uae", "Docs")
    add_edge("e8-uae", "icon-di-uae", "icon-srch-uae", "Indexing")

    # Peering indicators (conceptual)
    add_rect("peer-uae", "VNet Peering", "text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontStyle=2", 100, 1200, 100, 30)

    # Output to file
    tree = ET.ElementTree(mxfile)
    with open(output_path, "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)

    print(f"Success: Generated {output_path}")

if __name__ == "__main__":
    generate_xml()
