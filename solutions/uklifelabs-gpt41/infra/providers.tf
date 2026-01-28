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

# Hub / Shared Services Subscription
provider "azurerm" {
  alias           = "hub"
  subscription_id = var.hub_subscription_id
  features {}
}

# Production Spoke Subscription
provider "azurerm" {
  alias           = "prod"
  subscription_id = var.prod_subscription_id
  features {}
}

# Non-Prod Spoke Subscription
provider "azurerm" {
  alias           = "nonprod"
  subscription_id = var.nonprod_subscription_id
  features {}
}

# Disaster Recovery Subscription
provider "azurerm" {
  alias           = "dr"
  subscription_id = var.dr_subscription_id
  features {}
}
