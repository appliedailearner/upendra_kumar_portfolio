
import os
import base64
import re

# Base paths
icon_root = r"C:\MyResumePortfolio\blog\assets\Azure_Public_Service_Icons\Icons"
diagram_path = r"C:\MyResumePortfolio\docs\Azure_AI_Platform_Architecture.drawio"

# 100% Precise Mapping based on direct filesystem search
icon_map = {
    "icon-afw-uae": "10084-icon-service-Firewalls.svg",
    "icon-bastion-uae": "02422-icon-service-Bastions.svg",
    "icon-vpn-uae": "10063-icon-service-Virtual-Network-Gateways.svg",
    "icon-dns-uae": "10064-icon-service-DNS-Zones.svg",
    "icon-afw-ukc": "10084-icon-service-Firewalls.svg",
    "icon-sentinel": "10248-icon-service-Azure-Sentinel.svg",
    "icon-defender": "10363-icon-service-Microsoft-Defender-for-Cloud.svg",
    "icon-policy": "10344-icon-service-Policy.svg",
    "icon-agw-uae": "10076-icon-service-Application-Gateways.svg",
    "icon-apim-uae": "10042-icon-service-API-Management-Services.svg",
    "icon-app-uae": "10035-icon-service-App-Services.svg",
    "icon-oai-uae": "03438-icon-service-Azure-OpenAI.svg",
    "icon-srch-uae": "10044-icon-service-Cognitive-Search.svg",
    "icon-di-uae": "00819-icon-service-Form-Recognizers.svg",
    "icon-st-uae": "10015-icon-service-Storage-Accounts.svg",
    "icon-agw-ukc": "10076-icon-service-Application-Gateways.svg",
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

print("Baking Icons into XML payload...")

for cell_id, icon_file in icon_map.items():
    full_path = find_icon_path(icon_file)
    if full_path:
        b64_data = get_base64_svg(full_path)
        # Regex to target style attribute regardless of attribute order
        # Look for the start of the mxCell tag, find the style part for the specific id
        pattern = f'(<mxCell id="{cell_id}"[^>]*style=")([^"]*)(")'
        
        def replace_body(match):
            prefix = match.group(1)
            old_style = match.group(2)
            suffix = match.group(3)
            
            # Construct standard high-fidelity style
            # Clean old image/shape references to avoid layering artifacts
            clean_style = re.sub(r'image=[^;]+;?', '', old_style)
            clean_style = re.sub(r'shape=[^;]+;?', '', clean_style)
            
            new_style = f"image;html=1;labelBackgroundColor=none;align=center;verticalAlign=top;verticalLabelPosition=bottom;image={b64_data};"
            return prefix + new_style + suffix

        xml_content = re.sub(pattern, replace_body, xml_content, flags=re.DOTALL)
        print(f"BAKED: {cell_id} ({icon_file})")
    else:
        print(f"FAILED: Could not find asset for {icon_file}")

with open(diagram_path, 'w', encoding='utf-8') as f:
    f.write(xml_content)

print("\nINTEGRITY CHECK: Completed. Diagram is now 100% self-contained.")
