# AI Landing Zone - Bill of Materials

**Project**: Azure Landing Zones - Financial Services  
**Component**: AI Landing Zone  
**Version**: 1.0.0  
**Last Updated**: December 2025

---

## Executive Summary

This document provides a comprehensive inventory of all Azure resources, services, and third-party components required for the AI Landing Zone implementation. Cost estimates are based on East US 2 pricing as of December 2025.

---

## 1. Compute Resources

### 1.1 Azure Machine Learning Compute

| Resource | SKU | Quantity | Configuration | Monthly Cost (USD) |
|----------|-----|----------|---------------|-------------------|
| ML Workspace | Enterprise | 1 | Managed VNet, Private endpoints | $0 (workspace itself) |
| CPU Compute Cluster | Standard_D4s_v3 | 4-50 nodes | Autoscaling, 4 vCPU, 16 GB RAM | $2,400 (avg 15 nodes) |
| GPU Compute Cluster | Standard_NC6s_v3 | 2-20 nodes | Autoscaling, 6 vCPU, 112 GB RAM, V100 | $3,600 (avg 5 nodes) |
| Compute Instance (Dev) | Standard_DS3_v2 | 10 | 4 vCPU, 14 GB RAM, per data scientist | $1,200 |
| Inference Cluster (AKS) | Standard_D4s_v3 | 3-10 nodes | Production inference, autoscaling | $800 (avg 5 nodes) |

**Subtotal**: $8,000/month

---

### 1.2 Azure OpenAI Service

| Resource | Model | Deployment | Tokens/Month | Monthly Cost (USD) |
|----------|-------|------------|--------------|-------------------|
| Azure OpenAI - Primary | GPT-4 | Standard | 5M tokens | $150 |
| Azure OpenAI - Primary | GPT-4 Turbo | Standard | 10M tokens | $200 |
| Azure OpenAI - Primary | GPT-3.5 Turbo | Standard | 20M tokens | $40 |
| Azure OpenAI - Primary | text-embedding-ada-002 | Standard | 50M tokens | $10 |
| Azure OpenAI - Secondary | GPT-4 (DR) | Standard | 2M tokens (standby) | $60 |

**Subtotal**: $460/month

---

## 2. Storage Resources

### 2.1 Data Lake Storage Gen2

| Resource | Tier | Capacity | Redundancy | Monthly Cost (USD) |
|----------|------|----------|------------|-------------------|
| ML Data Lake - Hot | Premium | 5 TB | ZRS | $768 |
| ML Data Lake - Cool | Standard | 10 TB | GRS | $200 |
| ML Data Lake - Archive | Standard | 50 TB | GRS | $100 |
| Model Registry Storage | Standard Hot | 500 GB | LRS | $10 |
| Logs and Metrics | Standard Hot | 1 TB | LRS | $20 |

**Subtotal**: $1,098/month

---

### 2.2 Azure Blob Storage

| Resource | Tier | Capacity | Purpose | Monthly Cost (USD) |
|----------|------|----------|---------|-------------------|
| Training Datasets | Standard Hot | 2 TB | Active ML training | $40 |
| Model Artifacts | Standard Cool | 5 TB | Versioned models | $50 |
| Backup Storage | Standard Archive | 20 TB | Long-term retention | $40 |

**Subtotal**: $130/month

---

## 3. Networking Resources

### 3.1 Virtual Networks

| Resource | Configuration | Monthly Cost (USD) |
|----------|---------------|-------------------|
| AI Spoke VNet | 10.100.0.0/16, 4 subnets | $0 (no charge) |
| VNet Peering to Hub | Ingress/Egress data transfer | $150 (estimated) |

**Subtotal**: $150/month

---

### 3.2 Private Endpoints

| Resource | Service | Quantity | Monthly Cost (USD) |
|----------|---------|----------|-------------------|
| Private Endpoint | Azure OpenAI | 2 (primary + secondary) | $15 |
| Private Endpoint | ML Workspace | 1 | $7.50 |
| Private Endpoint | Storage Account (ADLS) | 2 | $15 |
| Private Endpoint | Key Vault | 1 | $7.50 |
| Private Endpoint | Container Registry | 1 | $7.50 |
| Private Endpoint | AKS (inference) | 1 | $7.50 |

**Subtotal**: $60/month

---

### 3.3 Load Balancing and Traffic Management

| Resource | SKU | Purpose | Monthly Cost (USD) |
|----------|-----|---------|-------------------|
| Azure Front Door | Standard | Global load balancing for OpenAI | $35 |
| Traffic Manager | Standard | Multi-region failover | $5 |

**Subtotal**: $40/month

---

## 4. Security and Identity

### 4.1 Azure Key Vault

| Resource | SKU | Configuration | Monthly Cost (USD) |
|----------|-----|---------------|-------------------|
| Key Vault | Premium | HSM-backed keys, CMK for encryption | $25 |
| Key Operations | - | 100K operations/month | $5 |
| Secrets Storage | - | 500 secrets | $2 |

**Subtotal**: $32/month

---

### 4.2 Azure AD Premium

| Resource | License | Quantity | Monthly Cost (USD) |
|----------|---------|----------|-------------------|
| Azure AD P2 | Per user | 50 users (AI team) | $450 (included in org license) |
| Conditional Access | - | Included in P2 | $0 |
| PIM | - | Included in P2 | $0 |

**Subtotal**: $0 (assumed existing license)

---

## 5. Monitoring and Management

### 5.1 Azure Monitor

| Resource | Configuration | Monthly Cost (USD) |
|----------|---------------|-------------------|
| Log Analytics Workspace | 100 GB/day ingestion | $230 |
| Application Insights | 50 GB/month | $115 |
| Metrics | 10M custom metrics | $10 |
| Alerts | 100 alert rules | $10 |

**Subtotal**: $365/month

---

### 5.2 Azure Sentinel

| Resource | Configuration | Monthly Cost (USD) |
|----------|---------------|-------------------|
| Sentinel Data Ingestion | 50 GB/day | $115 |
| Sentinel Analytics | Included | $0 |

**Subtotal**: $115/month

---

## 6. DevOps and Automation

### 6.1 Azure DevOps

| Resource | Configuration | Monthly Cost (USD) |
|----------|---------------|-------------------|
| Azure DevOps | Basic Plan, 10 users | $60 |
| Azure Pipelines | 2 parallel jobs (Microsoft-hosted) | $80 |
| Azure Artifacts | 10 GB storage | $4 |

**Subtotal**: $144/month

---

### 6.2 Container Registry

| Resource | SKU | Configuration | Monthly Cost (USD) |
|----------|-----|---------------|-------------------|
| Azure Container Registry | Premium | Geo-replication, private endpoints | $50 |
| Storage | 500 GB | Container images | $25 |

**Subtotal**: $75/month

---

## 7. Data Services

### 7.1 Azure Cosmos DB (for metadata)

| Resource | Configuration | Monthly Cost (USD) |
|----------|---------------|-------------------|
| Cosmos DB | 1000 RU/s, 100 GB | $60 |

**Subtotal**: $60/month

---

## 8. Backup and Disaster Recovery

### 8.1 Azure Backup

| Resource | Configuration | Monthly Cost (USD) |
|----------|---------------|-------------------|
| Backup Storage | 10 TB (GRS) | $200 |
| Backup Instances | 20 VMs/resources | $40 |

**Subtotal**: $240/month

---

### 8.2 Azure Site Recovery

| Resource | Configuration | Monthly Cost (USD) |
|----------|---------------|-------------------|
| ASR Licensing | 10 protected instances | $250 |

**Subtotal**: $250/month

---

## 9. Third-Party and Additional Services

### 9.1 Software Licenses

| Software | License Type | Quantity | Monthly Cost (USD) |
|----------|--------------|----------|-------------------|
| Python Libraries | Open source | - | $0 |
| MLflow | Open source | - | $0 |
| Responsible AI Toolbox | Open source | - | $0 |

**Subtotal**: $0/month

---

### 9.2 Support and Professional Services

| Service | Description | Monthly Cost (USD) |
|---------|-------------|-------------------|
| Azure Support | Professional Direct | $1,000 |
| External Consultants | As needed | Variable |

**Subtotal**: $1,000/month

---

## 10. Cost Summary

### 10.1 Monthly Recurring Costs

| Category | Monthly Cost (USD) |
|----------|-------------------|
| Compute Resources | $8,460 |
| Storage Resources | $1,228 |
| Networking | $250 |
| Security and Identity | $32 |
| Monitoring and Management | $480 |
| DevOps and Automation | $219 |
| Data Services | $60 |
| Backup and DR | $490 |
| Support | $1,000 |
| **Total Monthly Cost** | **$12,219** |

---

### 10.2 One-Time Costs

| Item | Cost (USD) |
|------|-----------|
| Initial Setup and Configuration | $5,000 |
| Data Migration | $3,000 |
| Training and Knowledge Transfer | $4,000 |
| Documentation | $2,000 |
| Testing and Validation | $3,000 |
| **Total One-Time Cost** | **$17,000** |

---

### 10.3 Annual Cost Projection

| Year | Monthly Avg | Annual Total | Notes |
|------|-------------|--------------|-------|
| Year 1 | $12,219 | $163,628 | Includes one-time costs ($17K) + 12 months operation |
| Year 2 | $12,219 | $146,628 | Operational costs only |
| Year 3 | $13,441 | $161,292 | 10% growth in usage |

---

## 11. Cost Optimization Opportunities

### 11.1 Reserved Instances

| Resource | Commitment | Savings | Annual Savings (USD) |
|----------|-----------|---------|---------------------|
| ML Compute (CPU) | 1-year RI | 40% | $11,520 |
| ML Compute (GPU) | 1-year RI | 40% | $17,280 |
| Storage (ADLS) | 1-year reservation | 20% | $2,400 |
| **Total Potential Savings** | - | - | **$31,200/year** |

---

### 11.2 Autoscaling and Scheduling

| Optimization | Description | Estimated Savings (USD/month) |
|--------------|-------------|------------------------------|
| Scale to zero | Stop dev compute instances after hours | $400 |
| Spot instances | Use spot VMs for training (non-critical) | $800 |
| Lifecycle policies | Auto-tier storage to cool/archive | $200 |
| **Total Monthly Savings** | - | **$1,400** |

---

## 12. Resource Tagging Strategy

All resources will be tagged with the following mandatory tags:

| Tag Name | Purpose | Example Value |
|----------|---------|---------------|
| Environment | Deployment environment | Production, Development, Test |
| CostCenter | Chargeback allocation | AI-Platform |
| Owner | Resource owner | data-science-team |
| Project | Project identifier | ai-landing-zone |
| Compliance | Compliance requirements | PCI-DSS, SOC2 |
| DR | Disaster recovery tier | Tier1 (critical) |
| DataClassification | Data sensitivity | HighlySensitive |

---

## 13. Resource Naming Convention

Resources follow this naming pattern:
```
<resource-type>-<environment>-<region>-<project>-<instance>
```

**Examples:**
- `aml-prod-eus2-ai-01` (Azure ML Workspace)
- `st-prod-eus2-ai-datalake` (Storage Account)
- `kv-prod-eus2-ai-01` (Key Vault)
- `aoai-prod-eus2-ai-01` (Azure OpenAI)

---

## 14. Procurement and Provisioning

### 14.1 Procurement Timeline

| Week | Activity | Owner |
|------|----------|-------|
| Week 1 | Submit Azure subscription request | Cloud Architect |
| Week 1 | Request quota increases | Cloud Architect |
| Week 2 | Provision networking resources | Network Engineer |
| Week 3 | Deploy core AI services | Cloud Architect |
| Week 4 | Configure security and monitoring | Security Engineer |

---

### 14.2 Quota Requirements

| Resource | Default Quota | Required Quota | Increase Needed |
|----------|---------------|----------------|-----------------|
| vCPUs (D-series) | 20 | 200 | Yes |
| vCPUs (NC-series GPU) | 0 | 120 | Yes |
| Storage Accounts | 250 | 10 | No |
| Private Endpoints | 64 | 10 | No |
| Azure OpenAI TPM | 60K | 300K | Yes |

---

## 15. Vendor and Licensing Information

### 15.1 Microsoft Licensing

| Product | License Type | Agreement |
|---------|--------------|-----------|
| Azure Services | Pay-as-you-go / EA | Enterprise Agreement |
| Azure OpenAI | Consumption-based | Standard Azure Terms |
| Azure ML | Consumption-based | Standard Azure Terms |

---

### 15.2 Third-Party Dependencies

| Component | License | Source |
|-----------|---------|--------|
| Python | PSF License | python.org |
| TensorFlow | Apache 2.0 | tensorflow.org |
| PyTorch | BSD License | pytorch.org |
| Scikit-learn | BSD License | scikit-learn.org |
| MLflow | Apache 2.0 | mlflow.org |

---

## 16. Change Log

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | Dec 2025 | Initial BOM | Cloud Architect |

---

## 17. Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Cloud Architect | [Redacted] | _________ | ______ |
| Finance Manager | [Redacted] | _________ | ______ |
| IT Director | [Redacted] | _________ | ______ |

---

**Document Owner**: Cloud Architect  
**Reviewers**: Finance Manager, Procurement, IT Director  
**Approval Date**: December 2025  
**Next Review**: March 2026 (quarterly review)
