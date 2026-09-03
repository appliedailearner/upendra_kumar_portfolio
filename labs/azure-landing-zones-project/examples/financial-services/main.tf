terraform {
  required_version = ">= 1.6.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.80.0"
    }
  }
}

provider "azurerm" {
  features {}
}

module "ai_landing_zone" {
  source = "../../terraform/modules/ai-landing-zone"

  # Resource Group
  resource_group_name = "rg-ai-finserv-prod-001"
  location           = "eastus2"
  environment        = "prod"

  # Networking
  vnet_address_space = ["10.0.0.0/16"]

  # Compliance
  industry_compliance = {
    pci_dss = true
    hipaa   = false
    sox     = true
    gdpr    = true
  }

  # Tags
  tags = {
    Environment = "Production"
    CostCenter  = "FinServ-AI-001"
    Project     = "FraudDetection"
    ManagedBy   = "Terraform"
  }
}
