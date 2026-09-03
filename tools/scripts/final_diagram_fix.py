
import base64
import os

# Define the absolute workspace path
workspace = "C:/MyResumePortfolio"
icon_base = f"{workspace}/blog/assets/Azure_Public_Service_Icons/Icons"
output_file = f"{workspace}/docs/Azure_AI_Platform_Architecture.drawio"

# Robust mapping of IDs to local SVG paths
icon_map = {
    "icon-afw-uae": f"{icon_base}/networking/10084-icon-service-Firewalls.svg",
    "icon-bastion-uae": f"{icon_base}/networking/02422-icon-service-Bastions.svg",
    "icon-vpn-uae": f"{icon_base}/networking/10063-icon-service-Virtual-Network-Gateways.svg",
    "icon-dns-uae": f"{icon_base}/networking/02882-icon-service-DNS-Private-Resolver.svg",
    "icon-afw-ukc": f"{icon_base}/networking/10084-icon-service-Firewalls.svg",
    "icon-sentinel": f"{icon_base}/security/10248-icon-service-Azure-Sentinel.svg",
    "icon-defender": f"{icon_base}/security/10241-icon-service-Microsoft-Defender-for-Cloud.svg",
    "icon-policy": f"{icon_base}/management + governance/10316-icon-service-Policy.svg",
    "icon-agw-uae": f"{icon_base}/networking/10076-icon-service-Application-Gateways.svg",
    "icon-apim-uae": f"{icon_base}/ai + machine learning/03173-icon-service-Cognitive-Services-Decisions.svg",
    "icon-app-uae": f"{icon_base}/app services/10035-icon-service-App-Services.svg",
    "icon-oai-uae": f"{icon_base}/ai + machine learning/03438-icon-service-Azure-OpenAI.svg",
    "icon-srch-uae": f"{icon_base}/ai + machine learning/03321-icon-service-Serverless-Search.svg",
    "icon-di-uae": f"{icon_base}/ai + machine learning/00819-icon-service-Form-Recognizers.svg",
    "icon-st-uae": f"{icon_base}/storage/10086-icon-service-Storage-Accounts.svg",
    "icon-agw-ukc": f"{icon_base}/networking/10076-icon-service-Application-Gateways.svg",
    "icon-app-ukc": f"{icon_base}/app services/10035-icon-service-App-Services.svg",
    "icon-tm-global": f"{icon_base}/networking/10065-icon-service-Traffic-Manager-Profiles.svg"
}

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')
    return None

# Generate the ENTIRE XML to ensure it's clean and "Leadership Worthy"
xml = f"""<mxfile host="app.diagrams.net" modified="2026-03-15T15:45:00.000Z" agent="Antigravity-L67" version="21.0.0" type="local">
  <diagram id="azure-ai-multi-region" name="Multi-Region AI Platform">
    <mxGraphModel dx="1422" dy="798" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        
        <!-- Management Groups -->
        <mxCell id="mg-platform" value="&lt;b&gt;Management Group: mg-platform&lt;/b&gt;" style="swimlane;whiteSpace=wrap;html=1;dashed=1;dashPattern=1 4;fillColor=#F3F2F1;strokeColor=#605E5C;startSize=30" vertex="1" parent="1">
          <mxGeometry x="20" y="20" width="1120" height="280" as="geometry" />
        </mxCell>
        
        <mxCell id="sub-connectivity" value="&lt;b&gt;Subscription: sub-connectivity-01&lt;/b&gt;" style="swimlane;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#0078D4;startSize=25;fontColor=#0078D4" vertex="1" parent="mg-platform">
          <mxGeometry x="20" y="50" width="700" height="200" as="geometry" />
        </mxCell>
        
        <mxCell id="vnet-hub-uae" value="&lt;b&gt;Hub UAE North (10.0.0.0/16)&lt;/b&gt;" style="swimlane;whiteSpace=wrap;html=1;fillColor=#E5F0FF;strokeColor=#0078D4" vertex="1" parent="sub-connectivity">
          <mxGeometry x="20" y="40" width="300" height="140" as="geometry" />
        </mxCell>
        
        <!-- ICONS WITH EMBEDDED DATA URIS -->
"""

# UAE Hub Icons
icons_to_add = [
    ("icon-afw-uae", "Azure Firewall", "vnet-hub-uae", 30, 45, 45, 40),
    ("icon-bastion-uae", "Bastion", "vnet-hub-uae", 110, 45, 45, 40),
    ("icon-vpn-uae", "VPN Gateway", "vnet-hub-uae", 190, 45, 45, 40),
    ("icon-dns-uae", "DNS Resolver", "vnet-hub-uae", 110, 100, 45, 40)
]

for cid, val, parent, x, y, w, h in icons_to_add:
    b64 = get_base64(icon_map[cid])
    style = f"image;html=1;labelBackgroundColor=none;align=center;verticalAlign=top;verticalLabelPosition=bottom;image=data:image/svg+xml;base64,{b64}"
    xml += f'        <mxCell id="{cid}" value="{val}" style="{style}" vertex="1" parent="{parent}">\n'
    xml += f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />\n'
    xml += f'        </mxCell>\n'

# UKC Hub
xml += f"""
        <mxCell id="vnet-hub-ukc" value="&lt;b&gt;Hub UK Central (10.100.0.0/16)&lt;/b&gt;" style="swimlane;whiteSpace=wrap;html=1;fillColor=#E5F0FF;strokeColor=#0078D4" vertex="1" parent="sub-connectivity">
          <mxGeometry x="380" y="40" width="300" height="140" as="geometry" />
        </mxCell>
"""
b64_afw_ukc = get_base64(icon_map["icon-afw-ukc"])
style_afw_ukc = f"image;html=1;labelBackgroundColor=none;align=center;verticalAlign=top;verticalLabelPosition=bottom;image=data:image/svg+xml;base64,{b64_afw_ukc}"
xml += f'        <mxCell id="icon-afw-ukc" value="Azure Firewall" style="{style_afw_ukc}" vertex="1" parent="vnet-hub-ukc">\n'
xml += f'          <mxGeometry x="30" y="45" width="45" height="40" as="geometry" />\n'
xml += f'        </mxCell>\n'

# Security Subscription
xml += f"""
        <mxCell id="sub-security" value="&lt;b&gt;Subscription: sub-security-01&lt;/b&gt;" style="swimlane;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#0078D4;startSize=25;fontColor=#0078D4" vertex="1" parent="mg-platform">
          <mxGeometry x="740" y="50" width="350" height="200" as="geometry" />
        </mxCell>
"""
sec_icons = [
    ("icon-sentinel", "Sentinel", "sub-security", 50, 45, 50, 50),
    ("icon-defender", "Defender", "sub-security", 150, 45, 50, 50),
    ("icon-policy", "Azure Policy", "sub-security", 250, 45, 50, 50)
]
for cid, val, parent, x, y, w, h in sec_icons:
    b64 = get_base64(icon_map[cid])
    style = f"image;html=1;labelBackgroundColor=none;align=center;verticalAlign=top;verticalLabelPosition=bottom;image=data:image/svg+xml;base64,{b64}"
    xml += f'        <mxCell id="{cid}" value="{val}" style="{style}" vertex="1" parent="{parent}">\n'
    xml += f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />\n'
    xml += f'        </mxCell>\n'

# Landing Zones
xml += f"""
        <mxCell id="mg-landingzones" value="&lt;b&gt;Management Group: mg-landingzones&lt;/b&gt;" style="swimlane;whiteSpace=wrap;html=1;dashed=1;dashPattern=1 4;fillColor=#F3F2F1;strokeColor=#605E5C;startSize=30" vertex="1" parent="1">
          <mxGeometry x="20" y="320" width="1120" height="480" as="geometry" />
        </mxCell>
        
        <mxCell id="sub-prod-ai" value="&lt;b&gt;Subscription: sub-prod-ai-01 (Production)&lt;/b&gt;" style="swimlane;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#0078D4;startSize=25;fontColor=#0078D4" vertex="1" parent="mg-landingzones">
          <mxGeometry x="20" y="40" width="1080" height="420" as="geometry" />
        </mxCell>

        <mxCell id="vnet-prod-uae" value="&lt;b&gt;VNet AI Prod UAE North&lt;/b&gt;" style="swimlane;whiteSpace=wrap;html=1;fillColor=#E5F0FF;strokeColor=#0078D4" vertex="1" parent="sub-prod-ai">
          <mxGeometry x="20" y="40" width="500" height="360" as="geometry" />
        </mxCell>
"""
uae_prod_icons = [
    ("icon-agw-uae", "App Gateway", "vnet-prod-uae", 30, 45, 50, 50),
    ("icon-apim-uae", "API Management", "vnet-prod-uae", 160, 45, 50, 50),
    ("icon-app-uae", "App Service", "vnet-prod-uae", 350, 45, 50, 50)
]
for cid, val, parent, x, y, w, h in uae_prod_icons:
    b64 = get_base64(icon_map[cid])
    style = f"image;html=1;labelBackgroundColor=none;align=center;verticalAlign=top;verticalLabelPosition=bottom;image=data:image/svg+xml;base64,{b64}"
    xml += f'        <mxCell id="{cid}" value="{val}" style="{style}" vertex="1" parent="{parent}">\n'
    xml += f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />\n'
    xml += f'        </mxCell>\n'

# AI Stack Layer
xml += f"""
        <mxCell id="pe-layer-uae" value="&lt;b&gt;Private Endpoints (AI Stack)&lt;/b&gt;" style="swimlane;whiteSpace=wrap;html=1;fillColor=#FFFFFF" vertex="1" parent="vnet-prod-uae">
          <mxGeometry x="20" y="140" width="460" height="200" as="geometry" />
        </mxCell>
"""
ai_icons = [
    ("icon-oai-uae", "Azure OpenAI", "pe-layer-uae", 40, 45, 50, 50),
    ("icon-srch-uae", "AI Search", "pe-layer-uae", 160, 45, 50, 50),
    ("icon-di-uae", "Doc Intelligence", "pe-layer-uae", 280, 45, 50, 50),
    ("icon-st-uae", "Storage", "pe-layer-uae", 380, 45, 50, 50)
]
for cid, val, parent, x, y, w, h in ai_icons:
    b64 = get_base64(icon_map[cid])
    style = f"image;html=1;labelBackgroundColor=none;align=center;verticalAlign=top;verticalLabelPosition=bottom;image=data:image/svg+xml;base64,{b64}"
    xml += f'        <mxCell id="{cid}" value="{val}" style="{style}" vertex="1" parent="{parent}">\n'
    xml += f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />\n'
    xml += f'        </mxCell>\n'

# UKC Region
xml += f"""
        <mxCell id="vnet-prod-ukc" value="&lt;b&gt;VNet AI Prod UK Central&lt;/b&gt;" style="swimlane;whiteSpace=wrap;html=1;fillColor=#E5F0FF;strokeColor=#0078D4" vertex="1" parent="sub-prod-ai">
          <mxGeometry x="550" y="40" width="500" height="360" as="geometry" />
        </mxCell>
"""
ukc_prod_icons = [
    ("icon-agw-ukc", "App Gateway", "vnet-prod-ukc", 30, 45, 50, 50),
    ("icon-app-ukc", "App Service (DR)", "vnet-prod-ukc", 350, 45, 50, 50)
]
for cid, val, parent, x, y, w, h in ukc_prod_icons:
    b64 = get_base64(icon_map[cid])
    style = f"image;html=1;labelBackgroundColor=none;align=center;verticalAlign=top;verticalLabelPosition=bottom;image=data:image/svg+xml;base64,{b64}"
    xml += f'        <mxCell id="{cid}" value="{val}" style="{style}" vertex="1" parent="{parent}">\n'
    xml += f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />\n'
    xml += f'        </mxCell>\n'

# Global Logic
b64_tm = get_base64(icon_map["icon-tm-global"])
style_tm = f"image;html=1;labelBackgroundColor=none;align=center;verticalAlign=top;verticalLabelPosition=bottom;image=data:image/svg+xml;base64,{b64_tm}"
xml += f'        <mxCell id="icon-tm-global" value="Global Traffic Manager" style="{style_tm}" vertex="1" parent="1">\n'
xml += f'          <mxGeometry x="550" y="-80" width="60" height="60" as="geometry" />\n'
xml += f'        </mxCell>\n'

# Closing
xml += """
        <mxCell id="flow-tm-uae" value="Primary" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;strokeColor=#107C41;strokeWidth=3;fontStyle=1;fontSize=11;fontColor=#107C41" edge="1" source="icon-tm-global" target="icon-agw-uae" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="flow-tm-ukc" value="Failover" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;strokeColor=#D83B01;strokeWidth=2;dashed=1;fontStyle=1;fontSize=11;fontColor=#D83B01" edge="1" source="icon-tm-global" target="icon-agw-ukc" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="note-exec" value="&lt;b&gt;Executive Summary &amp; Architecture Decisions&lt;/b&gt;&lt;hr&gt;&lt;ul&gt;&lt;li&gt;&lt;b&gt;Zero-Trust AI:&lt;/b&gt; OpenAI and Search isolated via Private Link.&lt;/li&gt;&lt;li&gt;&lt;b&gt;Regional Resiliency:&lt;/b&gt; UAE North (Primary) with UK Central (Warm DR).&lt;/li&gt;&lt;li&gt;&lt;b&gt;AI Gateway Pattern:&lt;/b&gt; Centralized API Mediation layer for prompt auditing.&lt;/li&gt;&lt;li&gt;&lt;b&gt;Enterprise Scale:&lt;/b&gt; Aligned with Microsoft Cloud Adoption Framework.&lt;/li&gt;&lt;/ul&gt;" style="text;html=1;strokeColor=#D83B01;fillColor=#FFF4CE;align=left;verticalAlign=top;whiteSpace=wrap;rounded=1;spacingLeft=10;spacingRight=10;spacingTop=10;shadow=1" vertex="1" parent="1">
          <mxGeometry x="840" y="-140" width="300" height="200" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""

with open(output_file, "w", encoding="utf-8") as f:
    f.write(xml)

print(f"Diagram successfully regenerated and encoded at {output_file}")
