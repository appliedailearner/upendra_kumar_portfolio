import base64
import json
import zlib
from urllib.parse import quote

xml = []
xml.append('<mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1100" pageHeight="850" math="0" shadow="0"><root>')
xml.append('<mxCell id="0" /><mxCell id="1" parent="0" />')

def node(id_str, label, x, y, width, height, icon_path="", fill="#ffffff", stroke="#000000"):
    style = f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
    if icon_path:
        style = f"shape=image;image={icon_path};verticalLabelPosition=bottom;verticalAlign=top;imageBackground="
    xml.append(f'<mxCell id="{id_str}" value="{label}" style="{style}" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{width}" height="{height}" as="geometry" /></mxCell>')

def group(id_str, label, x, y, width, height, fill="#f5f5f5", stroke="#666666", dashed="1"):
    style = f"rounded=0;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};dashed={dashed};verticalAlign=top;spacingTop=10;fontStyle=1"
    xml.append(f'<mxCell id="{id_str}" value="" style="{style}" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{width}" height="{height}" as="geometry" /></mxCell>')
    text_style = "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontStyle=1;fontSize=14"
    xml.append(f'<mxCell id="{id_str}_text" value="{label}" style="{text_style}" vertex="1" parent="1"><mxGeometry x="{x+10}" y="{y+5}" width="{width-20}" height="20" as="geometry" /></mxCell>')

def text(id_str, label, x, y, width, height, color="#000000"):
    style = f"text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontColor={color};fontStyle=1"
    xml.append(f'<mxCell id="{id_str}" value="{label}" style="{style}" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{width}" height="{height}" as="geometry" /></mxCell>')

def edge(id_str, source, target, style_params="strokeColor=#000000;strokeWidth=2;endArrow=classic;", label="", waypoints=None):
    geom = '<mxGeometry relative="1" as="geometry">'
    if waypoints:
        pts = "".join([f'<mxPoint x="{px}" y="{py}" />' for px, py in waypoints])
        geom = f'<mxGeometry relative="1" as="geometry"><Array as="points">{pts}</Array></mxGeometry>'
    
    xml.append(f'<mxCell id="{id_str}" value="{label}" style="{style_params}" edge="1" parent="1" source="{source}" target="{target}">{geom}</mxCell>')

# ----- DIAGRAM LAYOUT (TOGAF Style Architecture Block Diagram) -----

# Legend
group("g_legend", "Architecture Legend", 50, 50, 300, 150, fill="#ffffff", stroke="#000000", dashed="0")
edge("l_e1", "dummy1", "dummy2", "strokeColor=#0078D4;strokeWidth=3;endArrow=classic;", waypoints=[(70, 90), (120, 90)])
text("l_t1", "Flow 1: Front-End (Workspace UI)", 130, 80, 200, 20, color="#0078D4")

edge("l_e2", "dummy3", "dummy4", "strokeColor=#E3008C;strokeWidth=3;endArrow=classic;", waypoints=[(70, 130), (120, 130)])
text("l_t2", "Flow 2: Back-End (Control Plane)", 130, 120, 200, 20, color="#E3008C")

edge("l_e3", "dummy5", "dummy6", "strokeColor=#00B294;strokeWidth=3;endArrow=classic;", waypoints=[(70, 170), (120, 170)])
text("l_t3", "Flow 3: Data Plane (PaaS)", 130, 160, 200, 20, color="#00B294")


# Zones
ON_PREM_X = 50
VNET_X = 350
CP_X = 850

# Zone 1: Corporate Network
group("g_onprem", "Corporate Network (Users)", ON_PREM_X, 230, 250, 200, fill="#f8f9fa", stroke="#ced4da", dashed="0")
node("n_user", "Data Engineering Desktop", ON_PREM_X+90, 300, 60, 60, "img/lib/azure2/identity/Users.svg")

# Zone 2: Customer VNet
group("g_vnet", "Customer Managed VNet", VNET_X, 230, 450, 400, fill="#d1e7dd", stroke="#0f5132", dashed="0")
node("n_pe_front", "Workspace Private Endpoint\\n(Front-End)", VNET_X+50, 300, 60, 60, "img/lib/azure2/networking/Private_Endpoint.svg")
node("n_cluster", "Databricks Compute Cluster\\n(Injected Subnet)", VNET_X+200, 450, 60, 60, "img/lib/azure2/analytics/Azure_Databricks.svg")
node("n_pe_back", "SCC Relay Private Endpoint\\n(Back-End)", VNET_X+340, 450, 60, 60, "img/lib/azure2/networking/Private_Endpoint.svg")
node("n_pe_paas", "Storage/KV Private Endpoint\\n(Data Plane)", VNET_X+200, 550, 60, 60, "img/lib/azure2/networking/Private_Endpoint.svg")

# Zone 3: Control Plane
group("g_cp", "Databricks Control Plane", CP_X, 230, 250, 400, fill="#cfe2ff", stroke="#084298", dashed="0")
node("n_webapp", "Workspace Web App", CP_X+90, 300, 60, 60, "img/lib/azure2/app_services/App_Services.svg")
node("n_scc", "SCC Secure Relay", CP_X+90, 450, 60, 60, "img/lib/azure2/networking/Connections.svg")

# Zone 4: PaaS Backbone
group("g_paas", "Azure PaaS Backbone", VNET_X, 680, 450, 150, fill="#fff3cd", stroke="#856404", dashed="0")
node("n_adls", "ADLS Gen2", VNET_X+100, 730, 60, 60, "img/lib/azure2/storage/Storage_Accounts.svg")
node("n_kv", "Azure Key Vault", VNET_X+300, 730, 60, 60, "img/lib/azure2/security/Key_Vaults.svg")

# EDGES (Flows)

# Flow 1
edge("e_f1_a", "n_user", "n_pe_front", "strokeColor=#0078D4;strokeWidth=3;endArrow=classic;")
edge("e_f1_b", "n_pe_front", "n_webapp", "strokeColor=#0078D4;strokeWidth=3;endArrow=classic;dashed=1;")

# Flow 2
edge("e_f2_a", "n_cluster", "n_pe_back", "strokeColor=#E3008C;strokeWidth=3;endArrow=classic;")
edge("e_f2_b", "n_pe_back", "n_scc", "strokeColor=#E3008C;strokeWidth=3;endArrow=classic;dashed=1;")

# Flow 3
edge("e_f3_a", "n_cluster", "n_pe_paas", "strokeColor=#00B294;strokeWidth=3;endArrow=classic;", waypoints=[(VNET_X+230, 520)])
edge("e_f3_b", "n_pe_paas", "n_adls", "strokeColor=#00B294;strokeWidth=3;endArrow=classic;dashed=1;", waypoints=[(VNET_X+230, 650), (VNET_X+130, 650)])
edge("e_f3_c", "n_pe_paas", "n_kv", "strokeColor=#00B294;strokeWidth=3;endArrow=classic;dashed=1;", waypoints=[(VNET_X+230, 650), (VNET_X+330, 650)])

# Annotations
text("t_backbone1", "Microsoft Backbone", VNET_X+180, 270, 150, 20, color="#666666")
text("t_backbone2", "Microsoft Backbone", VNET_X+400, 420, 150, 20, color="#666666")
text("t_backbone3", "Microsoft Backbone", VNET_X+230, 630, 150, 20, color="#666666")


xml.append('</root></mxGraphModel>')
diagram_xml = "".join(xml)

encoded = quote(diagram_xml, safe='')
c = zlib.compressobj(9, zlib.DEFLATED, -15)
raw_deflate = c.compress(encoded.encode('utf-8')) + c.flush()
data = base64.b64encode(raw_deflate).decode()

payload = json.dumps({"type": "xml", "compressed": True, "data": data})
url = f"https://app.diagrams.net/?pv=0&grid=0#create={quote(payload, safe='')}"

html_output = f"""<!DOCTYPE html>
<html>
<head>
    <title>3 Private Link Flows TOGAF Diagram</title>
    <style>
        body {{ font-family: sans-serif; padding: 40px; text-align: center; }}
        .btn {{ display: inline-block; padding: 15px 30px; font-size: 18px; color: white; background-color: #0078D4; text-decoration: none; border-radius: 8px; }}
        .btn:hover {{ background-color: #005a9e; }}
    </style>
</head>
<body>
    <h1>Azure Databricks 3 Private Link Flows (TOGAF Style)</h1>
    <p>Click the button below to open the generated architecture diagram in draw.io.</p>
    <a href="{url}" class="btn" target="_blank">Open draw.io Diagram</a>
</body>
</html>
"""

import os
brain_dir = r"C:\Users\upend\.gemini\antigravity\brain\c03881da-61a2-42d7-9080-1a29a221e615"
html_path = os.path.join(brain_dir, "dbx_3_flows_togaf.html")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_output)

print(f"HTML artifact created at {html_path}")
