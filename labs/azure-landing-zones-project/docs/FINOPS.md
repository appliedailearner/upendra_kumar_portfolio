# FinOps Cost Management Guide

Comprehensive guide for implementing Financial Operations (FinOps) practices in your Azure Landing Zones.

## Overview

FinOps is a cultural practice that brings financial accountability to the variable spend model of cloud, enabling distributed teams to make business trade-offs between speed, cost, and quality.

## Cost Allocation Strategy

### Tagging Strategy

**Required Tags**:
```hcl
tags = {
  Environment  = "Production"           # dev, staging, prod
  CostCenter   = "AI-Platform"          # Business unit
  Owner        = "data-science-team"    # Team responsible
  Project      = "AI-Landing-Zone"      # Project name
  Compliance   = "PCI-DSS,SOC2"        # Compliance requirements
  ManagedBy    = "Terraform"            # Management method
}
```

### Cost Allocation by Environment

| Environment | Monthly Budget | Alert Threshold |
|-------------|---------------|-----------------|
| Development | $5,000 | 80% ($4,000) |
| Staging | $10,000 | 85% ($8,500) |
| Production | $50,000 | 90% ($45,000) |

## Budget Alerts

### Terraform Configuration

```hcl
# Budget Alert for AI Landing Zone
resource "azurerm_consumption_budget_resource_group" "ai_budget" {
  name              = "budget-ai-landing-zone"
  resource_group_id = azurerm_resource_group.ai_lz.id

  amount     = 15000  # $15,000/month
  time_grain = "Monthly"

  time_period {
    start_date = "2025-01-01T00:00:00Z"
  }

  notification {
    enabled   = true
    threshold = 80
    operator  = "GreaterThan"

    contact_emails = [
      "finops@contoso.com",
      "ai-ops@contoso.com"
    ]
  }

  notification {
    enabled   = true
    threshold = 90
    operator  = "GreaterThan"

    contact_emails = [
      "finops@contoso.com",
      "cfo@contoso.com"
    ]
  }

  notification {
    enabled   = true
    threshold = 100
    operator  = "GreaterThan"

    contact_emails = [
      "finops@contoso.com",
      "cfo@contoso.com",
      "ceo@contoso.com"
    ]
  }
}
```

## Cost Optimization Strategies

### 1. Reserved Instances (RIs)

**Savings**: 40-60% compared to pay-as-you-go

**Recommended for**:
- ML compute clusters (consistent usage)
- AVD session hosts (predictable workload)
- Database instances

**Implementation**:
```bash
# Analyze RI recommendations
az consumption reservation recommendation list \
  --resource-group rg-prod-eus2-ai-01 \
  --look-back-period Last30Days

# Purchase RI (1-year or 3-year)
az reservations reservation-order purchase \
  --reservation-order-id <order-id> \
  --sku Standard_D4s_v3 \
  --quantity 10 \
  --term P1Y
```

**Estimated Savings**:
- AI Landing Zone: $11,520/year
- AVD Landing Zone: $17,520/year
- Total: $29,040/year

### 2. Azure Savings Plans

**Savings**: Up to 65% for compute

**Best for**: Variable workloads across multiple services

```bash
# Purchase Savings Plan
az billing benefits savings-plan-order purchase \
  --savings-plan-order-id <order-id> \
  --sku Compute_Savings_Plan \
  --commitment-amount 500 \
  --commitment-grain Hourly \
  --term P1Y
```

### 3. Autoscaling

**Savings**: 30-50% on compute costs

**Configuration**:
```hcl
# ML Compute Cluster Autoscaling
resource "azurerm_machine_learning_compute_cluster" "cpu" {
  # ... other config ...
  
  scale_settings {
    min_node_count                       = 0    # Scale to zero
    max_node_count                       = 50
    scale_down_nodes_after_idle_duration = "PT5M"  # 5 minutes
  }
}
```

**Estimated Savings**: $16,800/year

### 4. Storage Lifecycle Management

**Savings**: 50-80% on storage costs

```hcl
resource "azurerm_storage_management_policy" "lifecycle" {
  storage_account_id = azurerm_storage_account.datalake.id

  rule {
    name    = "MoveRawToCool"
    enabled = true

    filters {
      prefix_match = ["raw/"]
      blob_types   = ["blockBlob"]
    }

    actions {
      base_blob {
        tier_to_cool_after_days_since_modification_greater_than    = 30
        tier_to_archive_after_days_since_modification_greater_than = 90
        delete_after_days_since_modification_greater_than          = 365
      }
    }
  }
}
```

**Estimated Savings**: $7,200/year

### 5. Spot Instances for Training

**Savings**: Up to 90% on compute

**Use for**: Non-critical ML training jobs

```hcl
# Spot VM for training
resource "azurerm_linux_virtual_machine" "spot_training" {
  # ... other config ...
  
  priority        = "Spot"
  eviction_policy = "Deallocate"
  max_bid_price   = 0.50  # Maximum price per hour
}
```

**Estimated Savings**: $2,160/year

## Cost Monitoring Dashboards

### Azure Monitor Workbook

```json
{
  "version": "Notebook/1.0",
  "items": [
    {
      "type": 9,
      "content": {
        "version": "KqlParameterItem/1.0",
        "query": "AzureCostManagement\n| where TimeGenerated > ago(30d)\n| summarize TotalCost = sum(Cost) by bin(TimeGenerated, 1d), ResourceGroup\n| render timechart",
        "size": 0,
        "title": "Daily Cost Trend by Resource Group"
      }
    }
  ]
}
```

### Cost Allocation Report

```kusto
// Monthly cost by tag
AzureCostManagement
| where TimeGenerated > startofmonth(now())
| extend CostCenter = tostring(Tags["CostCenter"])
| summarize TotalCost = sum(Cost) by CostCenter
| order by TotalCost desc
```

## FinOps Metrics & KPIs

### Key Metrics to Track

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Cost per User | < $75 | $61 | ✅ On Track |
| RI Coverage | > 60% | 40% | ⚠️ Action Needed |
| Waste (Idle Resources) | < 5% | 8% | ⚠️ Action Needed |
| Budget Variance | < 10% | 5% | ✅ On Track |

### Monthly Review Checklist

- [ ] Review cost trends and anomalies
- [ ] Validate budget vs. actual spend
- [ ] Identify idle or underutilized resources
- [ ] Review RI/Savings Plan coverage
- [ ] Update cost forecasts
- [ ] Optimize storage lifecycle policies
- [ ] Review and adjust autoscaling policies

## Cost Optimization Playbook

### Week 1: Assessment
1. Run cost analysis for all resource groups
2. Identify top 10 cost drivers
3. Analyze RI/Savings Plan recommendations
4. Review idle resources

### Week 2: Quick Wins
1. Implement autoscaling where missing
2. Delete unused resources
3. Resize over-provisioned VMs
4. Enable storage lifecycle policies

### Week 3: Strategic Optimization
1. Purchase RIs for consistent workloads
2. Implement Savings Plans
3. Configure budget alerts
4. Set up cost allocation tags

### Week 4: Monitoring & Governance
1. Create cost dashboards
2. Schedule monthly FinOps reviews
3. Document optimization decisions
4. Train teams on cost awareness

## Total Savings Potential

| Optimization | Annual Savings |
|--------------|---------------|
| Reserved Instances | $29,040 |
| Autoscaling | $16,800 |
| Storage Lifecycle | $7,200 |
| Spot Instances | $2,160 |
| **Total** | **$55,200/year** |

**ROI**: 30% cost reduction from baseline

## Tools & Resources

- [Azure Cost Management](https://portal.azure.com/#blade/Microsoft_Azure_CostManagement/Menu/overview)
- [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/)
- [Infracost](https://www.infracost.io/) - Cost estimation in CI/CD
- [FinOps Foundation](https://www.finops.org/)

## Contact

For FinOps questions:
- **FinOps Team**: finops@contoso.com
- **Cloud Center of Excellence**: ccoe@contoso.com
