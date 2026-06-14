
import xml.etree.ElementTree as ET

# Configuration
output_path = r"C:\MyResumePortfolio\docs\Azure_AI_Standard_Architecture.drawio"

# Official Stencil Mapping (Industry Standard)
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
    "dns-zone": "shape=mxgraph.azure2.dns_zones",
    "afw": "shape=mxgraph.azure2.firewall",
    "bastion": "shape=mxgraph.azure2.bastion",
    "vpn": "shape=mxgraph.azure2.virtual_network_gateways",
    "dns-res": "shape=mxgraph.azure2.dns_private_resolver",
    "policy": "shape=mxgraph.azure2.policy",
    "defender": "shape=mxgraph.azure2.microsoft_defender_for_cloud",
    "cost": "shape=mxgraph.azure2.cost_management_and_billing",
    "pe": "shape=mxgraph.azure2.private_endpoints"
}

def generate_xml():
    mxfile = ET.Element("mxfile", host="app.diagrams.net", agent="Antigravity-L67", version="21.0.0", type="local")
    diagram = ET.SubElement(mxfile, "diagram", id="std-azure-ai", name="Reference AI Architecture")
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
        style = f"{shape};html=1;labelBackgroundColor=none;align=center;verticalAlign=top;verticalLabelPosition=bottom;pointerEvents=1;fillColor=#FFFFFF;strokeColor=none;"
        cell = ET.SubElement(root, "mxCell", id=id, value=value, style=style, vertex="1", parent=parent)
        ET.SubElement(cell, "mxGeometry", x=str(x), y=str(y), width=str(ICON_SIZE), height=str(ICON_SIZE), attrib={"as": "geometry"})
        return cell

    # Layers Setup
    add_rect("mg", "<b>Management Group</b>", "swimlane;dashed=1;fillColor=#F3F2F1;startSize=30", 20, 20, PAGE_WIDTH, 1500)
    add_rect("sub-p", "<b>Subscription: AI Production</b>", "swimlane;fillColor=#FFFFFF;strokeColor=#D83B01;startSize=25", 40, 300, 1020, 680, "mg")
    
    # Regional Boundaries
    add_rect("reg-1", "<b>UAE North (Active)</b>", "swimlane;fillColor=#E5F0FF;strokeColor=#0078D4", 20, 40, 480, 600, "sub-p")
    add_rect("reg-2", "<b>UK Central (DR)</b>", "swimlane;fillColor=#FFF4CE;strokeColor=#D83B01", 520, 40, 480, 600, "sub-p")

    # Icons
    add_icon("i1", "Users", "users", 520, 50)
    add_icon("i2", "Traffic Manager", "tm", 520, 180)
    
    # UAE Stack
    add_icon("i3-uae", "App Gateway", "agw", 100, 60, "reg-1")
    add_icon("i4-uae", "AI Gateway", "apim", 100, 180, "reg-1")
    add_icon("i5-uae", "Orchestrator", "app", 100, 300, "reg-1")
    add_icon("i6-uae", "OpenAI", "oai", 300, 300, "reg-1")
    add_icon("i7-uae", "AI Search", "srch", 300, 420, "reg-1")
    add_icon("pe-1", "Private Endpoint", "pe", 200, 310, "reg-1")

    # Connectivity Hub
    add_rect("sub-c", "<b>Subscription: Connectivity</b>", "swimlane;fillColor=#FFFFFF;strokeColor=#0078D4;startSize=25", 40, 1200, 1020, 200, "mg")
    add_icon("fw-1", "Firewall", "afw", 100, 50, "sub-c")
    add_icon("bs-1", "Bastion", "bastion", 250, 50, "sub-c")

    # Output
    tree = ET.ElementTree(mxfile)
    with open(output_path, "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    generate_xml()
