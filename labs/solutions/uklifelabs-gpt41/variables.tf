variable "prefix" {
  type    = string
  default = "uklifelabs"
}

variable "environment" {
  type    = string
  default = "prod"
}

variable "dr_subscription_id" {
  type        = string
  description = "The Subscription ID for the DR environment"
}

variable "prod_subscription_id" {
  type        = string
  description = "The Subscription ID for the Primary environment"
}

variable "ptu_deployments" {
  type = map(object({
    model_name    = string
    model_format  = string
    model_version = string
    capacity      = number
  }))
  default = {
    "prod-gpt41" = {
      model_name    = "gpt-4"
      model_format  = "OpenAI"
      model_version = "vision-preview" # Using available version placeholder
      capacity      = 30
    }
  }
}
