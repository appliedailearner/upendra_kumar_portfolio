# Scenario 1: Internal-Only Agents (Regulated Enterprise)
# Private-only entry, private endpoints for model and data, egress controlled

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.80"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = "~> 2.45"
    }
  }
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy = true
    }
  }
}

# Variables
variable "location" {
  description = "Azure region"
  type        = string
  default     = "eastus2"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "prod"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "ai-agents"
}

variable "apim_sku" {
  description = "APIM SKU (Developer, Premium)"
  type        = string
  default     = "Developer"
}

variable "openai_sku" {
  description = "Azure OpenAI SKU"
  type        = string
  default     = "S0"
}

variable "enable_private_endpoints" {
  description = "Enable private endpoints"
  type        = bool
  default     = true
}

# Locals
locals {
  resource_suffix = "${var.project_name}-${var.environment}"
  tags = {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "Terraform"
    Scenario    = "internal-only"
  }
}

# Resource Group
resource "azurerm_resource_group" "main" {
  name     = "rg-${local.resource_suffix}"
  location = var.location
  tags     = local.tags
}

# Virtual Network
resource "azurerm_virtual_network" "main" {
  name                = "vnet-${local.resource_suffix}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  address_space       = ["10.0.0.0/16"]
  tags                = local.tags
}

# Subnets
resource "azurerm_subnet" "apim" {
  name                 = "snet-apim"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_subnet" "aca" {
  name                 = "snet-aca"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.2.0/23"]

  delegation {
    name = "aca-delegation"
    service_delegation {
      name = "Microsoft.App/environments"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/join/action"
      ]
    }
  }
}

resource "azurerm_subnet" "private_endpoints" {
  name                 = "snet-private-endpoints"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.4.0/24"]
}

# Private DNS Zones
resource "azurerm_private_dns_zone" "openai" {
  count               = var.enable_private_endpoints ? 1 : 0
  name                = "privatelink.openai.azure.com"
  resource_group_name = azurerm_resource_group.main.name
  tags                = local.tags
}

resource "azurerm_private_dns_zone_virtual_network_link" "openai" {
  count                 = var.enable_private_endpoints ? 1 : 0
  name                  = "vnet-link-openai"
  resource_group_name   = azurerm_resource_group.main.name
  private_dns_zone_name = azurerm_private_dns_zone.openai[0].name
  virtual_network_id    = azurerm_virtual_network.main.id
  tags                  = local.tags
}

# Azure OpenAI
resource "azurerm_cognitive_account" "openai" {
  name                = "oai-${local.resource_suffix}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  kind                = "OpenAI"
  sku_name            = var.openai_sku

  public_network_access_enabled = !var.enable_private_endpoints

  network_acls {
    default_action = var.enable_private_endpoints ? "Deny" : "Allow"
  }

  tags = local.tags
}

# Private Endpoint for Azure OpenAI
resource "azurerm_private_endpoint" "openai" {
  count               = var.enable_private_endpoints ? 1 : 0
  name                = "pe-openai-${local.resource_suffix}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  subnet_id           = azurerm_subnet.private_endpoints.id

  private_service_connection {
    name                           = "psc-openai"
    private_connection_resource_id = azurerm_cognitive_account.openai.id
    is_manual_connection           = false
    subresource_names              = ["account"]
  }

  private_dns_zone_group {
    name                 = "pdz-group-openai"
    private_dns_zone_ids = [azurerm_private_dns_zone.openai[0].id]
  }

  tags = local.tags
}

# API Management (Internal Mode)
resource "azurerm_api_management" "main" {
  name                = "apim-${local.resource_suffix}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  publisher_name      = var.project_name
  publisher_email     = "admin@${var.project_name}.com"
  sku_name            = "${var.apim_sku}_1"

  virtual_network_type = "Internal"

  virtual_network_configuration {
    subnet_id = azurerm_subnet.apim.id
  }

  identity {
    type = "SystemAssigned"
  }

  tags = local.tags
}

# Container Apps Environment
resource "azurerm_container_app_environment" "main" {
  name                           = "cae-${local.resource_suffix}"
  location                       = azurerm_resource_group.main.location
  resource_group_name            = azurerm_resource_group.main.name
  infrastructure_subnet_id       = azurerm_subnet.aca.id
  internal_load_balancer_enabled = true

  tags = local.tags
}

# Key Vault
resource "azurerm_key_vault" "main" {
  name                = "kv-${local.resource_suffix}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"

  public_network_access_enabled = !var.enable_private_endpoints

  network_acls {
    default_action = var.enable_private_endpoints ? "Deny" : "Allow"
    bypass         = "AzureServices"
  }

  tags = local.tags
}

# Application Insights
resource "azurerm_application_insights" "main" {
  name                = "appi-${local.resource_suffix}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  application_type    = "web"

  tags = local.tags
}

# Data sources
data "azurerm_client_config" "current" {}

# Outputs
output "resource_group_name" {
  value = azurerm_resource_group.main.name
}

output "apim_name" {
  value = azurerm_api_management.main.name
}

output "apim_gateway_url" {
  value = azurerm_api_management.main.gateway_url
}

output "openai_endpoint" {
  value = azurerm_cognitive_account.openai.endpoint
}

output "container_app_environment_id" {
  value = azurerm_container_app_environment.main.id
}

output "key_vault_uri" {
  value = azurerm_key_vault.main.vault_uri
}

output "application_insights_instrumentation_key" {
  value     = azurerm_application_insights.main.instrumentation_key
  sensitive = true
}
