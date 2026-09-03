# Strategic Selection Matrix: Azure Resiliency Patterns

| Service Tier | Pattern | Best For | Risk/Trade-off |
| :--- | :--- | :--- | :--- |
| **Foundation** | Locally redundant, single region | Internal tools, dev/test, low-impact workloads. | No protection against datacenter/zone faults. |
| **High Availability** | Single region, multi-zone | Production workloads requiring in-region resilience. | No protection from full regional outages. |
| **Zonal Control** | Zonal deployment across zones | VM-heavy/latency-sensitive apps needing tight control. | Failover/replication management is on you (Azure doesn't auto-manage). |
| **Standard DR** | Primary + Secondary (Active-Passive) | Business-critical apps tolerating some recovery time. | Potential data loss; near-zero RPO/RTO requires Active-Active. |
| **Mission Critical** | Multi-zone + Multi-region (Active-Active) | Always-on digital services with very low RTO/RPO. | Highest cost and complexity; requires high operational maturity. |
| **Compliance/GSA** | Multi-region (Nonpaired regions) | Regulated workloads with specific geo-DR requirements. | Nonpaired is not automatically better; must check service support. |
| **Basic Continuity** | Single region + Cross-region backups | Workloads with residency constraints but modest DR needs. | Backup is for recovery, NOT availability. No continuous service. |
