terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

# Primary Subscription (UK South)
provider "azurerm" {
  alias           = "prod"
  subscription_id = var.prod_subscription_id
  features {}
}

# DR Subscription (UK West)
provider "azurerm" {
  alias           = "dr"
  subscription_id = var.dr_subscription_id
  features {}
}
