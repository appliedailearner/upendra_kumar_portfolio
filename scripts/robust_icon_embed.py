
import os
import base64
import re

# Base paths
icon_root = r"C:\MyResumePortfolio\blog\assets\Azure_Public_Service_Icons\Icons"
diagram_path = r"C:\MyResumePortfolio\docs\Azure_AI_Platform_Architecture.drawio"

# Robust path mapping (Recursive search for the best match)
icon_map = {
    "icon-afw-uae": "10084-icon-service-Firewalls.svg",
    "icon-bastion-uae": "10161-icon-service-Bastions.svg",
    "icon-vpn-uae": "10061-icon-service-Virtual-Network-Gateways.svg",
    "icon-dns-uae": "10118-icon-service-DNS-Zones.svg",
    "icon-afw-ukc": "10084-icon-service-Firewalls.svg",
    "icon-sentinel": "Microsoft Sentinel.svg",
    "icon-defender": "10363-icon-service-Microsoft-Defender-for-Cloud.svg",
    "icon-policy": "10344-icon-service-Policy.svg",
    "icon-agw-uae": "10064-icon-service-Application-Gateways.svg",
    "icon-apim-uae": "10041-icon-service-API-Management-Services.svg",
    "icon-app-uae": "10035-icon-service-App-Services.svg",
    "icon-oai-uae": "Azure OpenAI Service.svg",
    "icon-srch-uae": "10166-icon-service-Search-Services.svg",
    "icon-di-uae": "Document Intelligence.svg",
    "icon-st-uae": "10015-icon-service-Storage-Accounts.svg",
    "icon-agw-ukc": "10064-icon-service-Application-Gateways.svg",
    "icon-app-ukc": "10035-icon-service-App-Services.svg",
    "icon-tm-global": "10065-icon-service-Traffic-Manager-Profiles.svg"
}

def find_icon_path(filename):
    for root, dirs, files in os.walk(icon_root):
        if filename in files:
            return os.path.join(root, filename)
    return None

def get_base64_svg(file_path):
    with open(file_path, "rb") as svg_file:
        encoded_string = base64.b64encode(svg_file.read()).decode('utf-8')
        return f"data:image/svg+xml;base64,{encoded_string}"

with open(diagram_path, 'r', encoding='utf-8') as f:
    xml_content = f.read()

for cell_id, icon_file in icon_map.items():
    full_path = find_icon_path(icon_file)
    if full_path:
        b64_data = get_base64_svg(full_path)
        # Regex to target the style attribute of the cell with this ID
        # We replace the entire style to ensure clarity and standard formatting
        pattern = f'(id="{cell_id}".*?style=")(.*?)(")'
        
        def replace_style(match):
            prefix = match.group(1)
            # Remove any existing shape= or image= to avoid conflicts
            new_style = "image;html=1;labelBackgroundColor=none;align=center;verticalAlign=top;verticalLabelPosition=bottom;image=" + b64_data
            suffix = match.group(3)
            return prefix + new_style + suffix
            
        xml_content = re.sub(pattern, replace_style, xml_content, flags=re.DOTALL)
        print(f"Embedded {icon_file} into {cell_id}")
    else:
        print(f"WARNING: Could not find {icon_file}")

with open(diagram_path, 'w', encoding='utf-8') as f:
    f.write(xml_content)

print("\nSuccess: Diagram updated with self-contained high-fidelity icons.")
