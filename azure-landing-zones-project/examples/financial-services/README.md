# Financial Services - AI Landing Zone Example

This example demonstrates deploying the AI Landing Zone for a Financial Services organization with PCI-DSS and SOC 2 compliance requirements.

## Features

- ✅ Azure OpenAI with GPT-4 and GPT-3.5 Turbo
- ✅ Azure Machine Learning Enterprise workspace
- ✅ Private endpoints for all PaaS services
- ✅ Customer-managed encryption keys
- ✅ PCI-DSS and SOC 2 compliance controls
- ✅ Multi-region deployment ready

## Usage

```hcl
module "ai_landing_zone" {
  source = "../../modules/ai-landing-zone"

  # Basic Configuration
  resource_group_name = "rg-prod-eus2-ai-01"
  location            = "eastus2"
  location_short      = "eus2"
  environment         = "prod"
  
  # Network Configuration
  vnet_address_space = ["10.100.0.0/16"]
  hub_vnet_address_space = "10.0.0.0/16"  # Hub VNet for connectivity
  
  # Compliance Requirements
  industry_compliance = {
    pci_dss = true   # Payment Card Industry
    hipaa   = false
    sox     = false
    gdpr    = true   # EU customers
  }
  
  # Cost Tier
  cost_tier = "standard"  # Balanced performance and cost
  
  # Enable Services
  enable_azure_openai = true
  enable_ml_workspace = true
  
  # Azure OpenAI Deployments
  openai_deployments = [
    {
      name          = "gpt-4"
      model_name    = "gpt-4"
      model_version = "0613"
      sku_name      = "Standard"
      sku_capacity  = 100
    },
    {
      name          = "gpt-35-turbo"
      model_name    = "gpt-35-turbo"
      model_version = "0613"
      sku_name      = "Standard"
      sku_capacity  = 200
    }
  ]
  
  # ML Compute Configuration
  ml_compute_config = {
    cpu_cluster_enabled   = true
    cpu_cluster_min_nodes = 0
    cpu_cluster_max_nodes = 50
    cpu_cluster_vm_size   = "Standard_D4s_v3"
    gpu_cluster_enabled   = true
    gpu_cluster_min_nodes = 0
    gpu_cluster_max_nodes = 20
    gpu_cluster_vm_size   = "Standard_NC6s_v3"
  }
  
  # Storage Lifecycle Rules
  storage_lifecycle_rules = [
    {
      name                       = "MoveRawToCool"
      prefix_match               = ["raw/"]
      tier_to_cool_after_days    = 30
      tier_to_archive_after_days = 90
      delete_after_days          = 0
    },
    {
      name                       = "DeleteOldInference"
      prefix_match               = ["inference/"]
      tier_to_cool_after_days    = 0
      tier_to_archive_after_days = 0
      delete_after_days          = 30
    }
  ]
  
  # Monitoring
  enable_diagnostic_settings = true
  enable_monitoring_alerts   = true
  alert_email_addresses      = ["ai-ops@contoso.com"]
  log_analytics_retention_days = 730  # 2 years for PCI-DSS
  
  # Tags
  tags = {
    Environment  = "Production"
    CostCenter   = "AI-Platform"
    Owner        = "data-science-team"
    Compliance   = "PCI-DSS,SOC2,GDPR"
    Project      = "AI-Landing-Zone"
    ManagedBy    = "Terraform"
  }
}
```

## Outputs

```hcl
output "ml_workspace_id" {
  description = "Azure ML workspace resource ID"
  value       = module.ai_landing_zone.ml_workspace_id
}

output "azure_openai_endpoint" {
  description = "Azure OpenAI endpoint URL"
  value       = module.ai_landing_zone.azure_openai_endpoint
}

output "storage_account_name" {
  description = "Data Lake storage account name"
  value       = module.ai_landing_zone.storage_account_name
}

output "key_vault_uri" {
  description = "Key Vault URI"
  value       = module.ai_landing_zone.key_vault_uri
}
```

## Deployment

### Prerequisites

1. Azure subscription with appropriate permissions
2. Terraform >= 1.6.0
3. Azure CLI logged in
4. Service Principal for Terraform (recommended)

### Steps

```bash
# 1. Initialize Terraform
terraform init

# 2. Review the plan
terraform plan -out=tfplan

# 3. Apply the configuration
terraform apply tfplan

# 4. Verify deployment
terraform output
```

## Cost Estimate

### Monthly Costs (Standard Tier)

| Service | Configuration | Monthly Cost (USD) |
|---------|--------------|-------------------|
| Azure OpenAI | 2 deployments | $460 |
| ML Workspace | Enterprise | $0 |
| CPU Compute | 15 nodes avg | $2,400 |
| GPU Compute | 5 nodes avg | $3,600 |
| Storage | 10 TB | $1,228 |
| Key Vault | Premium | $25 |
| Networking | Private endpoints | $250 |
| Monitoring | 100 GB logs | $365 |
| **Total** | | **~$8,328/month** |

### Cost Optimization

- **Reserved Instances**: Save 40% on compute ($1,600/month)
- **Autoscaling**: Reduce idle costs ($400/month)
- **Storage Lifecycle**: Archive old data ($200/month)
- **Total Savings**: **~$2,200/month**

## Security Controls

### Network Security
- All resources deployed with private endpoints
- No public IP addresses
- NSG rules restrict traffic to hub VNet only
- Azure Firewall integration ready

### Data Protection
- Customer-managed keys (CMK) for encryption
- TLS 1.3 for data in transit
- Soft delete enabled (90 days)
- Purge protection enabled

### Identity & Access
- System-assigned managed identities
- Azure AD integration
- RBAC with least privilege
- PIM for admin access

### Compliance
- PCI-DSS v4.0 controls
- SOC 2 Type II controls
- GDPR data residency
- 2-year log retention

## Post-Deployment

### 1. Configure Azure AD Access

```bash
# Grant users access to ML workspace
az ml workspace share \
  --name aml-prod-eus2-ai-01 \
  --resource-group rg-prod-eus2-ai-01 \
  --user user@contoso.com \
  --role Contributor
```

### 2. Upload Training Data

```bash
# Upload data to Data Lake
az storage blob upload-batch \
  --account-name stprodeus2aidatalake \
  --destination raw \
  --source ./training-data
```

### 3. Deploy ML Models

```bash
# Deploy model to Azure ML
az ml model deploy \
  --name fraud-detection \
  --model fraud-detection:1 \
  --compute-target aks-cluster
```

### 4. Configure Monitoring

```bash
# Set up alerts
az monitor metrics alert create \
  --name "High-GPU-Usage" \
  --resource-group rg-prod-eus2-ai-01 \
  --scopes /subscriptions/{sub-id}/resourceGroups/rg-prod-eus2-ai-01 \
  --condition "avg GPU Utilization > 90" \
  --window-size 5m \
  --evaluation-frequency 1m
```

## Troubleshooting

### Issue: Private endpoint connection failed
**Solution**: Verify NSG rules and private DNS zones

### Issue: ML workspace deployment timeout
**Solution**: Check VNet delegation and subnet configuration

### Issue: Azure OpenAI quota exceeded
**Solution**: Request quota increase via Azure Portal

## Next Steps

1. Configure CI/CD pipelines for ML models
2. Set up data governance policies
3. Implement model monitoring
4. Configure disaster recovery
5. Train operations team

## Support

For issues or questions:
- GitHub Issues: [Create an issue](https://github.com/appliedailearner/azure-landing-zones-project/issues)
- Documentation: [Main README](../../../README.md)
