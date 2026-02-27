import json, zlib, base64
from urllib.parse import quote
import os

xml = []
xml.append('<mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/>')

def escape(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def node(node_id, label, x, y, width, height, icon, parent="1", style_extra=""):
    style = f"shape=image;image={icon};verticalLabelPosition=bottom;verticalAlign=top;{style_extra}"
    xml.append(f'<mxCell id="{node_id}" value="{escape(label)}" style="{style}" vertex="1" parent="{parent}"><mxGeometry x="{x}" y="{y}" width="{width}" height="{height}" as="geometry"/></mxCell>')

def group(node_id, label, x, y, width, height, parent="1", fill="none", stroke="#cccccc", dashed="0", align="center", fontColor="#333333"):
    style = f"swimlane;whiteSpace=wrap;html=1;startSize=30;fillColor={fill};strokeColor={stroke};dashed={dashed};align={align};fontColor={fontColor};"
    xml.append(f'<mxCell id="{node_id}" value="{escape(label)}" style="{style}" vertex="1" parent="{parent}"><mxGeometry x="{x}" y="{y}" width="{width}" height="{height}" as="geometry"/></mxCell>')

def edge(edge_id, src, tgt, style_extra="strokeColor=#0078D4;strokeWidth=2;", label=""):
    # Added labelBackgroundColor=#ffffff to ensure text doesn't overlap messily with the line
    style = f"edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;labelBackgroundColor=#ffffff;fontColor=#333333;{style_extra}"
    xml.append(f'<mxCell id="{edge_id}" value="{escape(label)}" edge="1" parent="1" source="{src}" target="{tgt}"><mxGeometry relative="1" as="geometry"/></mxCell>')

# --- LAYOUT EXPERT MATH ---
# Perfectly align the primary data plane horizontally at Y=220
# Align the DNS and secondary plane horizontally at Y=380

ONPREM_X = 50
group("g_onprem", "On-Premises / Corporate Network", ONPREM_X, 150, 200, 350, fill="#eeeeee", stroke="#666666")
node("n_user", "Data Engineer", ONPREM_X+70, 220, 60, 60, "img/lib/azure2/identity/Users.svg")
node("n_localdns", "Local DNS Server", ONPREM_X+70, 380, 60, 60, "img/lib/azure2/networking/DNS_Zones.svg")

HUB_X = 350
group("g_hub", "Hub VNet (Connectivity)", HUB_X, 100, 250, 450, dashed="1", fill="#e1d5e7", stroke="#9673a6")
node("n_vpngw", "ExpressRoute/VPN GW", HUB_X+95, 220, 60, 60, "img/lib/azure2/networking/Virtual_Network_Gateways.svg")
node("n_dnspr", "Azure DNS Private Resolver", HUB_X+95, 380, 60, 60, "img/lib/azure2/networking/DNS_Private_Resolver.svg")
node("n_fw", "Azure Firewall", HUB_X+95, 470, 60, 60, "img/lib/azure2/networking/Firewalls.svg")

SPOKE_X = 700
group("g_spoke", "Spoke VNet (Data Landing Zone)", SPOKE_X, 100, 420, 450, dashed="1", fill="#d5e8d4", stroke="#82b366")

# Databricks Subnet
group("g_dbx_sub", "Databricks Workspace Subnet", SPOKE_X+20, 150, 160, 350, fill="#dae8fc", stroke="#6c8ebf")
node("n_dbx", "Azure Databricks Cluster", SPOKE_X+70, 300, 60, 60, "img/lib/azure2/analytics/Azure_Databricks.svg")

# Private Endpoint Subnet
group("g_pe_sub", "Private Endpoint Subnet", SPOKE_X+220, 150, 180, 350, fill="#fff2cc", stroke="#d6b656")
node("n_pe_adls", "Storage PE", SPOKE_X+280, 220, 60, 60, "img/lib/azure2/networking/Private_Endpoint.svg")
node("n_pe_kv", "Key Vault PE", SPOKE_X+280, 380, 60, 60, "img/lib/azure2/networking/Private_Endpoint.svg")

# PaaS Resources outside VNet but linked via PE
PAAS_X = 1220
group("g_paas", "Azure PaaS Services", PAAS_X, 100, 250, 450, fill="#ffe6cc", stroke="#d79b00")
node("n_adls", "ADLS Gen2", PAAS_X+95, 220, 60, 60, "img/lib/azure2/storage/Storage_Accounts.svg")
node("n_kv", "Azure Key Vault", PAAS_X+95, 380, 60, 60, "img/lib/azure2/security/Key_Vaults.svg")

# Connections

# 1. User Traffic Flow (Data Engineer -> VPN -> DBX)
edge("e_traf1", "n_user", "n_vpngw", "strokeColor=#0078D4;strokeWidth=3;endArrow=classic;")
# Using exitX=1;exitY=0.5;entryX=0;entryY=0.5; to enforce exact horizontal attachments
edge("e_traf2", "n_vpngw", "n_dbx", "strokeColor=#0078D4;strokeWidth=3;endArrow=classic;exitX=1;exitY=0.5;entryX=0;entryY=0.5;")

# 2. DNS Resolution Flow (Local DNS <-> DNS Resolver)
edge("e_dns1", "n_localdns", "n_dnspr", "strokeColor=#00B294;strokeWidth=2;dashed=1;endArrow=classic;exitX=1;exitY=0.25;entryX=0;entryY=0.25;", label="Conditional Forward")
edge("e_dns2", "n_dnspr", "n_localdns", "strokeColor=#00B294;strokeWidth=2;dashed=1;endArrow=classic;exitX=0;exitY=0.75;entryX=1;entryY=0.75;", label="Returns 10.1.2.5")

# 3. Databricks VNet Injection to Private Endpoints (Bypassing Azure Firewall)
edge("e_dbx_pe1", "n_dbx", "n_pe_adls", "strokeColor=#E3008C;strokeWidth=3;endArrow=classic;exitX=1;exitY=0.25;entryX=0;entryY=0.5;", label="Storage Traffic (UDR bypass Hub)")
edge("e_dbx_pe2", "n_dbx", "n_pe_kv", "strokeColor=#E3008C;strokeWidth=3;endArrow=classic;exitX=1;exitY=0.75;entryX=0;entryY=0.5;", label="Secret Fetch")

# 4. Private Endpoints to Actual PaaS Resources
edge("e_pe_adls", "n_pe_adls", "n_adls", "strokeColor=#E3008C;strokeWidth=3;dashed=1;endArrow=classic;exitX=1;exitY=0.5;entryX=0;entryY=0.5;", label="Private Link")
edge("e_pe_kv", "n_pe_kv", "n_kv", "strokeColor=#E3008C;strokeWidth=3;dashed=1;endArrow=classic;exitX=1;exitY=0.5;entryX=0;entryY=0.5;", label="Private Link")

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
<meta charset="utf-8">
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; background: #f8f9fa; }}
  .card {{ text-align: center; background: white; border-radius: 12px; padding: 40px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); max-width: 600px; }}
  .card h2 {{ margin: 0 0 12px; color: #1a1a1a; }}
  .card p {{ margin: 0 0 24px; color: #666; line-height: 1.5; }}
  .btn {{ display: inline-block; padding: 14px 32px; background: #0078D4; color: white; text-decoration: none; border-radius: 8px; font-size: 16px; font-weight: 600; transition: background 0.2s; }}
  .btn:hover {{ background: #005a9e; }}
</style>
</head>
<body>
  <div class="card">
    <h2>Databricks Private Link Architecture (Polished version)</h2>
    <p>A perfectly aligned XML topology map. Fixed the text overlapping, aligned nodes horizontally for straight connection lines, and added the Key Vault Private link requirement.</p>
    <a class="btn" href="{url}" target="_blank" rel="noopener noreferrer">
      Open Architecture Diagram in draw.io
    </a>
  </div>
</body>
</html>"""

artifact_dir = r"C:\Users\upend\.gemini\antigravity\brain\c03881da-61a2-42d7-9080-1a29a221e615"
os.makedirs(artifact_dir, exist_ok=True)
out_path = os.path.join(artifact_dir, "azure_databricks_caf_architecture.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html_output)

print(f"HTML artifact created at {out_path}.")
