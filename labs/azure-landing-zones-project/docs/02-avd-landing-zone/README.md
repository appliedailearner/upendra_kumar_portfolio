# AVD Landing Zone - Complete Documentation Package

**Project**: Azure Landing Zones - Financial Services  
**Component**: AVD (Azure Virtual Desktop) Landing Zone  
**Version**: 1.0.0  
**Last Updated**: December 2025

---

> **Note**: This is a consolidated documentation package. For detailed design decisions, see `01-design-decisions.md`.

## 1. Assumptions

### Organizational
- Existing Azure AD tenant with hybrid identity
- Active Directory Domain Services available
- 200+ remote workers requiring secure access
- Compliance requirements: PCI-DSS, SOC 2, GLBA

### Technical
- ExpressRoute connectivity: 1 Gbps minimum
- On-premises AD synchronized to Azure AD
- Network latency < 50ms to Azure region
- User profiles < 30 GB per user

### Financial
- Monthly budget: $15,000
- One-time setup: $25,000
- 3-year commitment acceptable for Reserved Instances

---

## 2. Bill of Materials

### Monthly Costs

| Resource | SKU | Quantity | Monthly Cost (USD) |
|----------|-----|----------|-------------------|
| Session Hosts (Pooled) | Standard_D4s_v5 | 30 VMs | $3,600 |
| Session Hosts (Personal) | Standard_D4s_v5 | 15 VMs | $1,800 |
| Azure Files Premium | 10 TB | 1 | $2,048 |
| Azure Firewall | Standard | 1 | $1,250 |
| Log Analytics | 50 GB/day | 1 | $115 |
| Azure Backup | 5 TB | 1 | $100 |
| **Total Monthly** | | | **$8,913** |

### One-Time Costs
- Initial setup and configuration: $10,000
- Image creation and testing: $5,000
- User migration: $8,000
- Training: $2,000
- **Total One-Time**: $25,000

---

## 3. Architecture Overview

### Network Topology
```
On-Premises ←→ ExpressRoute ←→ Hub VNet (10.0.0.0/16)
                                    ↓
                              AVD Spoke VNet (10.200.0.0/16)
                                    ├── Session Hosts (10.200.1.0/24)
                                    ├── Management (10.200.2.0/24)
                                    └── Private Endpoints (10.200.3.0/24)
```

### Components
- **Host Pools**: 3 pools (General, Power Users, Executives)
- **Session Hosts**: 45 VMs total
- **FSLogix Profiles**: Azure Files Premium
- **Image Management**: Azure Compute Gallery
- **Monitoring**: Azure Monitor + Log Analytics

---

## 4. Detailed Design

### Host Pool Configuration

**General Users Pool**:
- Name: hp-prod-eus2-avd-general
- Type: Pooled, multi-session
- Max sessions per host: 10
- Load balancing: Breadth-first
- VMs: 20 × Standard_D4s_v5

**Power Users Pool**:
- Name: hp-prod-eus2-avd-power
- Type: Pooled, multi-session
- Max sessions per host: 5
- Load balancing: Depth-first
- VMs: 10 × Standard_D8s_v5

**Executives Pool**:
- Name: hp-prod-eus2-avd-exec
- Type: Personal
- Assignment: Direct
- VMs: 15 × Standard_D4s_v5

### Security Configuration
- **Encryption**: BitLocker on OS disks, AES-256 for Azure Files
- **MFA**: Enforced via Conditional Access
- **Session Recording**: All sessions logged to immutable storage
- **Network**: All traffic through Azure Firewall

---

## 5. Low-Level Design

### Terraform Configuration

```hcl
resource "azurerm_virtual_desktop_host_pool" "general" {
  name                = "hp-prod-eus2-avd-general"
  location            = "eastus2"
  resource_group_name = "rg-prod-eus2-avd-01"
  type                = "Pooled"
  load_balancer_type  = "BreadthFirst"
  maximum_sessions_allowed = 10
  
  start_vm_on_connect = true
  
  scheduled_agent_updates {
    enabled = true
    schedule {
      day_of_week = "Saturday"
      hour_of_day = 2
    }
  }
}

resource "azurerm_virtual_desktop_application_group" "general_desktop" {
  name                = "ag-prod-eus2-avd-general-desktop"
  location            = "eastus2"
  resource_group_name = "rg-prod-eus2-avd-01"
  type                = "Desktop"
  host_pool_id        = azurerm_virtual_desktop_host_pool.general.id
}
```

### FSLogix Configuration

**Registry Settings**:
```
HKLM\SOFTWARE\FSLogix\Profiles
- Enabled: 1
- VHDLocations: \\stprodeus2avdprofiles.file.core.windows.net\profiles
- SizeInMBs: 30000
- IsDynamic: 1
- VolumeType: VHDX
- DeleteLocalProfileWhenVHDShouldApply: 1
```

---

## 6. Handover Document

### Support Contacts
- **L1 Support**: avd-support@contoso.com (24/7)
- **L2 Support**: desktop-ops@contoso.com (24/7)
- **L3 Engineering**: avd-engineering@contoso.com (8/5)

### Daily Operations

**Morning Checks**:
- [ ] Verify all host pools healthy
- [ ] Check session host availability
- [ ] Review overnight connection failures
- [ ] Validate FSLogix profile access

**Common Tasks**:

**Add User to AVD**:
```powershell
Add-AzRoleAssignment `
  -SignInName user@contoso.com `
  -RoleDefinitionName "Desktop Virtualization User" `
  -ResourceName "ag-prod-eus2-avd-general-desktop" `
  -ResourceGroupName "rg-prod-eus2-avd-01" `
  -ResourceType "Microsoft.DesktopVirtualization/applicationGroups"
```

**Drain Session Host**:
```powershell
Update-AzWvdSessionHost `
  -ResourceGroupName "rg-prod-eus2-avd-01" `
  -HostPoolName "hp-prod-eus2-avd-general" `
  -Name "avd-vm-01.contoso.com" `
  -AllowNewSession:$false
```

### Monitoring Dashboards
- **AVD Insights**: Azure Portal → Monitor → Insights → Azure Virtual Desktop
- **Connection Monitor**: Track connection success/failure rates
- **Performance**: CPU, memory, disk, network per session host
- **User Sessions**: Active sessions, disconnected sessions

### Known Issues
| Issue | Workaround | Target Fix |
|-------|------------|------------|
| Slow profile load (> 60s) | Clear local profile cache | Q1 2026 |
| Occasional black screen | Restart session host | Q2 2026 |

### Disaster Recovery
**Failover Procedure**:
1. Declare disaster (primary region unavailable)
2. Activate secondary host pools in West US 2
3. Update DNS for AVD gateway
4. Validate user connectivity
5. Monitor performance

**Recovery Time**: 4 hours  
**Recovery Point**: 4 hours

---

## References
- [Azure Virtual Desktop Documentation](https://learn.microsoft.com/azure/virtual-desktop/)
- [FSLogix Documentation](https://learn.microsoft.com/fslogix/)
- [AVD Security Best Practices](https://learn.microsoft.com/security/benchmark/azure/baselines/virtual-desktop-security-baseline)

---

**Document Owner**: Cloud Architect  
**Status**: Production Ready  
**Last Review**: December 2025
