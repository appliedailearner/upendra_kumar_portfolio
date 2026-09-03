
import os
import re

output_file = "C:/MyResumePortfolio/docs/Azure_AI_Platform_Architecture.drawio"

# Mapping IDs to mxgraph.azure stencil names
stencil_map = {
    "icon-afw-uae": "mxgraph.azure.firewall",
    "icon-bastion-uae": "mxgraph.azure.bastion",
    "icon-vpn-uae": "mxgraph.azure.virtual_network_gateways",
    "icon-dns-uae": "mxgraph.azure.dns",
    "icon-afw-ukc": "mxgraph.azure.firewall",
    "icon-sentinel": "mxgraph.azure.sentinel",
    "icon-defender": "mxgraph.azure.security_center",
    "icon-policy": "mxgraph.azure.policy",
    "icon-agw-uae": "mxgraph.azure.application_gateway",
    "icon-apim-uae": "mxgraph.azure.api_management",
    "icon-app-uae": "mxgraph.azure.app_service",
    "icon-oai-uae": "mxgraph.azure.cognitive_services",
    "icon-srch-uae": "mxgraph.azure.search",
    "icon-di-uae": "mxgraph.azure.form_recognizer",
    "icon-st-uae": "mxgraph.azure.storage_account",
    "icon-agw-ukc": "mxgraph.azure.application_gateway",
    "icon-app-ukc": "mxgraph.azure.app_service",
    "icon-tm-global": "mxgraph.azure.traffic_manager"
}

with open(output_file, 'r', encoding='utf-8') as f:
    xml_content = f.read()

for cell_id, stencil in stencil_map.items():
    # Use a more aggressive regex to replace the entire style attribute
    pattern = f'(id="{cell_id}".*?style=")(.*?)(")'
    
    def replace_style(match):
        prefix = match.group(1)
        suffix = match.group(3)
        # Standard stencil style
        new_style = f"shape={stencil};html=1;fillColor=#0072C6;strokeColor=none;verticalLabelPosition=bottom;verticalAlign=top;align=center;"
        return prefix + new_style + suffix

    xml_content = re.sub(pattern, replace_style, xml_content, flags=re.DOTALL)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(xml_content)

print(f"Diagram successfully migrated to mxgraph.azure stencils at {output_file}")
