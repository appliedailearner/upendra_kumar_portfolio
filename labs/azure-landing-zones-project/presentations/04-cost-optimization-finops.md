# Azure Landing Zones - Cost Optimization & FinOps
## Maximizing Cloud ROI

---

## Slide 1: Title Slide

# Cost Optimization & FinOps
## Azure Landing Zones

**Driving Cloud Financial Excellence**

Date: December 2025  
Audience: CFO, Finance Team, FinOps Practitioners

---

## Slide 2: FinOps Overview

### What is FinOps?

**Definition**: Financial Operations (FinOps) is a cultural practice that brings financial accountability to the variable spend model of cloud.

**Core Principles**:
1. **Teams need to collaborate**: Engineering, Finance, Business
2. **Everyone takes ownership**: Distributed decision-making
3. **Decisions are driven by business value**: Not just cost

### FinOps Lifecycle

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│ Inform  │ ──▶ │ Optimize│ ──▶ │ Operate │
└─────────┘     └─────────┘     └─────────┘
     ▲                                │
     └────────────────────────────────┘
```

---

## Slide 3: Current Cost Baseline

### Monthly Cloud Spend

| Component | Monthly Cost | % of Total |
|-----------|-------------|------------|
| AI Landing Zone | $12,219 | 29% |
| AVD Landing Zone | $8,913 | 21% |
| APIM | $6,005 | 14% |
| ExpressRoute | $11,405 | 27% |
| MCP | $611 | 1% |
| GitHub Copilot Studio | $2,742 | 7% |
| **Total** | **$41,895** | **100%** |

### Annual Projection

- **Year 1**: $502,740
- **Year 2**: $527,877 (5% growth)
- **Year 3**: $554,271 (5% growth)

**3-Year TCO**: $1,584,888

---

## Slide 4: Cost Breakdown by Category

### Compute Costs (60%)

```
AI/ML Compute: $14,520/month
├── CPU Clusters: $2,400
├── GPU Clusters: $3,600
├── ML Workspace: $0 (free tier)
└── Azure OpenAI: $460
```

### Storage Costs (15%)

```
Data Storage: $6,284/month
├── Data Lake (10 TB): $1,228
├── FSLogix (500 GB): $102
├── Backups: $450
└── Other: $504
```

### Networking Costs (20%)

```
Network Services: $8,379/month
├── ExpressRoute: $11,405
├── Private Endpoints: $250
├── Firewall: $1,200
└── VPN Gateway: $150
```

### Other Costs (5%)

```
Supporting Services: $2,095/month
├── Monitoring: $365
├── Key Vault: $25
└── Other: $205
```

---

## Slide 5: Cost Optimization Opportunities

### Immediate Wins (0-30 days)

| Optimization | Annual Savings | Effort |
|--------------|---------------|--------|
| **Reserved Instances** | $29,040 | Low |
| **Autoscaling** | $16,800 | Medium |
| **Storage Lifecycle** | $7,200 | Low |
| **Spot Instances** | $2,160 | Medium |
| **Total** | **$55,200** | |

### ROI Calculation

```
Annual Savings: $55,200
Implementation Cost: $10,000
Net Benefit Year 1: $45,200
ROI: 452%
Payback Period: 2.2 months
```

---

## Slide 6: Reserved Instances Strategy

### RI Recommendations

**AI Landing Zone Compute**:
| Resource | Current Cost | RI Cost | Savings | Term |
|----------|-------------|---------|---------|------|
| 10x D4s_v3 | $3,650/mo | $2,190/mo | 40% | 1-year |
| 5x NC6s_v3 | $3,600/mo | $2,160/mo | 40% | 1-year |

**AVD Session Hosts**:
| Resource | Current Cost | RI Cost | Savings | Term |
|----------|-------------|---------|---------|------|
| 10x D4s_v5 | $3,650/mo | $2,190/mo | 40% | 1-year |

### RI vs Savings Plans

**Reserved Instances**:
- ✅ Highest discount (up to 72%)
- ✅ Predictable workloads
- ❌ Less flexible

**Savings Plans**:
- ✅ More flexible
- ✅ Applies across services
- ❌ Lower discount (up to 65%)

**Recommendation**: RIs for base load, Savings Plans for variable workloads

---

## Slide 7: Autoscaling Implementation

### Current vs Optimized

**Before Autoscaling**:
```
ML Compute Cluster:
├── Min nodes: 10 (always running)
├── Max nodes: 50
└── Cost: $3,650/month
```

**After Autoscaling**:
```
ML Compute Cluster:
├── Min nodes: 0 (scale to zero)
├── Max nodes: 50
├── Idle timeout: 5 minutes
└── Cost: $2,250/month (avg)
```

**Savings**: $1,400/month = $16,800/year

### Autoscaling Configuration

```hcl
scale_settings {
  min_node_count = 0
  max_node_count = 50
  scale_down_nodes_after_idle_duration = "PT5M"
}
```

---

## Slide 8: Storage Optimization

### Lifecycle Management

**Policy Example**:
```
Raw Data (ingestion):
├── Day 0-30: Hot tier ($0.0184/GB)
├── Day 31-90: Cool tier ($0.01/GB)
├── Day 91-365: Archive tier ($0.002/GB)
└── Day 365+: Delete
```

**Cost Comparison** (10 TB dataset):
| Tier | Monthly Cost | Annual Cost |
|------|-------------|-------------|
| All Hot | $1,840 | $22,080 |
| Lifecycle | $920 | $11,040 |
| **Savings** | **$920** | **$11,040** |

### Blob Access Tiers

- **Hot**: Frequently accessed data
- **Cool**: Infrequently accessed (30+ days)
- **Archive**: Rarely accessed (180+ days)

---

## Slide 9: Spot Instances for Training

### Spot vs On-Demand

**Training Job Example**:
| Configuration | Cost/hour | 100-hour job | Savings |
|---------------|-----------|--------------|---------|
| On-Demand GPU | $0.90 | $90 | - |
| Spot GPU | $0.18 | $18 | 80% |

### Best Practices

**Good for Spot**:
- ✅ ML training (can checkpoint)
- ✅ Batch processing
- ✅ Dev/test workloads

**Not for Spot**:
- ❌ Production inference
- ❌ Stateful applications
- ❌ Time-sensitive workloads

### Implementation

```hcl
priority = "Spot"
eviction_policy = "Deallocate"
max_bid_price = 0.50  # Maximum $0.50/hour
```

---

## Slide 10: Cost Allocation & Tagging

### Tagging Strategy

**Required Tags**:
```hcl
tags = {
  Environment  = "Production"
  CostCenter   = "AI-Platform"
  Owner        = "data-science-team"
  Project      = "fraud-detection"
  Compliance   = "PCI-DSS"
}
```

### Cost Allocation Report

| Cost Center | Monthly | % of Total | Budget | Variance |
|-------------|---------|------------|--------|----------|
| AI Platform | $16,500 | 39% | $18,000 | -8% ✅ |
| AVD | $12,000 | 29% | $12,000 | 0% ✅ |
| APIM | $6,500 | 16% | $7,000 | -7% ✅ |
| Shared | $6,895 | 16% | $7,000 | -2% ✅ |

### Chargeback Model

- **Development**: 10% of total cost
- **Staging**: 15% of total cost
- **Production**: 75% of total cost

---

## Slide 11: Budget Alerts & Governance

### Budget Configuration

**AI Landing Zone Budget**:
```
Monthly Budget: $15,000
├── 80% Alert: $12,000 (Email: Team)
├── 90% Alert: $13,500 (Email: Manager)
├── 100% Alert: $15,000 (Email: CFO)
└── 110% Alert: $16,500 (Email: CEO + Auto-scale down)
```

### Automated Actions

**Threshold 100%**:
- Send alert to finance team
- Create incident ticket
- Schedule cost review meeting

**Threshold 110%**:
- Disable autoscaling expansion
- Stop non-production workloads
- Executive notification

---

## Slide 12: Cost Monitoring Dashboard

### Real-Time Cost Visibility

**Daily Cost Trend**:
```
$2,000 ┤                                    ╭─
$1,800 ┤                              ╭────╯
$1,600 ┤                        ╭────╯
$1,400 ┤                  ╭────╯
$1,200 ┤            ╭────╯
$1,000 ┤      ╭────╯
  $800 ┤╭────╯
       └┴────┴────┴────┴────┴────┴────┴────┴
        Mon  Tue  Wed  Thu  Fri  Sat  Sun
```

### Key Metrics

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Cost per User | < $75 | $61 | ✅ |
| RI Coverage | > 60% | 40% | ⚠️ |
| Waste (Idle) | < 5% | 8% | ⚠️ |
| Budget Variance | < 10% | 5% | ✅ |

---

## Slide 13: Waste Reduction

### Identifying Waste

**Common Sources**:
- Idle VMs (running but unused)
- Unattached disks
- Old snapshots
- Oversized resources
- Orphaned resources

### Waste Analysis

| Resource Type | Count | Monthly Cost | Action |
|---------------|-------|-------------|--------|
| Idle VMs | 3 | $1,095 | Shutdown |
| Unattached Disks | 12 | $240 | Delete |
| Old Snapshots | 45 | $180 | Delete |
| **Total Waste** | | **$1,515** | |

### Automated Cleanup

```powershell
# Weekly cleanup script
- Delete snapshots > 30 days
- Deallocate VMs idle > 7 days
- Remove unattached disks > 14 days
- Alert on oversized resources
```

---

## Slide 14: Right-Sizing Recommendations

### CPU Utilization Analysis

| Resource | Size | Avg CPU | Recommendation | Savings |
|----------|------|---------|----------------|---------|
| VM-Prod-01 | D8s_v3 | 15% | D4s_v3 | $365/mo |
| VM-Prod-02 | D16s_v3 | 25% | D8s_v3 | $730/mo |
| VM-Dev-01 | D4s_v3 | 5% | B2s | $120/mo |

**Total Right-Sizing Savings**: $1,215/month = $14,580/year

### Azure Advisor Recommendations

- **Cost**: 23 recommendations ($18,500/year savings)
- **Performance**: 8 recommendations
- **Security**: 12 recommendations
- **Reliability**: 5 recommendations

---

## Slide 15: FinOps Maturity Model

### Current State: Crawl → Walk

**Crawl** (Current):
- ✅ Cost visibility
- ✅ Basic tagging
- ✅ Monthly reporting
- ⚠️ Limited automation

**Walk** (Target - 6 months):
- Budget forecasting
- Automated optimization
- Chargeback/showback
- FinOps culture

**Run** (Future - 12 months):
- Predictive analytics
- AI-driven optimization
- Real-time governance
- FinOps excellence

---

## Slide 16: Cost Optimization Roadmap

### Phase 1: Quick Wins (Month 1)

- [x] Implement autoscaling
- [x] Purchase 1-year RIs
- [x] Enable storage lifecycle
- [ ] Right-size oversized VMs

**Expected Savings**: $4,600/month

### Phase 2: Automation (Months 2-3)

- [ ] Automated budget alerts
- [ ] Cost anomaly detection
- [ ] Waste cleanup automation
- [ ] FinOps dashboards

**Expected Savings**: Additional $1,000/month

### Phase 3: Optimization (Months 4-6)

- [ ] Evaluate 3-year RIs
- [ ] Implement Savings Plans
- [ ] Advanced right-sizing
- [ ] Container optimization

**Expected Savings**: Additional $800/month

---

## Slide 17: FinOps Team & Responsibilities

### FinOps Team Structure

**FinOps Lead**:
- Overall cost strategy
- Executive reporting
- Tool selection

**Engineering**:
- Resource optimization
- Autoscaling implementation
- Right-sizing

**Finance**:
- Budget management
- Chargeback/showback
- Forecasting

**Business**:
- Value prioritization
- ROI analysis
- Decision-making

### Meeting Cadence

- **Daily**: Cost anomaly review (automated)
- **Weekly**: Optimization opportunities
- **Monthly**: Executive cost review
- **Quarterly**: Strategy and planning

---

## Slide 18: Cost Optimization Tools

### Azure Native Tools

- **Azure Cost Management**: Cost analysis, budgets
- **Azure Advisor**: Optimization recommendations
- **Azure Monitor**: Resource utilization
- **Azure Policy**: Governance enforcement

### Third-Party Tools

- **Infracost**: IaC cost estimation
- **Kubecost**: Kubernetes cost allocation
- **CloudHealth**: Multi-cloud FinOps
- **Spot.io**: Automated optimization

### Custom Dashboards

- Power BI cost dashboards
- Grafana monitoring
- Custom KQL queries
- Automated reports

---

## Slide 19: Success Metrics

### Financial KPIs

| KPI | Baseline | Target | Current |
|-----|----------|--------|---------|
| Monthly Cloud Spend | $41,895 | $35,000 | $38,500 |
| Cost per User | $70 | $60 | $61 |
| RI Coverage | 0% | 60% | 40% |
| Waste % | 12% | < 5% | 8% |

### Operational KPIs

| KPI | Target | Current |
|-----|--------|---------|
| Budget Forecast Accuracy | > 95% | 92% |
| Cost Anomaly Detection | < 24 hours | 12 hours |
| Optimization Implementation | < 7 days | 5 days |

### Business KPIs

- **ROI on Cloud Investment**: 78%
- **Time to Market**: 40% faster
- **Innovation Budget**: 20% of cloud spend

---

## Slide 20: Call to Action

### Next Steps

**This Week**:
1. Approve RI purchases ($29K/year savings)
2. Enable autoscaling ($17K/year savings)
3. Implement storage lifecycle ($7K/year savings)

**This Month**:
4. Right-size oversized resources
5. Set up budget alerts
6. Deploy FinOps dashboard

**This Quarter**:
7. Establish FinOps culture
8. Monthly cost reviews
9. Continuous optimization

### Expected Impact

- **Year 1 Savings**: $55,200
- **3-Year Savings**: $180,000
- **ROI**: 452%

---

*Cost Optimization & FinOps - Confidential*  
*© 2025 Azure Landing Zones Project*
