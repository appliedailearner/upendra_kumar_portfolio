import os
# Add Graphviz to PATH to avoid execution errors
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"

from diagrams import Diagram, Cluster, Edge
from diagrams.azure.network import PrivateEndpoint, VirtualNetworks, DNSPrivateZones, ApplicationGateway
from diagrams.azure.web import AppServices
from diagrams.azure.database import SQLDatabases
from diagrams.azure.integration import APIManagement
from diagrams.azure.compute import FunctionApps
from diagrams.azure.storage import StorageAccounts
from diagrams.onprem.client import Users

# Shared Attributes
graph_attr = {"fontsize": "14", "fontname": "Segoe UI", "pad": "0.5"}
node_attr = {"fontname": "Segoe UI"}
edge_attr = {"fontname": "Segoe UI", "fontsize": "10"}

OUTPUT_DIR = "C:\\MyResumePortfolio\\azurewebapp"

# Scenario 1: Web App + PE
with Diagram("1_Baseline_Private_WebApp", show=False, outformat="png", filename=os.path.join(OUTPUT_DIR, "1_Baseline_Private_WebApp"), graph_attr=graph_attr, node_attr=node_attr, edge_attr=edge_attr):
    client = Users("Internal Client / VPN")
    with Cluster("Virtual Network"):
        pe = PrivateEndpoint("Private Endpoint")
    app = AppServices("App Service (Private)")
    dns = DNSPrivateZones("privatelink...")
    
    client >> Edge(color="darkblue") >> pe >> Edge(color="darkred") >> app
    pe >> Edge(style="dashed", color="gray") >> dns

# Scenario 2: Secure N-Tier Web App
with Diagram("2_Secure_NTier_WebApp", show=False, outformat="png", filename=os.path.join(OUTPUT_DIR, "2_Secure_NTier_WebApp"), graph_attr=graph_attr, node_attr=node_attr, edge_attr=edge_attr):
    public_client = Users("Public Internet")
    with Cluster("Virtual Network"):
        vnet = VirtualNetworks("VNet Subnets")
        fe = AppServices("Frontend App\n(VNet Integrated)")
        pe = PrivateEndpoint("Backend PE")
    be = AppServices("Backend App (Private)")
    
    public_client >> fe >> Edge(color="darkblue") >> vnet >> pe >> Edge(color="darkred") >> be

# Scenario 3: Web App VNet Injection
with Diagram("3_WebApp_VNetInjection_PE", show=False, outformat="png", filename=os.path.join(OUTPUT_DIR, "3_WebApp_VNetInjection_PE"), graph_attr=graph_attr, node_attr=node_attr, edge_attr=edge_attr):
    with Cluster("Virtual Network"):
        vnet = VirtualNetworks("Integration Subnet")
        fe = AppServices("Web App (Outbound)")
        pe = PrivateEndpoint("PE (Inbound Target)")
    target = AppServices("Target Service")
    
    fe >> Edge(color="darkblue") >> vnet >> pe >> Edge(color="darkred") >> target

# Scenario 4: Web App + App GW
with Diagram("4_AppGateway_WebApp_PE", show=False, outformat="png", filename=os.path.join(OUTPUT_DIR, "4_AppGateway_WebApp_PE"), graph_attr=graph_attr, node_attr=node_attr, edge_attr=edge_attr):
    public = Users("Internet User")
    with Cluster("Virtual Network"):
        appgw = ApplicationGateway("App Gateway v2 (WAF)")
        pe = PrivateEndpoint("Private Endpoint")
    app = AppServices("Web App (Private)")
    
    public >> appgw >> Edge(color="darkblue") >> pe >> Edge(color="darkred") >> app

# Scenario 5: SQL over PE
with Diagram("5_SQL_over_PE", show=False, outformat="png", filename=os.path.join(OUTPUT_DIR, "5_SQL_over_PE"), graph_attr=graph_attr, node_attr=node_attr, edge_attr=edge_attr):
    app = AppServices("Web App (VNet Integrated)")
    with Cluster("Virtual Network"):
        vnet = VirtualNetworks("Outbound Subnet")
        pe = PrivateEndpoint("SQL Private Endpoint")
    db = SQLDatabases("Azure SQL Db (Private)")
    
    app >> Edge(color="darkblue") >> vnet >> pe >> Edge(color="darkred") >> db

# Scenario 6: App Gw + Internal APIM
with Diagram("6_GoldStandard_WAF_APIM_WebApp", show=False, outformat="png", filename=os.path.join(OUTPUT_DIR, "6_GoldStandard_WAF_APIM_WebApp"), graph_attr=graph_attr, node_attr=node_attr, edge_attr=edge_attr):
    public = Users("Internet")
    with Cluster("Virtual Network"):
        appgw = ApplicationGateway("App Gateway v2")
        apim = APIManagement("Internal APIM")
        pe = PrivateEndpoint("Private Endpoint")
    app = AppServices("Web App (Private)")
    
    public >> appgw >> Edge(color="darkgreen") >> apim >> Edge(color="darkblue") >> pe >> Edge(color="darkred") >> app

# Bonus: Function App + Storage PE
with Diagram("Bonus_FunctionApp_Storage_PE", show=False, outformat="png", filename=os.path.join(OUTPUT_DIR, "Bonus_FunctionApp_Storage_PE"), graph_attr=graph_attr, node_attr=node_attr, edge_attr=edge_attr):
    func = FunctionApps("Function App\n(VNet Integrated)")
    with Cluster("Virtual Network"):
        pe_blob = PrivateEndpoint("Blob PE")
        pe_queue = PrivateEndpoint("Queue PE")
    storage = StorageAccounts("Secure Storage Account")
    
    func >> Edge(color="darkblue") >> pe_blob >> Edge(color="darkred") >> storage
    func >> Edge(color="darkblue") >> pe_queue >> Edge(color="darkred") >> storage

print("All diagrams generated successfully!")
