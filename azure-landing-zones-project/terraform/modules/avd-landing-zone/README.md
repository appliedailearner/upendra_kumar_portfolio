# AVD Landing Zone Terraform Module

Enterprise-grade Azure Virtual Desktop deployment for secure remote access.

## Features

- ✅ Multi-session Windows 11 host pools
- ✅ FSLogix profile management with Azure Files Premium
- ✅ Conditional Access and MFA enforcement
- ✅ Session recording for compliance
- ✅ Azure Monitor for AVD insights
- ✅ Autoscaling with "Start VM on Connect"
- ✅ MSIX App Attach for application delivery

## Usage

```hcl
module "avd_landing_zone" {
  source = "../../modules/avd-landing-zone"

  resource_group_name = "rg-prod-eus2-avd-01"
  location            = "eastus2"
  environment         = "prod"
  
  vnet_address_space = ["10.200.0.0/16"]
  
  host_pool_config = {
    type               = "Pooled"
    load_balancer_type = "BreadthFirst"
    max_session_limit  = 10
  }
  
  session_host_config = {
    vm_size       = "Standard_D4s_v5"
    vm_count      = 10
    image_sku     = "win11-22h2-avd"
  }
  
  fslogix_config = {
    storage_sku = "Premium_LRS"
    quota_gb    = 50
  }
  
  compliance = {
    session_recording = true
    mfa_required     = true
  }
}
```

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|----------|
| resource_group_name | Resource group name | string | yes |
| location | Azure region | string | yes |
| environment | Environment (dev/staging/prod) | string | yes |
| vnet_address_space | VNet address space | list(string) | yes |
| host_pool_config | Host pool configuration | object | no |
| session_host_config | Session host configuration | object | no |
| fslogix_config | FSLogix configuration | object | no |

## Outputs

| Name | Description |
|------|-------------|
| host_pool_id | AVD host pool ID |
| workspace_id | AVD workspace ID |
| storage_account_id | FSLogix storage account ID |

## Cost Estimate

**Monthly Cost (Standard Configuration)**:
- Host Pool VMs (10x D4s_v5): $3,650
- Azure Files Premium (500 GB): $102
- Networking: $150
- Monitoring: $100
- **Total**: ~$4,002/month

## Example

See [examples/avd-financial-services](../../examples/avd-financial-services/) for complete configuration.
