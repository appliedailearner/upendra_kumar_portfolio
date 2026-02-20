from diagrams import Diagram, Cluster, Edge
from diagrams.azure.network import Firewall, VirtualNetworkGateways, Subnets
from diagrams.azure.general import Managementgroups

graph_attr = {
    "bgcolor": "transparent",
    "pad": "0.5",
    "fontcolor": "#e2e8f0",
    "fontname": "Outfit",
    "fontsize": "16"
}
cluster_attr = {
    "bgcolor": "transparent",
    "fontcolor": "#e2e8f0",
    "pencolor": "#334155",
}

with Diagram("The Trap: Broken Logic", show=False, filename="c:/MyResumePortfolio/images/blog/diagram-trap", direction="TB", graph_attr=graph_attr):
    with Cluster("Azure Environment", graph_attr=cluster_attr):
        fw = Firewall("Azure Firewall")
    
    with Cluster("On-Prem", graph_attr=cluster_attr):
        onprem = VirtualNetworkGateways("On-Prem Gateway")
    
    ms = Managementgroups("Microsoft Control Plane")

    fw >> Edge(label=" 0.0.0.0/0 (Forced)", color="#ef4444", fontcolor="#e2e8f0") >> onprem
    onprem >> Edge(label=" Management Traffic Blocked", style="dashed", color="#ef4444", fontcolor="#e2e8f0") >> ms

with Diagram("The Fix: Split Planes", show=False, filename="c:/MyResumePortfolio/images/blog/diagram-fix", direction="TB", graph_attr=graph_attr):
    with Cluster("Azure Environment", graph_attr=cluster_attr):
        with Cluster("Azure Firewall", graph_attr={"bgcolor": "transparent", "style": "dashed", "color": "#10b981", "fontcolor": "#e2e8f0", "pencolor": "#10b981"}):
            data = Subnets("AzureFirewallSubnet\n(Data Plane)")
            mgmt = Subnets("AzureFirewallManagementSubnet\n(Mgmt Plane)")

    with Cluster("On-Prem", graph_attr=cluster_attr):
        onprem = VirtualNetworkGateways("On-Prem Gateway")
        
    ms = Managementgroups("Microsoft Control Plane")

    data >> Edge(label=" 0.0.0.0/0 (Forced)", fontcolor="#e2e8f0") >> onprem
    mgmt >> Edge(label=" Direct Internet", color="#10b981", fontcolor="#e2e8f0") >> ms
