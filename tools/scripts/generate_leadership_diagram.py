
import os
import urllib.parse
import xml.etree.ElementTree as ET
import re

# Configuration
output_path = r"C:\MyResumePortfolio\docs\Azure_Enterprise_AI_Leadership_Architecture.drawio"
icons_base = r"C:\MyResumePortfolio\blog\assets\Azure_Public_Service_Icons\Icons"

# Icon Mapping (Corrected paths)
icon_map = {
    "icon-usr": r"identity\00010-icon-service-Users.svg",
    "icon-tm": r"networking\10065-icon-service-Traffic-Manager-Profiles.svg",
    "icon-agw": r"networking\10064-icon-service-Application-Gateways.svg",
    "icon-apim": r"networking\10042-icon-service-API-Management-Services.svg",
    "icon-app": r"compute\10035-icon-service-App-Services.svg",
    "icon-oai": r"ai_machine_learning\00045-icon-service-Cognitive-Services.svg",
    "icon-srch": r"ai_machine_learning\10156-icon-service-Azure-Cognitive-Search.svg",
    "icon-di": r"ai_machine_learning\02521-icon-service-Form-Recognizers.svg",
    "icon-st": r"storage\10001-icon-service-Storage-Accounts.svg",
    "icon-kv": r"security\10051-icon-service-Key-Vaults.svg",
    "icon-mon": r"management_governance\10056-icon-service-Monitor.svg",
    "icon-law": r"management_governance\10005-icon-service-Log-Analytics-Workspaces.svg",
    "icon-ai": r"management_governance\10055-icon-service-Application-Insights.svg",
    "icon-fw": r"networking\10015-icon-service-Firewalls.svg",
    "icon-bas": r"networking\10066-icon-service-Bastion.svg",
    "icon-pe": r"other\02579-icon-service-Private-Endpoints.svg",
    "icon-policy": r"management_governance\10316-icon-service-Policy.svg",
    "icon-defender": r"security\10241-icon-service-Microsoft-Defender-for-Cloud.svg"
}

def get_encoded_svg(icon_key, cell_id):
    rel_path = icon_map.get(icon_key)
    if not rel_path: return ""
    full_path = os.path.join(icons_base, rel_path)
    if not os.path.exists(full_path): return ""
    
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Clean the SVG (remove newlines and XML declaration)
    content = re.sub(r'<\?xml.*?\?>', '', content)
    content = content.replace('\n', ' ').replace('\r', '')

    # CRITICAL: Rename internal IDs to prevent clashing across multiple icons
    # This prevents 'Grey Mountains' or 'Broken Gradients'
    id_prefix = f"cell_{cell_id}_"
    content = re.sub(r'id=["\'](.*?)["\']', lambda m: f'id="{id_prefix}{m.group(1)}"', content)
    content = re.sub(r'url\(#(.*?)\)', lambda m: f'url(#{id_prefix}{m.group(1)})', content)
    content = re.sub(r'xlink:href=["\']#(.*?)["\']', lambda m: f'xlink:href="#{id_prefix}{m.group(1)}"', content)

    # URL Encode for Draw.io (Self-contained and no semicolon issues)
    encoded = urllib.parse.quote(content)
    return f"data:image/svg+xml,{encoded}"

def generate_xml():
    mxfile = ET.Element("mxfile", host="app.diagrams.net", agent="Antigravity-L67", version="21.0.0", type="local")
    diagram = ET.SubElement(mxfile, "diagram", id="leadership-ai", name="Reference AI Architecture")
    mxGraphModel = ET.SubElement(diagram, "mxGraphModel", dx="1422", dy="798", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth="1169", pageHeight="1654", math="0", shadow="0")
    root = ET.SubElement(mxGraphModel, "root")
    
    ET.SubElement(root, "mxCell", id="0")
    ET.SubElement(root, "mxCell", id="1", parent="0")

    PAGE_WIDTH = 1100
    ICON_SIZE = 60
    
    def add_rect(id, value, style, x, y, w, h, parent="1"):
        cell = ET.SubElement(root, "mxCell", id=id, value=value, style=style, vertex="1", parent=parent)
        ET.SubElement(cell, "mxGeometry", x=str(x), y=str(y), width=str(w), height=str(h), attrib={"as": "geometry"})

    def add_icon(id, value, icon_key, x, y, parent="1"):
        data_uri = get_encoded_svg(icon_key, id)
        style = f"shape=image;html=1;labelBackgroundColor=none;align=center;verticalAlign=top;verticalLabelPosition=bottom;imageAspect=1;image={data_uri};"
        cell = ET.SubElement(root, "mxCell", id=id, value=value, style=style, vertex="1", parent=parent)
        ET.SubElement(cell, "mxGeometry", x=str(x), y=str(y), width=str(ICON_SIZE), height=str(ICON_SIZE), attrib={"as": "geometry"})

    # --- ARCHITECTURE LAYOUT ---
    add_rect("mg", "<b>Management Group: Enterprise-AI</b>", "swimlane;whiteSpace=wrap;html=1;dashed=1;dashPattern=1 4;fillColor=#F3F2F1;strokeColor=#605E5C;startSize=30", 20, 20, PAGE_WIDTH, 1400)
    
    # Layer 1: Users
    add_icon("usr-1", "External Users", "icon-usr", 520, 50, "mg")
    
    # Layer 2: Global
    add_icon("tm-1", "Azure Traffic Manager", "icon-tm", 520, 150, "mg")

    # Layer 3-7: Subscriptions
    add_rect("sub-p", "<b>Subscription: Production AI</b>", "swimlane;fillColor=#FFFFFF;strokeColor=#D83B01;startSize=25", 40, 260, 1020, 680, "mg")
    
    # Regional Landing Zones
    add_rect("reg-uae", "<b>Primary: UAE North</b>", "swimlane;fillColor=#E5F0FF;strokeColor=#0078D4", 20, 40, 480, 600, "sub-p")
    add_rect("reg-ukc", "<b>Failover: UK Central</b>", "swimlane;fillColor=#FFF4CE;strokeColor=#D83B01", 520, 40, 480, 600, "sub-p")

    # UAE Resources
    add_icon("agw-uae", "App Gateway (WAF)", "icon-agw", 210, 50, "reg-uae")
    add_icon("apim-uae", "AI Proxy (APIM)", "icon-apim", 210, 150, "reg-uae")
    add_icon("app-uae", "RAG Orchestrator", "icon-app", 210, 250, "reg-uae")
    add_icon("pe-uae-1", "", "icon-pe", 320, 260, "reg-uae")
    add_icon("oai-uae", "Azure OpenAI", "icon-oai", 380, 250, "reg-uae")
    add_icon("srch-uae", "Azure AI Search", "icon-srch", 380, 360, "reg-uae")

    # Hub Subscription
    add_rect("sub-c", "<b>Subscription: Connectivity (Hub)</b>", "swimlane;fillColor=#FFFFFF;strokeColor=#0078D4;startSize=25", 40, 1100, 1020, 200, "mg")
    add_icon("fw-hub", "Azure Firewall", "icon-fw", 100, 60, "sub-c")
    add_icon("bas-hub", "Azure Bastion", "icon-bas", 250, 60, "sub-c")

    # Save
    tree = ET.ElementTree(mxfile)
    with open(output_path, "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    generate_xml()
