variable "hub_subscription_id" {
  description = "The Subscription ID for Shared Services Hub"
  type        = string
}

variable "prod_subscription_id" {
  description = "The Subscription ID for Production Spoke"
  type        = string
}

variable "nonprod_subscription_id" {
  description = "The Subscription ID for Non-Prod Spoke"
  type        = string
}

variable "dr_subscription_id" {
  description = "The Subscription ID for Disaster Recovery"
  type        = string
}

variable "primary_region" {
  description = "Main deployment region"
  type        = string
  default     = "uksouth"
}

variable "dr_region" {
  description = "Disaster recovery region"
  type        = string
  default     = "ukwest"
}

variable "environment" {
  description = "Deployment environment (e.g., prod, dev)"
  type        = string
  default     = "prod"
}

variable "prefix" {
  description = "Prefix for all resources"
  type        = string
  default     = "ukl"
}
