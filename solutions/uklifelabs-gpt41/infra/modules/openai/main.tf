terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

# Azure OpenAI Account
resource "azurerm_cognitive_account" "openai" {
  name                = "oai-${var.environment}-${var.location_short}"
  location            = var.location
  resource_group_name = var.resource_group_name
  kind                = "OpenAI"
  sku_name            = "S0"

  custom_subdomain_name = "ukl-openai-${var.environment}"

  network_acls {
    default_action = "Deny"
    ip_rules       = []
  }

  public_network_access_enabled = false

  tags = var.tags
}

# Production Deployment (30 PTU)
resource "azurerm_cognitive_deployment" "gpt4_prod" {
  name                 = "gpt4-prod-deployment"
  cognitive_account_id = azurerm_cognitive_account.openai.id

  model {
    format  = "OpenAI"
    name    = "gpt-4"
    version = "turbo-2024-04-09"
  }

  sku {
    name     = "ProvisionedManaged"
    capacity = 30 # 30 PTU for Production
  }
}

# Test Deployment (10 PTU)
resource "azurerm_cognitive_deployment" "gpt4_test" {
  name                 = "gpt4-test-deployment"
  cognitive_account_id = azurerm_cognitive_account.openai.id

  model {
    format  = "OpenAI"
    name    = "gpt-4"
    version = "turbo-2024-04-09"
  }

  sku {
    name     = "ProvisionedManaged"
    capacity = 10 # 10 PTU for Test
  }
}

# Dev Deployment (10 PTU)
resource "azurerm_cognitive_deployment" "gpt4_dev" {
  name                 = "gpt4-dev-deployment"
  cognitive_account_id = azurerm_cognitive_account.openai.id

  model {
    format  = "OpenAI"
    name    = "gpt-4"
    version = "turbo-2024-04-09"
  }

  sku {
    name     = "ProvisionedManaged"
    capacity = 10 # 10 PTU for Dev
  }
}

# Private Endpoint for OpenAI
resource "azurerm_private_endpoint" "openai_pe" {
  name                = "pe-openai-${var.environment}"
  location            = var.location
  resource_group_name = var.hub_resource_group_name
  subnet_id           = var.hub_pe_subnet_id

  private_service_connection {
    name                           = "psc-openai-${var.environment}"
    private_connection_resource_id = azurerm_cognitive_account.openai.id
    is_manual_connection           = false
    subresource_names              = ["account"]
  }

  private_dns_zone_group {
    name                 = "default"
    private_dns_zone_ids = [var.openai_private_dns_zone_id]
  }
}

# Outputs
output "openai_id" {
  value       = azurerm_cognitive_account.openai.id
  description = "The ID of the OpenAI account"
}

output "openai_endpoint" {
  value       = azurerm_cognitive_account.openai.endpoint
  description = "The endpoint of the OpenAI account"
}

output "prod_deployment_name" {
  value       = azurerm_cognitive_deployment.gpt4_prod.name
  description = "Production deployment name"
}

output "test_deployment_name" {
  value       = azurerm_cognitive_deployment.gpt4_test.name
  description = "Test deployment name"
}

output "dev_deployment_name" {
  value       = azurerm_cognitive_deployment.gpt4_dev.name
  description = "Dev deployment name"
}
