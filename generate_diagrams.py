import os
from diagrams import Diagram, Cluster, Edge
from diagrams.azure.network import Firewall, VirtualNetworks, NetworkSecurityGroupsClassic
from diagrams.azure.database import SQLDatabases
from diagrams.azure.compute import VMWindows
from diagrams.onprem.client import Users, Client
from diagrams.onprem.network import Internet

os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"
dir_path = r"C:\Users\upend\.gemini\antigravity\brain\f8cf40ca-8d39-4eae-a103-d569d17b22d2"

with Diagram("1. Access Control (VIP Pass)", show=False, filename=os.path.join(dir_path, "access_control_pro"), direction="LR"):
    with Cluster("Ingress Sources"):
        devs = Users("Remote Developers")
        partners = Users("Partner Vendors")
        qa = Users("QA Team")

    with Cluster("Azure Security Perimeter"):
        fw = Firewall("Azure Firewall")
        
        with Cluster("Azure IP Groups"):
            ig1 = NetworkSecurityGroupsClassic("IP Group:\nVIP-Devs")
            ig2 = NetworkSecurityGroupsClassic("IP Group:\nTrusted-Vendors")
            ig3 = NetworkSecurityGroupsClassic("IP Group:\nUAT-Testers")
        
        devs >> Edge(label="Matches") >> ig1 >> Edge(color="darkgreen", label="Allow") >> fw
        partners >> Edge(label="Matches") >> ig2 >> Edge(color="darkgreen", label="Allow") >> fw
        qa >> Edge(label="Matches") >> ig3 >> Edge(color="darkgreen", label="Allow") >> fw

    with Cluster("Internal Assets"):
        prod = SQLDatabases("Production DB")
        api = VMWindows("Partner API")
        test = VirtualNetworks("Staging Env")

    fw >> prod
    fw >> api
    fw >> test

with Diagram("2. Security & Quarantine", show=False, filename=os.path.join(dir_path, "security_quarantine_pro"), direction="LR"):
    with Cluster("Threat Landscape & Updates"):
        hackers = Internet("Malicious Botnets")
        sick = VMWindows("Quarantined VMs")
        updates = VMWindows("Approved Patch Server")

    with Cluster("Azure Firewall Policies"):
        fw = Firewall("Azure Firewall")
        
        with Cluster("IP Groups Config"):
            ig_bad = NetworkSecurityGroupsClassic("IP Group: Threat-Intel")
            ig_sick = NetworkSecurityGroupsClassic("IP Group: Containment")
            ig_update = NetworkSecurityGroupsClassic("IP Group: Patch-Servers")
            
        hackers >> ig_bad >> Edge(color="darkred", label="100: DROP") >> fw
        sick >> ig_sick >> Edge(color="darkred", label="101: BLOCK OUTBOUND") >> fw
        fw >> Edge(color="darkgreen", label="200: ALLOW TO") >> ig_update
        ig_update >> updates
        
    with Cluster("Secure Zones"):
        internal = VirtualNetworks("Internal Network")
        internet = Internet("The Public Internet")
        
    fw >> Edge(color="darkred", style="dashed", label="Dropped") >> internal
    fw >> Edge(color="darkred", style="dashed", label="Blocked") >> internet

with Diagram("3. Routing & Migration Sync", show=False, filename=os.path.join(dir_path, "routing_migration_pro"), direction="TB"):
    with Cluster("Azure Resource Manager (Hub)"):
        with Cluster("Central IP Groups"):
            ig_merge = NetworkSecurityGroupsClassic("IP Group:\nNew-Subsidiary")
            ig_migrate = NetworkSecurityGroupsClassic("IP Group:\nCloud-Migrated")
            ig_hq = NetworkSecurityGroupsClassic("IP Group:\nGlobal-Branches")

    with Cluster("Global Azure Firewalls"):
        fw_east = Firewall("East US")
        fw_west = Firewall("West Europe")
        fw_asia = Firewall("Japan East")
        
    sync_edge = Edge(color="purple", style="dotted")
    
    ig_merge >> sync_edge >> fw_east
    ig_merge >> sync_edge >> fw_west
    ig_merge >> sync_edge >> fw_asia
    
    ig_migrate >> sync_edge >> fw_east
    ig_migrate >> sync_edge >> fw_west
    ig_migrate >> sync_edge >> fw_asia
    
    with Cluster("Regional Workloads"):
        vnet1 = VirtualNetworks("App VNet America")
        vnet2 = VirtualNetworks("App VNet Europe")
        
    fw_east >> vnet1
    fw_west >> vnet2
    fw_asia >> Edge(style="dashed", label="Backup Path") >> vnet1

with Diagram("Core Routing Architecture", show=False, filename=os.path.join(dir_path, "core_routing_pro"), direction="TB"):
    with Cluster("Azure Virtual Network"):
        app_subnet = VirtualNetworks("App Subnet\n(RT-Performance-Bypass)")

        with Cluster("Forced Tunnel Path (Latency)"):
            er_vpn = Firewall("ExpressRoute / VPN Gateway")
            on_prem_fw = Firewall("On-Premises DMZ Firewall")
            
        with Cluster("Microsoft Backbone (Speed)"):
            azure_cloud = VirtualNetworks("AzureCloud\n(Service Tag)")
            azure_sql = SQLDatabases("Azure SQL\n(Service Tag)")

    app_subnet >> Edge(color="darkred", style="dashed", label="0.0.0.0/0 All Other Traffic\n(Backhauled / High Latency)") >> er_vpn
    er_vpn >> Edge(color="darkred", style="dashed", label="BGP Route") >> on_prem_fw

    app_subnet >> Edge(color="darkgreen", label="UDR Bypass\n(Direct / Low Latency)") >> azure_cloud
    app_subnet >> Edge(color="darkgreen", label="UDR Bypass\n(Direct / Low Latency)") >> azure_sql
