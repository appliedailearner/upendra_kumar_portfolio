module "hub" {
  source = "./modules/hub"
  providers = {
    azurerm = azurerm.hub
  }

  prefix   = var.prefix
  location = var.primary_region
}

module "prod_spoke" {
  source = "./modules/spoke"
  providers = {
    azurerm = azurerm.prod
  }

  prefix              = var.prefix
  environment         = "prod"
  location            = var.primary_region
  vnet_address_space  = "10.1.0.0/16"
  aks_subnet_prefix   = "10.1.1.0/24"
  appgw_subnet_prefix = "10.1.2.0/24"
  hub_pe_subnet_id    = module.hub.shared_pe_subnet_id
  openai_dns_zone_id  = module.hub.openai_dns_zone_id
  pe_location         = var.primary_region
}

# VNet Peering: Hub -> Prod Spoke
resource "azurerm_virtual_network_peering" "hub_to_prod" {
  provider                  = azurerm.hub
  name                      = "peer-hub-to-prod"
  resource_group_name       = module.hub.resource_group_name
  virtual_network_name      = module.hub.vnet_name
  remote_virtual_network_id = module.prod_spoke.vnet_id
  allow_forwarded_traffic   = true
}

# VNet Peering: Prod Spoke -> Hub
resource "azurerm_virtual_network_peering" "prod_to_hub" {
  provider                  = azurerm.prod
  name                      = "peer-prod-to-hub"
  resource_group_name       = module.prod_spoke.resource_group_name
  virtual_network_name      = module.prod_spoke.vnet_name
  remote_virtual_network_id = module.hub.vnet_id
  allow_forwarded_traffic   = true
}

module "dr_spoke" {
  source = "./modules/spoke"
  providers = {
    azurerm = azurerm.dr
  }

  prefix              = var.prefix
  environment         = "dr"
  location            = var.dr_region
  vnet_address_space  = "10.2.0.0/16"
  aks_subnet_prefix   = "10.2.1.0/24"
  appgw_subnet_prefix = "10.2.2.0/24"
  hub_pe_subnet_id    = module.hub.shared_pe_subnet_id
  openai_dns_zone_id  = module.hub.openai_dns_zone_id
  pe_location         = var.primary_region # PE stays in Hub region
}

# VNet Peering: Hub -> DR Spoke (Global Peering)
resource "azurerm_virtual_network_peering" "hub_to_dr" {
  provider                  = azurerm.hub
  name                      = "peer-hub-to-dr"
  resource_group_name       = module.hub.resource_group_name
  virtual_network_name      = module.hub.vnet_name
  remote_virtual_network_id = module.dr_spoke.vnet_id
  allow_forwarded_traffic   = true
}

# VNet Peering: DR Spoke -> Hub
resource "azurerm_virtual_network_peering" "dr_to_hub" {
  provider                  = azurerm.dr
  name                      = "peer-dr-to-hub"
  resource_group_name       = module.dr_spoke.resource_group_name
  virtual_network_name      = module.dr_spoke.vnet_name
  remote_virtual_network_id = module.hub.vnet_id
  allow_forwarded_traffic   = true
}
