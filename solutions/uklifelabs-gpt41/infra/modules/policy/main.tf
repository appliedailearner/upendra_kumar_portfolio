terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

data "azurerm_subscription" "current" {}

# Assign Microsoft Cloud Security Benchmark v2 Initiative
resource "azurerm_subscription_policy_assignment" "mcsb_v2" {
  name                 = "mcsb-v2-compliance"
  policy_definition_id = "/providers/Microsoft.Authorization/policySetDefinitions/1f3afdf9-d0c9-4c3d-847f-89da613e70a8"
  subscription_id      = data.azurerm_subscription.current.id

  description  = "Microsoft Cloud Security Benchmark v2 compliance monitoring for AI Fortress"
  display_name = "MCSB v2 - AI Fortress Compliance"

  location = var.location

  identity {
    type = "SystemAssigned"
  }

  parameters = jsonencode({
    effect = {
      value = "AuditIfNotExists"
    }
  })
}

# Role assignment for policy remediation
resource "azurerm_role_assignment" "policy_remediation" {
  scope                = data.azurerm_subscription.current.id
  role_definition_name = "Contributor"
  principal_id         = azurerm_subscription_policy_assignment.mcsb_v2.identity[0].principal_id
}

# Output compliance assignment ID
output "mcsb_v2_assignment_id" {
  value       = azurerm_subscription_policy_assignment.mcsb_v2.id
  description = "The ID of the MCSB v2 policy assignment"
}

output "compliance_dashboard_url" {
  value       = "https://portal.azure.com/#view/Microsoft_Azure_Policy/PolicyMenuBlade/~/Compliance"
  description = "URL to view compliance dashboard in Azure Portal"
}
