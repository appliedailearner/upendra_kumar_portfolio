variable "location" {
  description = "Azure region for policy assignment identity"
  type        = string
  default     = "uksouth"
}

variable "subscription_id" {
  description = "Subscription ID to assign policy to"
  type        = string
  default     = ""
}
