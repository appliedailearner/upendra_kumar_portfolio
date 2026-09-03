import os

def create_xml(content):
    return f"""<mxfile host="Electron" modified="2026-04-18T00:00:00.000Z" agent="Mozilla/5.0" version="24.4.0" type="device">
  <diagram id="Exec_Diagram" name="Architecture">
    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="900" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
{content}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""

def write_exec_diagram():
    # Styles
    s_blue = "rounded=1;fillColor=#0078D4;fontColor=#FFFFFF;strokeColor=none;html=1;whiteSpace=wrap;"
    s_light_blue = "rounded=1;fillColor=#E1F0F9;fontColor=#000000;strokeColor=#0078D4;html=1;whiteSpace=wrap;"
    s_grey = "rounded=1;fillColor=#F3F2F1;fontColor=#000000;strokeColor=#C8C6C4;html=1;whiteSpace=wrap;"
    
    s_uae_swimlane = "swimlane;horizontal=1;startSize=40;fillColor=#F3F2F1;strokeColor=#C8C6C4;fontColor=#333333;fontStyle=1;html=1;"
    s_swe_swimlane = "swimlane;horizontal=1;startSize=40;fillColor=#E8F4F8;strokeColor=#B1D6E8;fontColor=#333333;fontStyle=1;html=1;"
    
    s_edge_data = "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor=#0078D4;strokeWidth=2;"
    s_edge_control = "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor=#717171;strokeWidth=2;dashed=1;dashPattern=1 2;"
    
    xml = []
    
    # Global
    xml.append(f'<mxCell id="clients" value="&lt;b&gt;Clients / Apps&lt;/b&gt;" style="{s_grey}" vertex="1" parent="1"><mxGeometry x="100" y="40" width="140" height="60" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="afd" value="&lt;b&gt;Azure Front Door&lt;/b&gt;&lt;br&gt;Global Access" style="{s_blue}" vertex="1" parent="1"><mxGeometry x="400" y="40" width="180" height="60" as="geometry"/></mxCell>')
    
    # Edges global
    xml.append(f'<mxCell id="e_c_afd" edge="1" parent="1" source="clients" target="afd" style="{s_edge_data}"><mxGeometry relative="1" as="geometry"/></mxCell>')

    # UAE North Swimlane
    xml.append(f'<mxCell id="uae" value="Primary Region: UAE North" style="{s_uae_swimlane}" vertex="1" parent="1"><mxGeometry x="40" y="180" width="480" height="500" as="geometry"/></mxCell>')
    
    # Hub/Spoke inside UAE
    xml.append(f'<mxCell id="uae_appgw" value="&lt;b&gt;App Gateway (WAF)&lt;/b&gt;&lt;br&gt;Regional Ingress" style="{s_blue}" vertex="1" parent="uae"><mxGeometry x="40" y="60" width="160" height="60" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="uae_apim" value="&lt;b&gt;Azure API Management&lt;/b&gt;&lt;br&gt;Standard v2" style="{s_blue}" vertex="1" parent="uae"><mxGeometry x="260" y="60" width="180" height="60" as="geometry"/></mxCell>')
    
    # AI Services container (Swimlane inside swimlane uses generic startSize)
    xml.append(f'<mxCell id="uae_ai" value="Predeployed Regional AI Services" style="swimlane;startSize=30;fillColor=#FFFFFF;strokeColor=#C8C6C4;html=1;" vertex="1" parent="uae"><mxGeometry x="40" y="160" width="400" height="280" as="geometry"/></mxCell>')
    
    xml.append(f'<mxCell id="uae_search" value="&lt;b&gt;Azure AI Search&lt;/b&gt;" style="{s_light_blue}" vertex="1" parent="uae_ai"><mxGeometry x="20" y="60" width="150" height="60" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="uae_openai" value="&lt;b&gt;Azure OpenAI&lt;/b&gt;" style="{s_light_blue}" vertex="1" parent="uae_ai"><mxGeometry x="210" y="60" width="150" height="60" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="uae_doc" value="&lt;b&gt;Document Intel&lt;/b&gt;" style="{s_light_blue}" vertex="1" parent="uae_ai"><mxGeometry x="20" y="160" width="150" height="60" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="uae_foundry" value="&lt;b&gt;AI Foundry&lt;/b&gt;" style="{s_light_blue}" vertex="1" parent="uae_ai"><mxGeometry x="210" y="160" width="150" height="60" as="geometry"/></mxCell>')
    
    # Sweden Central Swimlane
    xml.append(f'<mxCell id="swe" value="DR Region: Sweden Central (Standby)" style="{s_swe_swimlane}" vertex="1" parent="1"><mxGeometry x="580" y="180" width="480" height="500" as="geometry"/></mxCell>')
    
    xml.append(f'<mxCell id="swe_appgw" value="&lt;b&gt;App Gateway (WAF)&lt;/b&gt;&lt;br&gt;Standby Ingress" style="{s_blue}" vertex="1" parent="swe"><mxGeometry x="40" y="60" width="160" height="60" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="swe_apim" value="&lt;b&gt;Azure API Management&lt;/b&gt;&lt;br&gt;Standard v2 (Twin)" style="{s_blue}" vertex="1" parent="swe"><mxGeometry x="260" y="60" width="180" height="60" as="geometry"/></mxCell>')
    
    xml.append(f'<mxCell id="swe_ai" value="Predeployed Regional AI Services" style="swimlane;startSize=30;fillColor=#FFFFFF;strokeColor=#B1D6E8;html=1;" vertex="1" parent="swe"><mxGeometry x="40" y="160" width="400" height="280" as="geometry"/></mxCell>')
    
    xml.append(f'<mxCell id="swe_search" value="&lt;b&gt;Azure AI Search&lt;/b&gt;" style="{s_light_blue}" vertex="1" parent="swe_ai"><mxGeometry x="20" y="60" width="150" height="60" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="swe_openai" value="&lt;b&gt;Azure OpenAI&lt;/b&gt;" style="{s_light_blue}" vertex="1" parent="swe_ai"><mxGeometry x="210" y="60" width="150" height="60" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="swe_doc" value="&lt;b&gt;Document Intel&lt;/b&gt;" style="{s_light_blue}" vertex="1" parent="swe_ai"><mxGeometry x="20" y="160" width="150" height="60" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="swe_foundry" value="&lt;b&gt;AI Foundry&lt;/b&gt;" style="{s_light_blue}" vertex="1" parent="swe_ai"><mxGeometry x="210" y="160" width="150" height="60" as="geometry"/></mxCell>')
    
    # Internal Edges UAE
    xml.append(f'<mxCell id="e_uag_apim" edge="1" parent="uae" source="uae_appgw" target="uae_apim" style="{s_edge_data}"><mxGeometry relative="1" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="e_apim_uai1" edge="1" parent="uae" source="uae_apim" target="uae_search" style="{s_edge_data}"><mxGeometry relative="1" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="e_apim_uai2" edge="1" parent="uae" source="uae_apim" target="uae_openai" style="{s_edge_data}"><mxGeometry relative="1" as="geometry"/></mxCell>')
    
    # Internal Edges SWE
    xml.append(f'<mxCell id="e_swe_apim" edge="1" parent="swe" source="swe_appgw" target="swe_apim" style="{s_edge_data}"><mxGeometry relative="1" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="e_apim_sai1" edge="1" parent="swe" source="swe_apim" target="swe_search" style="{s_edge_data}"><mxGeometry relative="1" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="e_apim_sai2" edge="1" parent="swe" source="swe_apim" target="swe_openai" style="{s_edge_data}"><mxGeometry relative="1" as="geometry"/></mxCell>')
    
    # Global Edges
    xml.append(f'<mxCell id="e_afd_uae" value="Priority 1" edge="1" parent="1" source="afd" target="uae_appgw" style="{s_edge_data}"><mxGeometry relative="1" as="geometry" y="10"/></mxCell>')
    xml.append(f'<mxCell id="e_afd_swe" value="Priority 2 (Health Probe Only in Steady)" edge="1" parent="1" source="afd" target="swe_appgw" style="{s_edge_control}"><mxGeometry relative="1" as="geometry" y="-10"/></mxCell>')
    xml.append(f'<mxCell id="e_sync1" value="APIOps / IaC Sync" edge="1" parent="1" source="uae_apim" target="swe_apim" style="{s_edge_control}"><mxGeometry relative="1" as="geometry" y="-10"/></mxCell>')
    xml.append(f'<mxCell id="e_sync2" value="Index &amp; Content Sync" edge="1" parent="1" source="uae_search" target="swe_search" style="{s_edge_control}"><mxGeometry relative="1" as="geometry" y="-10"/></mxCell>')

    with open('C:\\MyResumePortfolio\\blog\\Azure APIM and AI DR\\azure_dr_exec_architecture_final.drawio', 'w', encoding='utf-8') as f:
        f.write(create_xml("\n".join(xml)))


def write_landing_zone_diagram():
    # Same styles
    s_blue = "rounded=1;fillColor=#0078D4;fontColor=#FFFFFF;strokeColor=none;html=1;whiteSpace=wrap;"
    s_light_blue = "rounded=1;fillColor=#E1F0F9;fontColor=#000000;strokeColor=#0078D4;html=1;whiteSpace=wrap;"
    s_grey = "rounded=1;fillColor=#F3F2F1;fontColor=#000000;strokeColor=#C8C6C4;html=1;whiteSpace=wrap;"
    s_edge_data = "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor=#0078D4;strokeWidth=2;"
    s_edge_control = "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor=#717171;strokeWidth=2;dashed=1;dashPattern=1 2;"
    
    xml = []
    
    xml.append(f'<mxCell id="clients" value="&lt;b&gt;Clients / Apps&lt;/b&gt;" style="{s_grey}" vertex="1" parent="1"><mxGeometry x="100" y="40" width="140" height="60" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="afd" value="&lt;b&gt;Azure Front Door&lt;/b&gt;" style="{s_blue}" vertex="1" parent="1"><mxGeometry x="400" y="40" width="180" height="60" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="e_c_afd" edge="1" parent="1" source="clients" target="afd" style="{s_edge_data}"><mxGeometry relative="1" as="geometry"/></mxCell>')

    # UAE Region
    xml.append(f'<mxCell id="uae" value="Primary Region: UAE North" style="swimlane;horizontal=1;startSize=40;fillColor=#F3F2F1;strokeColor=#C8C6C4;fontColor=#333333;fontStyle=1;html=1;" vertex="1" parent="1"><mxGeometry x="40" y="180" width="600" height="600" as="geometry"/></mxCell>')
    
    # Hub
    xml.append(f'<mxCell id="u_hub" value="Platform Hub VNet" style="swimlane;startSize=30;fillColor=#FFFFFF;strokeColor=#C8C6C4;html=1;" vertex="1" parent="uae"><mxGeometry x="20" y="60" width="180" height="400" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="u_fw" value="Azure Firewall&lt;br&gt;(Secured Egress)" style="{s_light_blue}" vertex="1" parent="u_hub"><mxGeometry x="20" y="60" width="140" height="60" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="u_pdns" value="Private DNS Zones" style="{s_light_blue}" vertex="1" parent="u_hub"><mxGeometry x="20" y="160" width="140" height="60" as="geometry"/></mxCell>')
    
    # Spoke
    xml.append(f'<mxCell id="u_spoke" value="Application Spoke VNet" style="swimlane;startSize=30;fillColor=#FFFFFF;strokeColor=#C8C6C4;html=1;" vertex="1" parent="uae"><mxGeometry x="220" y="60" width="360" height="500" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="u_appgw" value="&lt;b&gt;App Gateway (WAF)&lt;/b&gt;" style="{s_blue}" vertex="1" parent="u_spoke"><mxGeometry x="20" y="60" width="140" height="60" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="u_apim" value="&lt;b&gt;Azure APIM&lt;/b&gt;" style="{s_blue}" vertex="1" parent="u_spoke"><mxGeometry x="200" y="60" width="140" height="60" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="u_pe" value="AI Services Private Endpoints" style="{s_grey}" vertex="1" parent="u_spoke"><mxGeometry x="20" y="180" width="320" height="60" as="geometry"/></mxCell>')

    xml.append(f'<mxCell id="u_search" value="&lt;b&gt;Azure AI Search&lt;/b&gt;" style="{s_light_blue}" vertex="1" parent="u_spoke"><mxGeometry x="20" y="280" width="140" height="60" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="u_openai" value="&lt;b&gt;Azure OpenAI&lt;/b&gt;" style="{s_light_blue}" vertex="1" parent="u_spoke"><mxGeometry x="200" y="280" width="140" height="60" as="geometry"/></mxCell>')

    xml.append(f'<mxCell id="e_uag_uap" edge="1" parent="u_spoke" source="u_appgw" target="u_apim" style="{s_edge_data}"><mxGeometry relative="1" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="e_uap_pe" edge="1" parent="u_spoke" source="u_apim" target="u_pe" style="{s_edge_data}"><mxGeometry relative="1" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="e_pe_search" edge="1" parent="u_spoke" source="u_pe" target="u_search" style="{s_edge_data}"><mxGeometry relative="1" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="e_pe_oai" edge="1" parent="u_spoke" source="u_pe" target="u_openai" style="{s_edge_data}"><mxGeometry relative="1" as="geometry"/></mxCell>')

    # Sweden Region
    xml.append(f'<mxCell id="swe" value="DR Region: Sweden Central" style="swimlane;horizontal=1;startSize=40;fillColor=#E8F4F8;strokeColor=#B1D6E8;fontColor=#333333;fontStyle=1;html=1;" vertex="1" parent="1"><mxGeometry x="700" y="180" width="600" height="600" as="geometry"/></mxCell>')
    
    xml.append(f'<mxCell id="s_hub" value="Platform Hub VNet" style="swimlane;startSize=30;fillColor=#FFFFFF;strokeColor=#B1D6E8;html=1;" vertex="1" parent="swe"><mxGeometry x="20" y="60" width="180" height="400" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="s_fw" value="Azure Firewall" style="{s_light_blue}" vertex="1" parent="s_hub"><mxGeometry x="20" y="60" width="140" height="60" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="s_pdns" value="Private DNS Zones" style="{s_light_blue}" vertex="1" parent="s_hub"><mxGeometry x="20" y="160" width="140" height="60" as="geometry"/></mxCell>')
    
    xml.append(f'<mxCell id="s_spoke" value="Application Spoke VNet" style="swimlane;startSize=30;fillColor=#FFFFFF;strokeColor=#B1D6E8;html=1;" vertex="1" parent="swe"><mxGeometry x="220" y="60" width="360" height="500" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="s_appgw" value="&lt;b&gt;App Gateway (WAF)&lt;/b&gt;" style="{s_blue}" vertex="1" parent="s_spoke"><mxGeometry x="20" y="60" width="140" height="60" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="s_apim" value="&lt;b&gt;Azure APIM&lt;/b&gt;" style="{s_blue}" vertex="1" parent="s_spoke"><mxGeometry x="200" y="60" width="140" height="60" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="s_pe" value="AI Services Private Endpoints" style="{s_grey}" vertex="1" parent="s_spoke"><mxGeometry x="20" y="180" width="320" height="60" as="geometry"/></mxCell>')

    xml.append(f'<mxCell id="s_search" value="&lt;b&gt;Azure AI Search&lt;/b&gt;" style="{s_light_blue}" vertex="1" parent="s_spoke"><mxGeometry x="20" y="280" width="140" height="60" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="s_openai" value="&lt;b&gt;Azure OpenAI&lt;/b&gt;" style="{s_light_blue}" vertex="1" parent="s_spoke"><mxGeometry x="200" y="280" width="140" height="60" as="geometry"/></mxCell>')

    xml.append(f'<mxCell id="e_sag_sap" edge="1" parent="s_spoke" source="s_appgw" target="s_apim" style="{s_edge_data}"><mxGeometry relative="1" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="e_sap_pe" edge="1" parent="s_spoke" source="s_apim" target="s_pe" style="{s_edge_data}"><mxGeometry relative="1" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="e_spe_search" edge="1" parent="s_spoke" source="s_pe" target="s_search" style="{s_edge_data}"><mxGeometry relative="1" as="geometry"/></mxCell>')
    xml.append(f'<mxCell id="e_spe_oai" edge="1" parent="s_spoke" source="s_pe" target="s_openai" style="{s_edge_data}"><mxGeometry relative="1" as="geometry"/></mxCell>')

    # Global Edges
    xml.append(f'<mxCell id="e_afd_uag" value="Active Path" edge="1" parent="1" source="afd" target="u_appgw" style="{s_edge_data}"><mxGeometry relative="1" as="geometry" y="10"/></mxCell>')
    xml.append(f'<mxCell id="e_afd_sag" value="Standby Probe Path" edge="1" parent="1" source="afd" target="s_appgw" style="{s_edge_control}"><mxGeometry relative="1" as="geometry" y="-10"/></mxCell>')
    
    with open('C:\\MyResumePortfolio\\blog\\Azure APIM and AI DR\\azure_dr_landing_zone_technical_view_final.drawio', 'w', encoding='utf-8') as f:
        f.write(create_xml("\n".join(xml)))


def write_failover_diagram():
    s_blue = "rounded=1;fillColor=#0078D4;fontColor=#FFFFFF;strokeColor=none;html=1;whiteSpace=wrap;"
    s_grey = "rounded=1;fillColor=#F3F2F1;fontColor=#000000;strokeColor=#C8C6C4;html=1;whiteSpace=wrap;"
    s_edge_data = "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor=#0078D4;strokeWidth=2;"
    
    xml = []
    
    steps = [
        "1. Detect Failure\\nFront Door health probes fail on UAE North. Regional ingress is marked unhealthy.",
        "2. Stop Primary Routing\\nFront Door stops sending requests to UAE North. Public DNS stays same.",
        "3. Promote DR Ingress\\nTraffic routed to Sweden Central App Gateway organically. No client change.",
        "4. Use DR APIM\\nSweden Central APIM takes traffic using aligned APIOps/IaC policies.",
        "5. Call Regional AI\\nDR APIM routes to pre-deployed Sweden Central OpenAI and Search via Private Endpoints.",
        "6. Validate Business Readiness\\nOperations validates Search index freshness and model reachability.",
        "7. Controlled Failback\\nManual fallback to UAE North only after resolution and sync."
    ]
    
    for i, step in enumerate(steps):
        row = i // 3
        col = i % 3
        x = 40 + (col * 300)
        y = 40 + (row * 160)
        
        # We add the node
        xml.append(f'<mxCell id="s{i}" value="&lt;div style=&quot;text-align:left;padding:10px;&quot;&gt;{step}&lt;/div&gt;" style="{s_grey}" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="260" height="100" as="geometry"/></mxCell>')
        
        # Connect to previous if not first
        if i > 0:
            # If same row, orthogonal left to right. If new row, orthogonal down from last of previous row.
            xml.append(f'<mxCell id="e_s{i-1}_s{i}" edge="1" parent="1" source="s{i-1}" target="s{i}" style="{s_edge_data}"><mxGeometry relative="1" as="geometry"/></mxCell>')

    with open('C:\\MyResumePortfolio\\blog\\Azure APIM and AI DR\\azure_dr_failover_sequence_final.drawio', 'w', encoding='utf-8') as f:
        f.write(create_xml("\n".join(xml)))

if __name__ == "__main__":
    write_exec_diagram()
    write_landing_zone_diagram()
    write_failover_diagram()
    print("Successfully generated all .drawio artifacts.")
