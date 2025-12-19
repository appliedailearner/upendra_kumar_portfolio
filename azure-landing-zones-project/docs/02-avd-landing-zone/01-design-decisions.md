# AVD Landing Zone - Design Decisions

**Project**: Azure Landing Zones - Financial Services  
**Component**: AVD (Azure Virtual Desktop) Landing Zone  
**Version**: 1.0.0  
**Last Updated**: December 2025

---

## Executive Summary

This document outlines key architectural decisions for implementing Azure Virtual Desktop (AVD) for secure remote access in a Financial Services organization, ensuring compliance with PCI-DSS, SOC 2, and regulatory requirements.

---

## 1. AVD Deployment Model

### Decision: Pooled Multi-Session with Personal Desktops for Executives

**Rationale**:
- **Pooled Multi-Session**: Windows 11 Enterprise multi-session for general users (cost-effective, 80% of users)
- **Personal Desktops**: Dedicated VMs for executives and compliance officers (data isolation, 20% of users)
- **Hybrid Approach**: Balances cost and security requirements

**Configuration**:
| User Type | Deployment Type | VM SKU | Users per VM | Total VMs |
|-----------|----------------|--------|--------------|-----------|
| General Users | Pooled | Standard_D4s_v5 | 10 | 20 |
| Power Users | Pooled | Standard_D8s_v5 | 5 | 10 |
| Executives | Personal | Standard_D4s_v5 | 1 | 15 |

---

## 2. Network Architecture

### Decision: Dedicated AVD VNet with Hub-Spoke Topology

**Network Design**:
```
Hub VNet (10.0.0.0/16)
└── Azure Firewall, Gateway

AVD Spoke VNet (10.200.0.0/16)
├── Session Host Subnet (10.200.1.0/24)
├── Management Subnet (10.200.2.0/24)
└── Private Endpoints Subnet (10.200.3.0/24)
```

**Security Controls**:
- All traffic routed through Azure Firewall
- RDP Shortpath for optimal performance
- Private endpoints for Azure Files (FSLogix)
- No public IP addresses on session hosts

---

## 3. Identity and Access

### Decision: Azure AD with Hybrid Join and Conditional Access

**Authentication**:
- Azure AD hybrid join for session hosts
- Azure AD authentication for user access
- MFA mandatory for all users
- Conditional Access policies:
  - Require compliant device
  - Require MFA
  - Block legacy authentication
  - Geo-fencing (US only)

**RBAC Roles**:
| Role | Permissions | Assignment |
|------|-------------|------------|
| Desktop Virtualization User | Access AVD resources | All AVD users |
| Virtual Machine User Login | Login to session hosts | General users |
| Virtual Machine Administrator Login | Admin access | IT support |

---

## 4. FSLogix Profile Management

### Decision: Azure Files Premium with Private Endpoints

**Storage Configuration**:
- **Tier**: Azure Files Premium (low latency)
- **Capacity**: 10 TB (expandable)
- **Redundancy**: ZRS (zone-redundant)
- **Encryption**: SMB 3.1.1 with AES-256-GCM
- **Access**: Private endpoint only

**FSLogix Settings**:
```
VHDLocations=\\stprodeus2avdprofiles.file.core.windows.net\profiles
SizeInMBs=30000
IsDynamic=1
VolumeType=VHDX
FlipFlopProfileDirectoryName=1
```

---

## 5. Image Management

### Decision: Azure Compute Gallery with Golden Images

**Image Pipeline**:
1. Base Image: Windows 11 Enterprise multi-session
2. Security hardening (CIS benchmarks)
3. Application installation (Office 365, LOB apps)
4. Optimization (Virtual Desktop Optimization Tool)
5. Sysprep and capture
6. Publish to Compute Gallery
7. Replicate to DR region

**Update Cadence**:
- Monthly security patches
- Quarterly feature updates
- Automated deployment via Azure DevOps

---

## 6. Monitoring and Management

### Decision: Azure Monitor with Log Analytics and Insights for AVD

**Monitoring Stack**:
- Azure Monitor for AVD (built-in insights)
- Log Analytics workspace
- Connection diagnostics
- Performance counters
- User session tracking

**Key Metrics**:
- Connection success rate (target: > 99%)
- Login time (target: < 30 seconds)
- Input delay (target: < 150ms)
- Session host CPU/memory utilization

---

## 7. Disaster Recovery

### Decision: Active-Passive with Secondary Region

**DR Strategy**:
- **Primary**: East US 2
- **Secondary**: West US 2
- **RPO**: 4 hours
- **RTO**: 4 hours
- **Failover**: Manual with automated runbooks

**DR Components**:
- Host pools replicated to secondary region
- FSLogix profiles geo-replicated (GRS)
- Images replicated via Compute Gallery
- Quarterly DR testing

---

## 8. Security Controls

### Decision: Defense-in-Depth with MFA, Encryption, and Monitoring

**Security Layers**:
1. **Network**: NSGs, Azure Firewall, no public IPs
2. **Identity**: Azure AD, MFA, Conditional Access
3. **Data**: Encryption at rest and in transit
4. **Monitoring**: Azure Sentinel, session recording
5. **Compliance**: Azure Policy enforcement

**Session Recording**:
- All privileged sessions recorded
- Retention: 90 days
- Storage: Immutable blob storage

---

## 9. Scaling Strategy

### Decision: Autoscaling with Start VM on Connect

**Autoscaling Configuration**:
- **Peak Hours** (8 AM - 6 PM): 80% capacity
- **Off-Peak**: 20% capacity
- **Scaling Trigger**: Available sessions < 20%
- **Start VM on Connect**: Enabled for cost savings

**Cost Optimization**:
- Deallocate VMs during off-hours
- Use Azure Hybrid Benefit
- Reserved Instances for base capacity

---

## 10. Application Delivery

### Decision: MSIX App Attach for Application Management

**Rationale**:
- Separates apps from OS image
- Faster image updates
- Reduced storage requirements
- Dynamic app delivery

**MSIX Packages**:
- Microsoft Office 365
- Adobe Acrobat Reader
- LOB applications
- Browser extensions

---

## Decision Log

| ID | Decision | Date | Owner | Status |
|----|----------|------|-------|--------|
| DD-AVD-001 | Pooled + Personal deployment | Dec 2025 | Cloud Architect | Approved |
| DD-AVD-002 | Azure Files Premium for FSLogix | Dec 2025 | Storage Architect | Approved |
| DD-AVD-003 | Hybrid Azure AD join | Dec 2025 | Identity Architect | Approved |
| DD-AVD-004 | MSIX App Attach | Dec 2025 | App Delivery Lead | Approved |
| DD-AVD-005 | Session recording for compliance | Dec 2025 | Security Architect | Approved |

---

**Document Owner**: Cloud Architect  
**Reviewers**: Security Architect, Identity Architect, Compliance Officer  
**Approval Date**: December 2025  
**Next Review**: March 2026
