resource "azurerm_resource_group" "spoke" {
  name     = "${var.prefix}-${var.environment}-rg"
  location = var.location
}

resource "azurerm_virtual_network" "spoke" {
  name                = "vnet-${var.environment}-${var.location}-spoke"
  location            = azurerm_resource_group.spoke.location
  resource_group_name = azurerm_resource_group.spoke.name
  address_space       = [var.vnet_address_space]
}

resource "azurerm_subnet" "aks" {
  name                 = "snet-aks-nodes"
  resource_group_name  = azurerm_resource_group.spoke.name
  virtual_network_name = azurerm_virtual_network.spoke.name
  address_prefixes     = [var.aks_subnet_prefix]
}

resource "azurerm_kubernetes_cluster" "aks" {
  name                    = "aks-${var.environment}-uks-001"
  location                = azurerm_resource_group.spoke.location
  resource_group_name     = azurerm_resource_group.spoke.name
  dns_prefix              = "${var.prefix}aks"
  private_cluster_enabled = true

  default_node_pool {
    name           = "default"
    node_count     = 2
    vm_size        = "Standard_DS2_v2"
    vnet_subnet_id = azurerm_subnet.aks.id
  }

  identity {
    type = "SystemAssigned"
  }

  ingress_application_gateway {
    gateway_name = "appgw-${var.environment}-uks"
    subnet_cidr  = var.appgw_subnet_prefix
  }

  network_profile {
    network_plugin = "azure"
    network_policy = "azure"
  }
}

resource "azurerm_cognitive_account" "openai" {
  name                = "${var.prefix}-openai-${var.environment}"
  location            = azurerm_resource_group.spoke.location
  resource_group_name = azurerm_resource_group.spoke.name
  kind                = "OpenAI"
  sku_name            = "S0"

  public_network_access_enabled = false
}

resource "azurerm_private_endpoint" "openai" {
  name                = "pe-openai-${var.environment}"
  location            = var.pe_location
  resource_group_name = azurerm_resource_group.spoke.name
  subnet_id           = var.hub_pe_subnet_id

  private_service_connection {
    name                           = "psc-openai"
    private_connection_resource_id = azurerm_cognitive_account.openai.id
    is_manual_connection           = false
    subresource_names              = ["account"]
  }

  private_dns_zone_group {
    name                 = "openai-dns-group"
    private_dns_zone_ids = [var.openai_dns_zone_id]
  }
}
