# Required Variables

variable "resource_group_name" {
  description = "Name of the resource group for AI Landing Zone resources"
  type        = string
  validation {
    condition     = length(var.resource_group_name) > 0 && length(var.resource_group_name) <= 90
    error_message = "Resource group name must be between 1 and 90 characters"
  }
}

variable "location" {
  description = "Azure region for resources"
  type        = string
  validation {
    condition     = contains(["eastus2", "westus2", "northeurope", "westeurope"], var.location)
    error_message = "Location must be one of: eastus2, westus2, northeurope, westeurope"
  }
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod"
  }
}

variable "vnet_address_space" {
  description = "Address space for the AI Landing Zone VNet"
  type        = list(string)
  validation {
    condition     = length(var.vnet_address_space) > 0
    error_message = "At least one address space must be provided"
  }
}

# Optional Variables

variable "location_short" {
  description = "Short name for location (e.g., eus2 for eastus2)"
  type        = string
  default     = "eus2"
}

variable "industry_compliance" {
  description = "Industry compliance requirements"
  type = object({
    pci_dss = bool
    hipaa   = bool
    sox     = bool
    gdpr    = bool
  })
  default = {
    pci_dss = false
    hipaa   = false
    sox     = false
    gdpr    = true
  }
}

variable "cost_tier" {
  description = "Cost optimization tier (minimal, standard, premium)"
  type        = string
  default     = "standard"
  validation {
    condition     = contains(["minimal", "standard", "premium"], var.cost_tier)
    error_message = "Cost tier must be minimal, standard, or premium"
  }
}

variable "enable_azure_openai" {
  description = "Enable Azure OpenAI Service deployment"
  type        = bool
  default     = true
}

variable "enable_ml_workspace" {
  description = "Enable Azure Machine Learning workspace deployment"
  type        = bool
  default     = true
}

variable "hub_vnet_address_space" {
  description = "Address space of hub VNet for NSG rules (optional)"
  type        = string
  default     = null
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}

# Advanced Configuration

variable "ml_compute_config" {
  description = "Machine Learning compute cluster configuration"
  type = object({
    cpu_cluster_enabled     = bool
    cpu_cluster_min_nodes   = number
    cpu_cluster_max_nodes   = number
    cpu_cluster_vm_size     = string
    gpu_cluster_enabled     = bool
    gpu_cluster_min_nodes   = number
    gpu_cluster_max_nodes   = number
    gpu_cluster_vm_size     = string
  })
  default = {
    cpu_cluster_enabled   = true
    cpu_cluster_min_nodes = 0
    cpu_cluster_max_nodes = 50
    cpu_cluster_vm_size   = "Standard_D4s_v3"
    gpu_cluster_enabled   = true
    gpu_cluster_min_nodes = 0
    gpu_cluster_max_nodes = 20
    gpu_cluster_vm_size   = "Standard_NC6s_v3"
  }
}

variable "openai_deployments" {
  description = "Azure OpenAI model deployments"
  type = list(object({
    name          = string
    model_name    = string
    model_version = string
    sku_name      = string
    sku_capacity  = number
  }))
  default = [
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
}

variable "storage_lifecycle_rules" {
  description = "Storage lifecycle management rules"
  type = list(object({
    name                       = string
    prefix_match               = list(string)
    tier_to_cool_after_days    = number
    tier_to_archive_after_days = number
    delete_after_days          = number
  }))
  default = [
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
}

variable "enable_private_dns_zones" {
  description = "Create private DNS zones for private endpoints"
  type        = bool
  default     = true
}

variable "private_dns_zone_ids" {
  description = "Existing private DNS zone IDs (if not creating new ones)"
  type = object({
    blob_dns_zone_id      = string
    dfs_dns_zone_id       = string
    vault_dns_zone_id     = string
    openai_dns_zone_id    = string
    azureml_api_dns_zone_id = string
    azureml_notebooks_dns_zone_id = string
  })
  default = null
}

variable "log_analytics_retention_days" {
  description = "Log Analytics workspace retention in days"
  type        = number
  default     = 90
  validation {
    condition     = var.log_analytics_retention_days >= 30 && var.log_analytics_retention_days <= 730
    error_message = "Retention must be between 30 and 730 days"
  }
}

variable "enable_diagnostic_settings" {
  description = "Enable diagnostic settings for all resources"
  type        = bool
  default     = true
}

variable "enable_monitoring_alerts" {
  description = "Enable Azure Monitor alerts"
  type        = bool
  default     = true
}

variable "alert_email_addresses" {
  description = "Email addresses for alert notifications"
  type        = list(string)
  default     = []
}
