
import base64
import os
import re

# Define the icons to embed and their local paths
icons = {
    "icon-afw-uae": "networking/10084-icon-service-Firewalls.svg",
    "icon-bastion-uae": "networking/02422-icon-service-Bastions.svg",
    "icon-vpn-uae": "networking/10063-icon-service-Virtual-Network-Gateways.svg",
    "icon-dns-uae": "networking/02882-icon-service-DNS-Private-Resolver.svg",
    "icon-afw-ukc": "networking/10084-icon-service-Firewalls.svg",
    "icon-sentinel": "security/10248-icon-service-Azure-Sentinel.svg",
    "icon-defender": "security/10241-icon-service-Microsoft-Defender-for-Cloud.svg",
    "icon-policy": "management + governance/10316-icon-service-Policy.svg",
    "icon-agw-uae": "networking/10076-icon-service-Application-Gateways.svg",
    "icon-apim-uae": "ai + machine learning/03173-icon-service-Cognitive-Services-Decisions.svg",
    "icon-app-uae": "app services/10035-icon-service-App-Services.svg",
    "icon-oai-uae": "ai + machine learning/03438-icon-service-Azure-OpenAI.svg",
    "icon-srch-uae": "ai + machine learning/03321-icon-service-Serverless-Search.svg",
    "icon-di-uae": "ai + machine learning/00819-icon-service-Form-Recognizers.svg",
    "icon-st-uae": "storage/10086-icon-service-Storage-Accounts.svg",
    "icon-agw-ukc": "networking/10076-icon-service-Application-Gateways.svg",
    "icon-app-ukc": "app services/10035-icon-service-App-Services.svg",
    "icon-tm-global": "networking/10065-icon-service-Traffic-Manager-Profiles.svg"
}

base_path = "C:/MyResumePortfolio/blog/assets/Azure_Public_Service_Icons/Icons/"
xml_file = "C:/MyResumePortfolio/docs/Azure_AI_Platform_Architecture.drawio"

with open(xml_file, 'r', encoding='utf-8') as f:
    xml_content = f.read()

for cell_id, icon_rel_path in icons.items():
    full_path = os.path.join(base_path, icon_rel_path)
    if os.path.exists(full_path):
        with open(full_path, 'rb') as f:
            svg_data = f.read()
            encoded = base64.b64encode(svg_data).decode('utf-8')
            data_uri = f"data:image/svg+xml;base64,{encoded}"
            
            # Find the line with the specific cell_id and replace the style completely to be robust
            # We look for <mxCell id="ID" ... style="STYLE"
            # And replace the style contents including the image part
            pattern = f'(id="{cell_id}".*?style=")(.*?)(")'
            
            def replace_style(match):
                prefix = match.group(1)
                old_style = match.group(2)
                suffix = match.group(3)
                
                # Create a clean reliable style for embedded images
                new_style = "shape=image;verticalLabelPosition=bottom;verticalAlign=top;imageAspect=0;aspect=fixed;image=" + data_uri
                return prefix + new_style + suffix

            xml_content = re.sub(pattern, replace_style, xml_content, flags=re.DOTALL)
            print(f"Embedded {cell_id} successfully.")
    else:
        print(f"WARNING: Icon file not found: {full_path}")

with open(xml_file, 'w', encoding='utf-8') as f:
    f.write(xml_content)

print("Diagram upgrade complete.")
