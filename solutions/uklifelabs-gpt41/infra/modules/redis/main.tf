terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

# Azure Cache for Redis Premium (VNet Injection)
resource "azurerm_redis_cache" "semantic_cache" {
  name                = "redis-${var.environment}-${var.location_short}-cache"
  location            = var.location
  resource_group_name = var.resource_group_name
  capacity            = 1
  family              = "P"
  sku_name            = "Premium"

  enable_non_ssl_port = false
  minimum_tls_version = "1.2"

  redis_configuration {
    maxmemory_policy                = "allkeys-lru" # Evict least recently used keys
    maxmemory_reserved              = 50
    maxfragmentationmemory_reserved = 50
  }

  subnet_id = var.redis_subnet_id

  tags = var.tags
}

# Private Endpoint for Redis (in Hub)
resource "azurerm_private_endpoint" "redis_pe" {
  name                = "pe-redis-${var.environment}"
  location            = var.location
  resource_group_name = var.hub_resource_group_name
  subnet_id           = var.hub_pe_subnet_id

  private_service_connection {
    name                           = "psc-redis-${var.environment}"
    private_connection_resource_id = azurerm_redis_cache.semantic_cache.id
    is_manual_connection           = false
    subresource_names              = ["redisCache"]
  }

  private_dns_zone_group {
    name                 = "default"
    private_dns_zone_ids = [var.redis_private_dns_zone_id]
  }
}

# Store Redis connection string in Key Vault
resource "azurerm_key_vault_secret" "redis_connection_string" {
  name         = "redis-connection-string"
  value        = azurerm_redis_cache.semantic_cache.primary_connection_string
  key_vault_id = var.key_vault_id
}

# Outputs
output "redis_id" {
  value       = azurerm_redis_cache.semantic_cache.id
  description = "The ID of the Redis cache"
}

output "redis_hostname" {
  value       = azurerm_redis_cache.semantic_cache.hostname
  description = "The hostname of the Redis cache"
}

output "redis_private_endpoint_ip" {
  value       = azurerm_private_endpoint.redis_pe.private_service_connection[0].private_ip_address
  description = "The private IP address of the Redis cache"
}
