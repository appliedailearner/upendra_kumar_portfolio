# Required Variables
variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
}

variable "location_short" {
  description = "Short location name"
  type        = string
  default     = "eus2"
}

variable "environment" {
  description = "Environment (dev/staging/prod)"
  type        = string
}

variable "vnet_address_space" {
  description = "VNet address space"
  type        = list(string)
}

# Optional Variables
variable "host_pool_config" {
  description = "Host pool configuration"
  type = object({
    type               = string
    load_balancer_type = string
    max_session_limit  = number
  })
  default = {
    type               = "Pooled"
    load_balancer_type = "BreadthFirst"
    max_session_limit  = 10
  }
}

variable "session_host_config" {
  description = "Session host configuration"
  type = object({
    vm_size   = string
    vm_count  = number
    image_sku = string
  })
  default = {
    vm_size   = "Standard_D4s_v5"
    vm_count  = 10
    image_sku = "win11-22h2-avd"
  }
}

variable "fslogix_config" {
  description = "FSLogix configuration"
  type = object({
    storage_sku = string
    quota_gb    = number
  })
  default = {
    storage_sku = "Premium_LRS"
    quota_gb    = 50
  }
}

variable "compliance" {
  description = "Compliance requirements"
  type = object({
    session_recording = bool
    mfa_required     = bool
  })
  default = {
    session_recording = true
    mfa_required     = true
  }
}

variable "hub_vnet_address_space" {
  description = "Hub VNet address space for NSG rules"
  type        = string
  default     = null
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
  default     = {}
}
