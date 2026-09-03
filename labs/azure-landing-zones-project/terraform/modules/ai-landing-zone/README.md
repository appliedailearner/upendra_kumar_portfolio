# AI Landing Zone Terraform Module

This module deploys an enterprise-grade AI Landing Zone for Azure, following Microsoft Cloud Adoption Framework and Azure Verified Modules patterns.

## Features

- ✅ Azure OpenAI Service with private endpoints
- ✅ Azure Machine Learning workspace with managed VNet
- ✅ Data Lake Storage Gen2 with encryption
- ✅ Azure Key Vault for secrets management
- ✅ Container Registry for ML images
- ✅ Log Analytics and Application Insights
- ✅ Network security (NSGs, private endpoints)
- ✅ RBAC and managed identities
- ✅ Compliance controls (PCI-DSS, SOC 2, HIPAA)

## Usage

```hcl
module "ai_landing_zone" {
  source = "../../modules/ai-landing-zone"

  # Required variables
  resource_group_name = "rg-prod-eus2-ai-01"
  location            = "eastus2"
  environment         = "prod"
  
  # Network configuration
  vnet_address_space = ["10.100.0.0/16"]
  
  # Compliance requirements
  industry_compliance = {
    pci_dss = true
    hipaa   = false
    sox     = false
    gdpr    = true
  }
  
  # Cost tier
  cost_tier = "standard"  # minimal, standard, premium
  
  # Tags
  tags = {
    Environment = "Production"
    CostCenter  = "AI-Platform"
    Owner       = "data-science-team"
    Compliance  = "PCI-DSS,SOC2"
  }
}
```

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.6.0 |
| azurerm | >= 3.80.0 |
| azuread | >= 2.45.0 |

## Providers

| Name | Version |
|------|---------|
| azurerm | >= 3.80.0 |
| azuread | >= 2.45.0 |

## Resources Created

### Core AI Services
- Azure OpenAI Service (primary and secondary regions)
- Azure Machine Learning workspace
- Azure Container Registry
- Azure Key Vault

### Storage
- Azure Data Lake Storage Gen2 (raw, curated, feature zones)
- Blob storage for model artifacts

### Networking
- Virtual Network with subnets
- Private endpoints for all PaaS services
- Network Security Groups
- Private DNS zones

### Monitoring
- Log Analytics workspace
- Application Insights
- Azure Monitor alerts

### Security
- Managed identities
- RBAC role assignments
- Customer-managed encryption keys

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| resource_group_name | Name of the resource group | `string` | n/a | yes |
| location | Azure region | `string` | n/a | yes |
| environment | Environment (dev, staging, prod) | `string` | n/a | yes |
| vnet_address_space | VNet address space | `list(string)` | n/a | yes |
| industry_compliance | Compliance requirements | `object` | See below | no |
| cost_tier | Cost optimization tier | `string` | `"standard"` | no |
| enable_azure_openai | Deploy Azure OpenAI | `bool` | `true` | no |
| enable_ml_workspace | Deploy ML workspace | `bool` | `true` | no |
| tags | Resource tags | `map(string)` | `{}` | no |

### Industry Compliance Object

```hcl
industry_compliance = {
  pci_dss = bool  # Payment Card Industry Data Security Standard
  hipaa   = bool  # Health Insurance Portability and Accountability Act
  sox     = bool  # Sarbanes-Oxley Act
  gdpr    = bool  # General Data Protection Regulation
}
```

## Outputs

| Name | Description |
|------|-------------|
| ml_workspace_id | Azure ML workspace resource ID |
| ml_workspace_name | Azure ML workspace name |
| azure_openai_endpoint | Azure OpenAI endpoint URL |
| storage_account_id | Data Lake storage account ID |
| key_vault_id | Key Vault resource ID |
| vnet_id | Virtual Network ID |
| resource_group_name | Resource group name |

## Examples

See the `examples/` directory for complete examples:
- [Financial Services](../../examples/financial-services/)
- [Healthcare](../../examples/healthcare/)
- [Manufacturing](../../examples/manufacturing/)

## Cost Estimation

### Standard Tier (Monthly)
- Azure OpenAI: ~$460
- ML Workspace Compute: ~$2,400
- Storage: ~$1,228
- Networking: ~$250
- Monitoring: ~$365
- **Total**: ~$4,703/month

### Cost Optimization
- Use Reserved Instances for 40% savings on compute
- Enable autoscaling to reduce idle costs
- Implement storage lifecycle policies

## Security Considerations

### Network Security
- All resources deployed with private endpoints
- No public IP addresses
- NSG rules restrict traffic
- Azure Firewall integration supported

### Data Protection
- Customer-managed keys (CMK) for encryption
- TLS 1.3 for data in transit
- Immutable storage for compliance data

### Identity & Access
- Managed identities for service-to-service auth
- Azure AD integration with MFA
- RBAC with least privilege
- PIM for admin access

## Compliance

This module helps meet the following compliance requirements:

- **PCI-DSS v4.0**: Network segmentation, encryption, access control
- **SOC 2 Type II**: Security, availability, confidentiality controls
- **HIPAA**: PHI protection, audit logging, encryption
- **GDPR**: Data residency, right to erasure, consent management

## Contributing

See [CONTRIBUTING.md](../../../.github/CONTRIBUTING.md) for guidelines.

## License

See [LICENSE](../../../LICENSE) for details.

## Support

For issues and questions:
- GitHub Issues: https://github.com/appliedailearner/azure-landing-zones-project/issues
- Documentation: [Main README](../../../README.md)
