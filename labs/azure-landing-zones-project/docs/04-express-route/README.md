# ExpressRoute - Complete Documentation Package

**Project**: Azure Landing Zones - Financial Services  
**Component**: ExpressRoute Connectivity  
**Version**: 1.0.0  
**Last Updated**: December 2025

---

## 1. Design Decisions & Architecture

### ExpressRoute Configuration

**Circuit Details**:
- **Provider**: Equinix / Megaport
- **Peering Location**: Washington DC
- **Bandwidth**: 10 Gbps
- **SKU**: Premium (global connectivity)
- **Redundancy**: Dual circuits for high availability

**Connectivity Model**:
```
On-Premises Data Center
    ├── Primary Circuit (10 Gbps) → Equinix DC1
    └── Secondary Circuit (10 Gbps) → Equinix DC2
         ↓
    Azure ExpressRoute Gateway (ErGw3AZ)
         ↓
    Hub VNet (10.0.0.0/16)
         ├── AI Spoke VNet
         ├── AVD Spoke VNet
         └── APIM Spoke VNet
```

---

## 2. Network Design

### BGP Configuration

**Primary Circuit**:
- **ASN (Azure)**: 12076
- **ASN (On-Premises)**: 65001
- **Primary Subnet**: 192.168.1.0/30
- **Secondary Subnet**: 192.168.1.4/30
- **VLAN ID**: 100

**Route Advertisement**:
- On-Premises to Azure: 172.16.0.0/12 (corporate network)
- Azure to On-Premises: 10.0.0.0/8 (Azure VNets)

**BGP Peering**:
```
Primary Link:
- Azure Router: 192.168.1.1
- Customer Router: 192.168.1.2

Secondary Link:
- Azure Router: 192.168.1.5
- Customer Router: 192.168.1.6
```

### ExpressRoute Gateway

**Configuration**:
- **SKU**: ErGw3AZ (zone-redundant, 10 Gbps)
- **Location**: East US 2
- **Public IP**: Standard SKU, zone-redundant
- **FastPath**: Enabled for low latency

---

## 3. Bill of Materials

### Monthly Costs

| Resource | Configuration | Monthly Cost (USD) |
|----------|--------------|-------------------|
| ExpressRoute Circuit (Primary) | 10 Gbps Premium | $5,125 |
| ExpressRoute Circuit (Secondary) | 10 Gbps Premium | $5,125 |
| ExpressRoute Gateway | ErGw3AZ | $730 |
| Outbound Data Transfer | 5 TB/month | $425 |
| **Total Monthly** | | **$11,405** |

### One-Time Costs
- Circuit provisioning: $2,000
- On-premises router configuration: $5,000
- Testing and validation: $3,000
- **Total One-Time**: $10,000

---

## 4. Detailed Configuration

### Terraform Deployment

```hcl
resource "azurerm_express_route_circuit" "primary" {
  name                  = "erc-prod-eus2-primary"
  resource_group_name   = "rg-prod-eus2-network-01"
  location              = "eastus2"
  service_provider_name = "Equinix"
  peering_location      = "Washington DC"
  bandwidth_in_mbps     = 10000
  
  sku {
    tier   = "Premium"
    family = "MeteredData"
  }
  
  tags = {
    Environment = "Production"
    Circuit     = "Primary"
  }
}

resource "azurerm_express_route_circuit_peering" "private" {
  peering_type                  = "AzurePrivatePeering"
  express_route_circuit_name    = azurerm_express_route_circuit.primary.name
  resource_group_name           = "rg-prod-eus2-network-01"
  peer_asn                      = 65001
  primary_peer_address_prefix   = "192.168.1.0/30"
  secondary_peer_address_prefix = "192.168.1.4/30"
  vlan_id                       = 100
  shared_key                    = var.bgp_shared_key
}

resource "azurerm_virtual_network_gateway" "ergw" {
  name                = "ergw-prod-eus2-01"
  location            = "eastus2"
  resource_group_name = "rg-prod-eus2-network-01"
  
  type     = "ExpressRoute"
  vpn_type = "RouteBased"
  
  sku = "ErGw3AZ"
  
  ip_configuration {
    name                          = "ergw-ipconfig"
    public_ip_address_id          = azurerm_public_ip.ergw.id
    private_ip_address_allocation = "Dynamic"
    subnet_id                     = azurerm_subnet.gateway.id
  }
}
```

### Route Filters

**For Financial Services Compliance**:
```bash
# Create route filter
az network route-filter create \
  --name rf-prod-eus2-er \
  --resource-group rg-prod-eus2-network-01 \
  --location eastus2

# Add rule to allow specific services
az network route-filter rule create \
  --filter-name rf-prod-eus2-er \
  --name AllowAzureStorage \
  --resource-group rg-prod-eus2-network-01 \
  --access Allow \
  --communities "12076:52004"  # Azure Storage
```

---

## 5. Monitoring & Operations

### Key Metrics

| Metric | Target | Alert Threshold |
|--------|--------|----------------|
| Circuit Availability | 99.95% | < 99.9% |
| BGP Session Status | Up | Down |
| Throughput | < 8 Gbps | > 9 Gbps |
| Packet Loss | < 0.01% | > 0.1% |
| Latency | < 10ms | > 50ms |

### Monitoring Configuration

**Connection Monitor**:
```bash
az network watcher connection-monitor create \
  --name cm-expressroute \
  --location eastus2 \
  --test-group-name tg-er-connectivity \
  --endpoint-source-name onprem-endpoint \
  --endpoint-source-resource-id /subscriptions/{sub-id}/resourceGroups/rg-onprem/providers/Microsoft.Compute/virtualMachines/vm-onprem \
  --endpoint-dest-name azure-endpoint \
  --endpoint-dest-resource-id /subscriptions/{sub-id}/resourceGroups/rg-prod-eus2-ai-01/providers/Microsoft.Compute/virtualMachines/vm-azure \
  --test-config-name tc-icmp \
  --protocol Icmp \
  --icmp-disable-trace-route false
```

### Alerts

**BGP Session Down Alert**:
```bash
az monitor metrics alert create \
  --name "ER-BGP-Session-Down" \
  --resource-group rg-prod-eus2-network-01 \
  --scopes /subscriptions/{sub-id}/resourceGroups/rg-prod-eus2-network-01/providers/Microsoft.Network/expressRouteCircuits/erc-prod-eus2-primary \
  --condition "count BgpAvailability < 1" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --severity 0 \
  --action email network-ops@contoso.com pagerduty
```

---

## 6. Disaster Recovery & Failover

### High Availability Design

**Dual Circuit Configuration**:
- Primary circuit: Active
- Secondary circuit: Active (load balanced)
- Automatic failover via BGP
- Failover time: < 30 seconds

**Failover Testing**:
```bash
# Simulate primary circuit failure
az network express-route update \
  --name erc-prod-eus2-primary \
  --resource-group rg-prod-eus2-network-01 \
  --set serviceProviderProvisioningState=NotProvisioned

# Monitor BGP convergence
az network vnet-gateway list-bgp-peer-status \
  --name ergw-prod-eus2-01 \
  --resource-group rg-prod-eus2-network-01
```

### DR Procedures

**Circuit Failure Response**:
1. Alert triggered (BGP session down)
2. Verify secondary circuit active
3. Check traffic flow via secondary
4. Contact service provider for primary circuit
5. Monitor performance during repair
6. Validate both circuits after restoration

---

## 7. Security Controls

### Network Security

**Traffic Filtering**:
- Azure Firewall inspects all ExpressRoute traffic
- NSGs on spoke VNet subnets
- Route tables force traffic through firewall

**Encryption**:
- MACsec encryption on ExpressRoute Direct (optional)
- IPsec VPN over ExpressRoute for additional encryption
- TLS 1.3 for application-layer encryption

**Access Control**:
- Private peering only (no Microsoft peering)
- Route filters to limit service access
- Azure Policy to prevent public endpoints

---

## 8. Operational Procedures

### Common Tasks

**Check Circuit Status**:
```bash
az network express-route show \
  --name erc-prod-eus2-primary \
  --resource-group rg-prod-eus2-network-01 \
  --query "{Name:name, Status:serviceProviderProvisioningState, BandwidthInMbps:serviceProviderProperties.bandwidthInMbps}"
```

**View BGP Routes**:
```bash
az network vnet-gateway list-advertised-routes \
  --name ergw-prod-eus2-01 \
  --resource-group rg-prod-eus2-network-01 \
  --peer 192.168.1.2
```

**Test Connectivity**:
```bash
# From Azure VM to on-premises
Test-NetConnection -ComputerName 172.16.10.10 -Port 443 -InformationLevel Detailed
```

### Troubleshooting

**Issue**: High latency over ExpressRoute  
**Solution**:
1. Check BGP route metrics
2. Verify no asymmetric routing
3. Test with traceroute
4. Contact service provider

**Issue**: BGP session flapping  
**Solution**:
1. Check physical layer (fiber, optics)
2. Verify BGP timers match
3. Review BGP logs
4. Check for route dampening

---

## 9. Compliance & Governance

### PCI-DSS Requirements
- ✓ Dedicated private connectivity
- ✓ Encrypted data transmission
- ✓ Network segmentation
- ✓ Continuous monitoring
- ✓ Redundant connectivity

### Change Management
- All ExpressRoute changes require CAB approval
- Maintenance windows: Saturday 2 AM - 6 AM
- Notification: 2 weeks advance notice
- Rollback plan required

---

## 10. Support & Handover

### Support Contacts
- **L1 Support**: network-support@contoso.com (24/7)
- **L2 Support**: network-ops@contoso.com (24/7)
- **Service Provider**: Equinix NOC (24/7): +1-xxx-xxx-xxxx
- **Microsoft Support**: Premier Support (24/7)

### Escalation Path
1. L1 Network Support → 15 minutes
2. L2 Network Operations → 30 minutes
3. Network Architect → 1 hour
4. Service Provider NOC → Immediate (parallel)
5. Microsoft Support → Immediate (parallel)

### Known Issues
| Issue | Workaround | Target Fix |
|-------|------------|------------|
| Occasional BGP flap | Increase BGP timers | Q1 2026 |
| Latency spikes during peak hours | Traffic shaping | Q2 2026 |

---

## References
- [ExpressRoute Documentation](https://learn.microsoft.com/azure/expressroute/)
- [ExpressRoute Connectivity Models](https://learn.microsoft.com/azure/expressroute/expressroute-connectivity-models)
- [ExpressRoute Best Practices](https://learn.microsoft.com/azure/expressroute/expressroute-best-practices)

---

**Document Owner**: Network Architect  
**Status**: Production Ready  
**Last Review**: December 2025  
**Next Review**: March 2026
