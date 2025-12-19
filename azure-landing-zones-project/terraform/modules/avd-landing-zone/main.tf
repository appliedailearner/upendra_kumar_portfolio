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
  }
}

# Data sources
data "azurerm_client_config" "current" {}

# Resource Group
resource "azurerm_resource_group" "avd" {
  name     = var.resource_group_name
  location = var.location
  tags     = var.tags
}

# Virtual Network
resource "azurerm_virtual_network" "avd_vnet" {
  name                = "vnet-${var.environment}-${var.location_short}-avd-spoke"
  location            = azurerm_resource_group.avd.location
  resource_group_name = azurerm_resource_group.avd.name
  address_space       = var.vnet_address_space
  tags                = var.tags
}

# Subnets
resource "azurerm_subnet" "session_hosts" {
  name                 = "snet-${var.environment}-${var.location_short}-avd-hosts"
  resource_group_name  = azurerm_resource_group.avd.name
  virtual_network_name = azurerm_virtual_network.avd_vnet.name
  address_prefixes     = [cidrsubnet(var.vnet_address_space[0], 8, 1)]
}

resource "azurerm_subnet" "private_endpoints" {
  name                 = "snet-${var.environment}-${var.location_short}-avd-pe"
  resource_group_name  = azurerm_resource_group.avd.name
  virtual_network_name = azurerm_virtual_network.avd_vnet.name
  address_prefixes     = [cidrsubnet(var.vnet_address_space[0], 8, 2)]
}

# NSG for Session Hosts
resource "azurerm_network_security_group" "session_hosts" {
  name                = "nsg-${var.environment}-${var.location_short}-avd-hosts"
  location            = azurerm_resource_group.avd.location
  resource_group_name = azurerm_resource_group.avd.name
  tags                = var.tags

  security_rule {
    name                       = "Allow-RDP-From-Hub"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "3389"
    source_address_prefix      = var.hub_vnet_address_space != null ? var.hub_vnet_address_space : "10.0.0.0/16"
    destination_address_prefix = azurerm_subnet.session_hosts.address_prefixes[0]
  }
}

resource "azurerm_subnet_network_security_group_association" "session_hosts" {
  subnet_id                 = azurerm_subnet.session_hosts.id
  network_security_group_id = azurerm_network_security_group.session_hosts.id
}

# Storage Account for FSLogix
resource "azurerm_storage_account" "fslogix" {
  name                     = "st${var.environment}${var.location_short}avdfslogix"
  resource_group_name      = azurerm_resource_group.avd.name
  location                 = azurerm_resource_group.avd.location
  account_tier             = "Premium"
  account_replication_type = "LRS"
  account_kind             = "FileStorage"
  min_tls_version          = "TLS1_3"
  
  public_network_access_enabled = false
  
  azure_files_authentication {
    directory_type = "AADDS"
  }
  
  tags = var.tags
}

# File Share for FSLogix Profiles
resource "azurerm_storage_share" "profiles" {
  name                 = "profiles"
  storage_account_name = azurerm_storage_account.fslogix.name
  quota                = var.fslogix_config.quota_gb
}

# AVD Host Pool
resource "azurerm_virtual_desktop_host_pool" "pool" {
  name                = "vdpool-${var.environment}-${var.location_short}-01"
  location            = azurerm_resource_group.avd.location
  resource_group_name = azurerm_resource_group.avd.name
  
  type               = var.host_pool_config.type
  load_balancer_type = var.host_pool_config.load_balancer_type
  maximum_sessions_allowed = var.host_pool_config.max_session_limit
  
  start_vm_on_connect = true
  
  tags = var.tags
}

# AVD Application Group
resource "azurerm_virtual_desktop_application_group" "desktop" {
  name                = "vdag-${var.environment}-${var.location_short}-desktop"
  location            = azurerm_resource_group.avd.location
  resource_group_name = azurerm_resource_group.avd.name
  
  type          = "Desktop"
  host_pool_id  = azurerm_virtual_desktop_host_pool.pool.id
  friendly_name = "Desktop Application Group"
  
  tags = var.tags
}

# AVD Workspace
resource "azurerm_virtual_desktop_workspace" "workspace" {
  name                = "vdws-${var.environment}-${var.location_short}-01"
  location            = azurerm_resource_group.avd.location
  resource_group_name = azurerm_resource_group.avd.name
  friendly_name       = "AVD Workspace"
  
  tags = var.tags
}

# Associate Application Group with Workspace
resource "azurerm_virtual_desktop_workspace_application_group_association" "desktop" {
  workspace_id         = azurerm_virtual_desktop_workspace.workspace.id
  application_group_id = azurerm_virtual_desktop_application_group.desktop.id
}

# Log Analytics Workspace
resource "azurerm_log_analytics_workspace" "avd" {
  name                = "log-${var.environment}-${var.location_short}-avd-01"
  location            = azurerm_resource_group.avd.location
  resource_group_name = azurerm_resource_group.avd.name
  sku                 = "PerGB2018"
  retention_in_days   = 90
  tags                = var.tags
}

# Diagnostic Settings for Host Pool
resource "azurerm_monitor_diagnostic_setting" "host_pool" {
  name                       = "diag-host-pool"
  target_resource_id         = azurerm_virtual_desktop_host_pool.pool.id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.avd.id
  
  enabled_log {
    category = "Checkpoint"
  }
  
  enabled_log {
    category = "Error"
  }
  
  enabled_log {
    category = "Management"
  }
  
  enabled_log {
    category = "Connection"
  }
  
  enabled_log {
    category = "HostRegistration"
  }
}
