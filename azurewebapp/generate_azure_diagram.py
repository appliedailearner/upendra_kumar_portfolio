import os
# Add Graphviz to PATH to avoid execution errors
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"

from diagrams import Diagram, Cluster, Edge
from diagrams.azure.integration import APIManagement
from diagrams.azure.network import DNSPrivateZones, PrivateEndpoint
from diagrams.azure.web import AppServices
from diagrams.onprem.client import Users

graph_attr = {
    "fontsize": "14",
    "fontname": "Segoe UI",
    "pad": "0.5"
}
node_attr = {
    "fontname": "Segoe UI"
}
edge_attr = {
    "fontname": "Segoe UI",
    "fontsize": "10"
}

with Diagram("ICTSI App Service Private-Only Architecture", show=False, filename="azure_architecture_diagram_official", 
             graph_attr=graph_attr, node_attr=node_attr, edge_attr=edge_attr, outformat="png"):

    client = Users("Users /\nInternet Clients")

    with Cluster("Virtual Network: vnet-ictsi-sea-01"):
        apim = APIManagement("Azure API Management\n(External/Internal VNet Mode)")
        pe = PrivateEndpoint("Azure Private Endpoint\nIP: 10.50.10.x")
        
    with Cluster("Azure PaaS Services (Isolated)"):
        app = AppServices("App Service Web App\nPublic Access: Disabled")

    dns = DNSPrivateZones("Private DNS Zone\nprivatelink.azurewebsites.net")

    # Flow connections
    client >> Edge(color="darkgreen", label="HTTPS Request\n(Public/Internal)") >> apim
    apim >> Edge(color="darkblue", label="Routes to Private IP") >> pe
    pe >> Edge(color="darkred", label="Private Link") >> app
    
    # DNS Resolution
    apim >> Edge(color="gray", style="dashed", label="Resolves Backend Name") >> dns
    dns >> Edge(color="gray", style="dashed", label="Returns 10.50.10.x") >> apim
