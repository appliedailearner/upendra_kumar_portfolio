variable "environment" {
  description = "Environment name (prod, test, dev)"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "uksouth"
}

variable "location_short" {
  description = "Short location code"
  type        = string
  default     = "uks"
}

variable "resource_group_name" {
  description = "Resource group for Redis cache"
  type        = string
}

variable "hub_resource_group_name" {
  description = "Hub resource group for private endpoint"
  type        = string
}

variable "redis_subnet_id" {
  description = "Subnet ID for Redis VNet injection"
  type        = string
}

variable "hub_pe_subnet_id" {
  description = "Hub subnet ID for private endpoint"
  type        = string
}

variable "redis_private_dns_zone_id" {
  description = "Private DNS zone ID for Redis"
  type        = string
}

variable "key_vault_id" {
  description = "Key Vault ID for storing connection string"
  type        = string
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
  default     = {}
}
