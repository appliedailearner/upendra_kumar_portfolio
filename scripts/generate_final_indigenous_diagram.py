
import xml.etree.ElementTree as ET

# Configuration
output_path = r"C:\MyResumePortfolio\docs\Azure_Enterprise_AI_Indigenous_Architecture.drawio"

# Official Stencil Mapping (Indigenous Draw.io Library)
# These are guaranteed to render as vectors in any Draw.io viewer
stencil_map = {
    "users": "shape=mxgraph.azure2.users",
    "tm": "shape=mxgraph.azure2.traffic_manager",
    "agw": "shape=mxgraph.azure2.application_gateways",
    "apim": "shape=mxgraph.azure2.api_management_services",
    "app": "shape=mxgraph.azure2.app_services",
    "oai": "shape=mxgraph.azure2.openai",
    "srch": "shape=mxgraph.azure2.cognitive_search",
    "di": "shape=mxgraph.azure2.form_recognizers",
    "st": "shape=mxgraph.azure2.storage_accounts",
    "kv": "shape=mxgraph.azure2.key_vaults",
    "monitor": "shape=mxgraph.azure2.monitor",
    "log": "shape=mxgraph.azure2.log_analytics_workspaces",
    "insights": "shape=mxgraph.azure2.application_insights",
    "afw": "shape=mxgraph.azure2.firewall",
    "bastion": "shape=mxgraph.azure2.bastion",
    "pe": "shape=mxgraph.azure2.private_endpoints",
    "policy": "shape=mxgraph.azure2.policy",
    "defender": "shape=mxgraph.azure2.security_center",
    "cost": "shape=mxgraph.azure2.cost_management_and_billing"
}

def generate_xml():
    mxfile = ET.Element("mxfile", host="app.diagrams.net", agent="Antigravity-L67", version="21.0.0", type="local")
    diagram = ET.SubElement(mxfile, "diagram", id="indigenous-azure-ai", name="Indigenous Reference Architecture")
    mxGraphModel = ET.SubElement(diagram, "mxGraphModel", dx="1422", dy="798", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth="1169", pageHeight="1654", math="0", shadow="0")
    root = ET.SubElement(mxGraphModel, "root")
    
    # Base cells
    ET.SubElement(root, "mxCell", id="0")
    ET.SubElement(root, "mxCell", id="1", parent="0")

    PAGE_WIDTH = 1100
    ICON_SIZE = 60
    
    def add_rect(id, value, style, x, y, w, h, parent="1"):
        cell = ET.SubElement(root, "mxCell", id=id, value=value, style=style, vertex="1", parent=parent)
        ET.SubElement(cell, "mxGeometry", x=str(x), y=str(y), width=str(w), height=str(h), attrib={"as": "geometry"})
        return cell

    def add_icon(id, value, stencil_key, x, y, parent="1"):
        shape = stencil_map.get(stencil_key, "")
        # Native Stencil Style (NO image= header needed)
        style = f"verticalLabelPosition=bottom;html=1;verticalAlign=top;align=center;strokeColor=none;fillColor=none;{shape};pointerEvents=1;"
        cell = ET.SubElement(root, "mxCell", id=id, value=value, style=style, vertex="1", parent=parent)
        ET.SubElement(cell, "mxGeometry", x=str(x), y=str(y), width=str(ICON_SIZE), height=str(ICON_SIZE), attrib={"as": "geometry"})
        return cell

    # --- MANAGEMENT GROUP BOUNDARY ---
    add_rect("mg", "<b>Management Group: Enterprise-AI</b>", "swimlane;whiteSpace=wrap;html=1;dashed=1;dashPattern=1 4;fillColor=#F3F2F1;strokeColor=#605E5C;startSize=30", 20, 20, PAGE_WIDTH, 1400)

    # --- LAYER 1: USERS ---
    add_icon("usr", "External Users", "users", 520, 50, "mg")

    # --- LAYER 2: GLOBAL ---
    add_icon("tm", "Traffic Manager", "tm", 520, 150, "mg")

    # --- LAYER 3: SUBSCRIPTIONS ---
    add_rect("sub-prod", "<b>Subscription: Production AI</b>", "swimlane;fillColor=#FFFFFF;strokeColor=#D83B01;startSize=25", 40, 260, 1020, 680, "mg")
    
    # --- LAYER 4: REGIONAL LANDING ZONES ---
    add_rect("reg-uae", "<b>UAE North (Active)</b>", "swimlane;fillColor=#E5F0FF;strokeColor=#0078D4", 20, 40, 480, 600, "sub-prod")
    add_rect("reg-ukc", "<b>UK Central (DR)</b>", "swimlane;fillColor=#FFF4CE;strokeColor=#D83B01", 520, 40, 480, 600, "sub-prod")

    # --- UAE STACK ---
    add_icon("agw-uae", "App Gateway", "agw", 210, 50, "reg-uae")
    add_icon("apim-uae", "AI Proxy", "apim", 210, 150, "reg-uae")
    add_icon("app-uae", "Orchestrator", "app", 210, 250, "reg-uae")
    add_icon("oai-uae", "Azure OpenAI", "oai", 380, 250, "reg-uae")
    add_icon("srch-uae", "AI Search", "srch", 380, 360, "reg-uae")
    add_icon("pe-uae", "Private Endpoint", "pe", 320, 260, "reg-uae")
    add_icon("st-uae", "Storage", "st", 100, 450, "reg-uae")

    # --- UKC STACK ---
    add_icon("agw-ukc", "App Gateway", "agw", 210, 50, "reg-ukc")
    add_icon("oai-ukc", "Azure OpenAI (DR)", "oai", 380, 250, "reg-ukc")

    # --- LAYER 8: SHARED SERVICES ---
    add_rect("sub-shared", "<b>Subscription: Shared Services</b>", "swimlane;fillColor=#FFFFFF;strokeColor=#0078D4;startSize=25", 40, 960, 1020, 120, "mg")
    add_icon("mon", "Monitor", "monitor", 100, 40, "sub-shared")
    add_icon("law", "Log Analytics", "log", 250, 40, "sub-shared")
    add_icon("ai", "App Insights", "insights", 400, 40, "sub-shared")

    # --- LAYER 9: CONNECTIVITY ---
    add_rect("sub-conn", "<b>Subscription: Connectivity</b>", "swimlane;fillColor=#FFFFFF;strokeColor=#0078D4;startSize=25", 40, 1100, 1020, 150, "mg")
    add_icon("fw", "Firewall", "afw", 100, 40, "sub-conn")
    add_icon("bas", "Bastion", "bastion", 250, 40, "sub-conn")

    # --- LAYER 10: GOVERNANCE ---
    add_rect("sub-sec", "<b>Subscription: Security</b>", "swimlane;fillColor=#FFFFFF;strokeColor=#0078D4;startSize=25", 40, 1260, 1020, 120, "mg")
    add_icon("pol", "Policy", "policy", 100, 40, "sub-sec")
    add_icon("def", "Defender", "defender", 250, 40, "sub-sec")
    add_icon("cost", "Cost Mgmt", "cost", 400, 40, "sub-sec")

    # Save
    tree = ET.ElementTree(mxfile)
    with open(output_path, "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    generate_xml()
