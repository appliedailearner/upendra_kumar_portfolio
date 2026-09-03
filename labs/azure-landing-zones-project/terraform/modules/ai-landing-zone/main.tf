terraform {
  required_version = ">= 1.6.0"
  
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.80.0"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = ">= 2.45.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.5.0"
    }
  }
}

# Data sources
data "azurerm_client_config" "current" {}

data "azuread_client_config" "current" {}

# Resource Group
resource "azurerm_resource_group" "ai_lz" {
  name     = var.resource_group_name
  location = var.location
  tags     = var.tags
}

# Virtual Network
resource "azurerm_virtual_network" "ai_vnet" {
  name                = "vnet-${var.environment}-${var.location_short}-ai-spoke"
  location            = azurerm_resource_group.ai_lz.location
  resource_group_name = azurerm_resource_group.ai_lz.name
  address_space       = var.vnet_address_space
  tags                = var.tags
}

# Subnets
resource "azurerm_subnet" "ml_workspace" {
  name                 = "snet-${var.environment}-${var.location_short}-ai-ml"
  resource_group_name  = azurerm_resource_group.ai_lz.name
  virtual_network_name = azurerm_virtual_network.ai_vnet.name
  address_prefixes     = [cidrsubnet(var.vnet_address_space[0], 8, 1)]
  
  delegation {
    name = "ml-delegation"
    service_delegation {
      name = "Microsoft.MachineLearningServices/workspaces"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/join/action",
      ]
    }
  }
}

resource "azurerm_subnet" "compute" {
  name                 = "snet-${var.environment}-${var.location_short}-ai-compute"
  resource_group_name  = azurerm_resource_group.ai_lz.name
  virtual_network_name = azurerm_virtual_network.ai_vnet.name
  address_prefixes     = [cidrsubnet(var.vnet_address_space[0], 7, 1)]
}

resource "azurerm_subnet" "private_endpoints" {
  name                 = "snet-${var.environment}-${var.location_short}-ai-pe"
  resource_group_name  = azurerm_resource_group.ai_lz.name
  virtual_network_name = azurerm_virtual_network.ai_vnet.name
  address_prefixes     = [cidrsubnet(var.vnet_address_space[0], 8, 4)]
}

resource "azurerm_subnet" "data" {
  name                 = "snet-${var.environment}-${var.location_short}-ai-data"
  resource_group_name  = azurerm_resource_group.ai_lz.name
  virtual_network_name = azurerm_virtual_network.ai_vnet.name
  address_prefixes     = [cidrsubnet(var.vnet_address_space[0], 8, 5)]
}

# Network Security Groups
resource "azurerm_network_security_group" "ml_workspace" {
  name                = "nsg-${var.environment}-${var.location_short}-ai-ml"
  location            = azurerm_resource_group.ai_lz.location
  resource_group_name = azurerm_resource_group.ai_lz.name
  tags                = var.tags

  security_rule {
    name                       = "Allow-Hub-Inbound"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = var.hub_vnet_address_space != null ? var.hub_vnet_address_space : "10.0.0.0/16"
    destination_address_prefix = azurerm_subnet.ml_workspace.address_prefixes[0]
  }

  security_rule {
    name                       = "Allow-AzureLoadBalancer"
    priority                   = 110
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "AzureLoadBalancer"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "Deny-All-Inbound"
    priority                   = 4096
    direction                  = "Inbound"
    access                     = "Deny"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

resource "azurerm_subnet_network_security_group_association" "ml_workspace" {
  subnet_id                 = azurerm_subnet.ml_workspace.id
  network_security_group_id = azurerm_network_security_group.ml_workspace.id
}

# Storage Account for Data Lake
resource "azurerm_storage_account" "datalake" {
  name                     = "st${var.environment}${var.location_short}aidatalake"
  resource_group_name      = azurerm_resource_group.ai_lz.name
  location                 = azurerm_resource_group.ai_lz.location
  account_tier             = var.cost_tier == "minimal" ? "Standard" : "Premium"
  account_replication_type = var.cost_tier == "minimal" ? "LRS" : "ZRS"
  account_kind             = "StorageV2"
  is_hns_enabled           = true
  min_tls_version          = "TLS1_3"
  
  public_network_access_enabled = false
  
  blob_properties {
    versioning_enabled = true
    
    delete_retention_policy {
      days = 30
    }
  }
  
  network_rules {
    default_action             = "Deny"
    bypass                     = ["AzureServices"]
    virtual_network_subnet_ids = [azurerm_subnet.data.id, azurerm_subnet.ml_workspace.id]
  }
  
  tags = var.tags
}

# Storage Containers
resource "azurerm_storage_container" "raw" {
  name                  = "raw"
  storage_account_name  = azurerm_storage_account.datalake.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "curated" {
  name                  = "curated"
  storage_account_name  = azurerm_storage_account.datalake.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "models" {
  name                  = "models"
  storage_account_name  = azurerm_storage_account.datalake.name
  container_access_type = "private"
}

# Key Vault
resource "azurerm_key_vault" "ai_kv" {
  name                       = "kv-${var.environment}-${var.location_short}-ai-01"
  location                   = azurerm_resource_group.ai_lz.location
  resource_group_name        = azurerm_resource_group.ai_lz.name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = var.industry_compliance.pci_dss || var.industry_compliance.hipaa ? "premium" : "standard"
  soft_delete_retention_days = 90
  purge_protection_enabled   = var.industry_compliance.pci_dss || var.industry_compliance.hipaa
  
  public_network_access_enabled = false
  
  network_acls {
    default_action             = "Deny"
    bypass                     = "AzureServices"
    virtual_network_subnet_ids = [azurerm_subnet.ml_workspace.id]
  }
  
  tags = var.tags
}

# Container Registry
resource "azurerm_container_registry" "acr" {
  count               = var.enable_ml_workspace ? 1 : 0
  name                = "acr${var.environment}${var.location_short}ai01"
  resource_group_name = azurerm_resource_group.ai_lz.name
  location            = azurerm_resource_group.ai_lz.location
  sku                 = var.cost_tier == "minimal" ? "Basic" : "Premium"
  admin_enabled       = false
  
  public_network_access_enabled = false
  
  tags = var.tags
}

# Log Analytics Workspace
resource "azurerm_log_analytics_workspace" "law" {
  name                = "log-${var.environment}-${var.location_short}-ai-01"
  location            = azurerm_resource_group.ai_lz.location
  resource_group_name = azurerm_resource_group.ai_lz.name
  sku                 = "PerGB2018"
  retention_in_days   = var.industry_compliance.pci_dss || var.industry_compliance.hipaa ? 730 : 90
  tags                = var.tags
}

# Application Insights
resource "azurerm_application_insights" "appinsights" {
  name                = "appi-${var.environment}-${var.location_short}-ai-01"
  location            = azurerm_resource_group.ai_lz.location
  resource_group_name = azurerm_resource_group.ai_lz.name
  workspace_id        = azurerm_log_analytics_workspace.law.id
  application_type    = "web"
  tags                = var.tags
}

# Azure Machine Learning Workspace
resource "azurerm_machine_learning_workspace" "ml_workspace" {
  count               = var.enable_ml_workspace ? 1 : 0
  name                = "aml-${var.environment}-${var.location_short}-ai-01"
  location            = azurerm_resource_group.ai_lz.location
  resource_group_name = azurerm_resource_group.ai_lz.name
  
  application_insights_id = azurerm_application_insights.appinsights.id
  key_vault_id            = azurerm_key_vault.ai_kv.id
  storage_account_id      = azurerm_storage_account.datalake.id
  container_registry_id   = azurerm_container_registry.acr[0].id
  
  identity {
    type = "SystemAssigned"
  }
  
  public_network_access_enabled = false
  
  managed_network {
    isolation_mode = "AllowOnlyApprovedOutbound"
  }
  
  tags = var.tags
}

# Azure OpenAI Service
resource "azurerm_cognitive_account" "openai" {
  count               = var.enable_azure_openai ? 1 : 0
  name                = "aoai-${var.environment}-${var.location_short}-ai-01"
  location            = azurerm_resource_group.ai_lz.location
  resource_group_name = azurerm_resource_group.ai_lz.name
  kind                = "OpenAI"
  sku_name            = "S0"
  
  custom_subdomain_name         = "aoai-${var.environment}-${var.location_short}-ai-01"
  public_network_access_enabled = false
  
  network_acls {
    default_action = "Deny"
    virtual_network_rules {
      subnet_id = azurerm_subnet.ml_workspace.id
    }
  }
  
  identity {
    type = "SystemAssigned"
  }
  
  tags = var.tags
}

# Private Endpoints
resource "azurerm_private_endpoint" "storage_blob" {
  name                = "pe-${var.environment}-${var.location_short}-storage-blob"
  location            = azurerm_resource_group.ai_lz.location
  resource_group_name = azurerm_resource_group.ai_lz.name
  subnet_id           = azurerm_subnet.private_endpoints.id
  
  private_service_connection {
    name                           = "psc-storage-blob"
    private_connection_resource_id = azurerm_storage_account.datalake.id
    is_manual_connection           = false
    subresource_names              = ["blob"]
  }
  
  tags = var.tags
}

resource "azurerm_private_endpoint" "storage_dfs" {
  name                = "pe-${var.environment}-${var.location_short}-storage-dfs"
  location            = azurerm_resource_group.ai_lz.location
  resource_group_name = azurerm_resource_group.ai_lz.name
  subnet_id           = azurerm_subnet.private_endpoints.id
  
  private_service_connection {
    name                           = "psc-storage-dfs"
    private_connection_resource_id = azurerm_storage_account.datalake.id
    is_manual_connection           = false
    subresource_names              = ["dfs"]
  }
  
  tags = var.tags
}

resource "azurerm_private_endpoint" "key_vault" {
  name                = "pe-${var.environment}-${var.location_short}-keyvault"
  location            = azurerm_resource_group.ai_lz.location
  resource_group_name = azurerm_resource_group.ai_lz.name
  subnet_id           = azurerm_subnet.private_endpoints.id
  
  private_service_connection {
    name                           = "psc-keyvault"
    private_connection_resource_id = azurerm_key_vault.ai_kv.id
    is_manual_connection           = false
    subresource_names              = ["vault"]
  }
  
  tags = var.tags
}

resource "azurerm_private_endpoint" "openai" {
  count               = var.enable_azure_openai ? 1 : 0
  name                = "pe-${var.environment}-${var.location_short}-openai"
  location            = azurerm_resource_group.ai_lz.location
  resource_group_name = azurerm_resource_group.ai_lz.name
  subnet_id           = azurerm_subnet.private_endpoints.id
  
  private_service_connection {
    name                           = "psc-openai"
    private_connection_resource_id = azurerm_cognitive_account.openai[0].id
    is_manual_connection           = false
    subresource_names              = ["account"]
  }
  
  tags = var.tags
}

# Diagnostic Settings
resource "azurerm_monitor_diagnostic_setting" "ml_workspace" {
  count                      = var.enable_ml_workspace ? 1 : 0
  name                       = "diag-ml-workspace"
  target_resource_id         = azurerm_machine_learning_workspace.ml_workspace[0].id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.law.id
  
  enabled_log {
    category = "AmlComputeClusterEvent"
  }
  
  enabled_log {
    category = "AmlComputeJobEvent"
  }
  
  metric {
    category = "AllMetrics"
    enabled  = true
  }
}
