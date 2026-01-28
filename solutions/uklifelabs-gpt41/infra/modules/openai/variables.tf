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
  description = "Resource group for OpenAI"
  type        = string
}

variable "hub_resource_group_name" {
  description = "Hub resource group for private endpoint"
  type        = string
}

variable "hub_pe_subnet_id" {
  description = "Hub subnet ID for private endpoint"
  type        = string
}

variable "openai_private_dns_zone_id" {
  description = "Private DNS zone ID for OpenAI"
  type        = string
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
  default     = {}
}
