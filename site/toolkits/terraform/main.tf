terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "rg-ai-hosting-toolkit"
  location = "East US"
}

# 1. Virtual Network & Subnets
resource "azurerm_virtual_network" "vnet" {
  name                = "vnet-ai-hosting"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_subnet" "snet_infra" {
  name                 = "snet-aca-infra"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.0.0/23"]
}

resource "azurerm_subnet" "snet_pe" {
  name                 = "snet-private-endpoints"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.2.0/24"]
}

# 2. Azure Container Apps Environment (VNet Integrated)
resource "azurerm_container_app_environment" "env" {
  name                           = "aca-env-ai-hosting"
  location                       = azurerm_resource_group.rg.location
  resource_group_name            = azurerm_resource_group.rg.name
  infrastructure_subnet_id       = azurerm_subnet.snet_infra.id
  internal_load_balancer_enabled = true # Crucial for Private Access
}

# 3. Azure OpenAI Service 
resource "azurerm_cognitive_account" "openai" {
  name                          = "oai-ai-hosting-demo"
  location                      = azurerm_resource_group.rg.location
  resource_group_name           = azurerm_resource_group.rg.name
  kind                          = "OpenAI"
  sku_name                      = "S0"
  public_network_access_enabled = false # Secure by default
  custom_subdomain_name         = "oai-ai-hosting-demo"
}

# 4. Private Endpoint for OpenAI
resource "azurerm_private_endpoint" "pe_openai" {
  name                = "pe-openai"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  subnet_id           = azurerm_subnet.snet_pe.id

  private_service_connection {
    name                           = "psc-openai"
    private_connection_resource_id = azurerm_cognitive_account.openai.id
    subresource_names              = ["account"]
    is_manual_connection           = false
  }
}

# 5. Private DNS Zone
resource "azurerm_private_dns_zone" "dns_openai" {
  name                = "privatelink.openai.azure.com"
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_private_dns_zone_virtual_network_link" "vnet_link" {
  name                  = "vnet-link"
  resource_group_name   = azurerm_resource_group.rg.name
  private_dns_zone_name = azurerm_private_dns_zone.dns_openai.name
  virtual_network_id    = azurerm_virtual_network.vnet.id
}
