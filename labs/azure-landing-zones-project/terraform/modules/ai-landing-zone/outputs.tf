# Core Resource Outputs

output "resource_group_name" {
  description = "Name of the resource group"
  value       = azurerm_resource_group.ai_lz.name
}

output "resource_group_id" {
  description = "ID of the resource group"
  value       = azurerm_resource_group.ai_lz.id
}

output "location" {
  description = "Azure region where resources are deployed"
  value       = azurerm_resource_group.ai_lz.location
}

# Networking Outputs

output "vnet_id" {
  description = "ID of the AI Landing Zone VNet"
  value       = azurerm_virtual_network.ai_vnet.id
}

output "vnet_name" {
  description = "Name of the AI Landing Zone VNet"
  value       = azurerm_virtual_network.ai_vnet.name
}

output "subnet_ids" {
  description = "Map of subnet names to IDs"
  value = {
    ml_workspace      = azurerm_subnet.ml_workspace.id
    compute           = azurerm_subnet.compute.id
    private_endpoints = azurerm_subnet.private_endpoints.id
    data              = azurerm_subnet.data.id
  }
}

# Storage Outputs

output "storage_account_id" {
  description = "ID of the Data Lake storage account"
  value       = azurerm_storage_account.datalake.id
}

output "storage_account_name" {
  description = "Name of the Data Lake storage account"
  value       = azurerm_storage_account.datalake.name
}

output "storage_primary_blob_endpoint" {
  description = "Primary blob endpoint of the storage account"
  value       = azurerm_storage_account.datalake.primary_blob_endpoint
}

output "storage_primary_dfs_endpoint" {
  description = "Primary DFS endpoint of the storage account"
  value       = azurerm_storage_account.datalake.primary_dfs_endpoint
}

# Key Vault Outputs

output "key_vault_id" {
  description = "ID of the Key Vault"
  value       = azurerm_key_vault.ai_kv.id
}

output "key_vault_name" {
  description = "Name of the Key Vault"
  value       = azurerm_key_vault.ai_kv.name
}

output "key_vault_uri" {
  description = "URI of the Key Vault"
  value       = azurerm_key_vault.ai_kv.vault_uri
}

# Machine Learning Outputs

output "ml_workspace_id" {
  description = "ID of the Azure ML workspace"
  value       = var.enable_ml_workspace ? azurerm_machine_learning_workspace.ml_workspace[0].id : null
}

output "ml_workspace_name" {
  description = "Name of the Azure ML workspace"
  value       = var.enable_ml_workspace ? azurerm_machine_learning_workspace.ml_workspace[0].name : null
}

output "ml_workspace_discovery_url" {
  description = "Discovery URL of the Azure ML workspace"
  value       = var.enable_ml_workspace ? azurerm_machine_learning_workspace.ml_workspace[0].discovery_url : null
}

# Azure OpenAI Outputs

output "azure_openai_id" {
  description = "ID of the Azure OpenAI service"
  value       = var.enable_azure_openai ? azurerm_cognitive_account.openai[0].id : null
}

output "azure_openai_name" {
  description = "Name of the Azure OpenAI service"
  value       = var.enable_azure_openai ? azurerm_cognitive_account.openai[0].name : null
}

output "azure_openai_endpoint" {
  description = "Endpoint URL of the Azure OpenAI service"
  value       = var.enable_azure_openai ? azurerm_cognitive_account.openai[0].endpoint : null
}

# Container Registry Outputs

output "container_registry_id" {
  description = "ID of the Container Registry"
  value       = var.enable_ml_workspace ? azurerm_container_registry.acr[0].id : null
}

output "container_registry_name" {
  description = "Name of the Container Registry"
  value       = var.enable_ml_workspace ? azurerm_container_registry.acr[0].name : null
}

output "container_registry_login_server" {
  description = "Login server of the Container Registry"
  value       = var.enable_ml_workspace ? azurerm_container_registry.acr[0].login_server : null
}

# Monitoring Outputs

output "log_analytics_workspace_id" {
  description = "ID of the Log Analytics workspace"
  value       = azurerm_log_analytics_workspace.law.id
}

output "log_analytics_workspace_name" {
  description = "Name of the Log Analytics workspace"
  value       = azurerm_log_analytics_workspace.law.name
}

output "application_insights_id" {
  description = "ID of Application Insights"
  value       = azurerm_application_insights.appinsights.id
}

output "application_insights_instrumentation_key" {
  description = "Instrumentation key of Application Insights"
  value       = azurerm_application_insights.appinsights.instrumentation_key
  sensitive   = true
}

output "application_insights_connection_string" {
  description = "Connection string of Application Insights"
  value       = azurerm_application_insights.appinsights.connection_string
  sensitive   = true
}

# Private Endpoint Outputs

output "private_endpoint_ids" {
  description = "Map of private endpoint names to IDs"
  value = {
    storage_blob = azurerm_private_endpoint.storage_blob.id
    storage_dfs  = azurerm_private_endpoint.storage_dfs.id
    key_vault    = azurerm_private_endpoint.key_vault.id
    openai       = var.enable_azure_openai ? azurerm_private_endpoint.openai[0].id : null
  }
}

# Managed Identity Outputs

output "ml_workspace_identity_principal_id" {
  description = "Principal ID of the ML workspace managed identity"
  value       = var.enable_ml_workspace ? azurerm_machine_learning_workspace.ml_workspace[0].identity[0].principal_id : null
}

output "openai_identity_principal_id" {
  description = "Principal ID of the Azure OpenAI managed identity"
  value       = var.enable_azure_openai ? azurerm_cognitive_account.openai[0].identity[0].principal_id : null
}

# Compliance Outputs

output "compliance_tags" {
  description = "Compliance-related tags applied to resources"
  value = {
    pci_dss = var.industry_compliance.pci_dss
    hipaa   = var.industry_compliance.hipaa
    sox     = var.industry_compliance.sox
    gdpr    = var.industry_compliance.gdpr
  }
}

output "encryption_enabled" {
  description = "Encryption status of resources"
  value = {
    storage_encryption = "AES-256"
    key_vault_sku      = azurerm_key_vault.ai_kv.sku_name
    tls_version        = "TLS1_3"
  }
}

# Cost Outputs

output "cost_tier" {
  description = "Cost tier used for deployment"
  value       = var.cost_tier
}

output "estimated_monthly_cost_usd" {
  description = "Estimated monthly cost in USD (approximate)"
  value = var.cost_tier == "minimal" ? 3000 : (var.cost_tier == "standard" ? 12000 : 25000)
}
