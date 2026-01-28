# Global Ingress (Front Door) - Managed in Prod Sub
module "frontdoor" {
  providers = { azize = azurerm.prod }
  source    = "./modules/frontdoor"
  prefix    = "ukl-global"
}

# Regional Hub - Primary (UK South)
module "hub_prod" {
  providers = { azurerm = azurerm.prod }
  source    = "./modules/hub"
  location  = "uksouth"
  prefix    = "ukl-prod"
}

# Regional Hub - DR (UK West)
module "hub_dr" {
  providers = { azurerm = azurerm.dr }
  source    = "./modules/hub"
  location  = "ukwest"
  prefix    = "ukl-dr"
}

# AKS Clusters - Deployed into Regional Hubs
module "aks_prod" {
  providers = { azurerm = azurerm.prod }
  source    = "./modules/aks"
  location  = "uksouth"
  subnet_id = module.hub_prod.aks_subnet_id
}

# AI & API Infrastructure (UK South)
module "ai_prod" {
  providers = { azurerm = azurerm.prod }
  source    = "./modules/ai_hub"
  location  = "uksouth"
  ptu_units = 50
  subnet_id = module.hub_prod.ai_subnet_id
}
