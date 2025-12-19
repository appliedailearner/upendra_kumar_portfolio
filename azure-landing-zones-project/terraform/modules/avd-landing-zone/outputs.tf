output "resource_group_name" {
  description = "Resource group name"
  value       = azurerm_resource_group.avd.name
}

output "host_pool_id" {
  description = "AVD host pool ID"
  value       = azurerm_virtual_desktop_host_pool.pool.id
}

output "host_pool_name" {
  description = "AVD host pool name"
  value       = azurerm_virtual_desktop_host_pool.pool.name
}

output "workspace_id" {
  description = "AVD workspace ID"
  value       = azurerm_virtual_desktop_workspace.workspace.id
}

output "workspace_name" {
  description = "AVD workspace name"
  value       = azurerm_virtual_desktop_workspace.workspace.name
}

output "application_group_id" {
  description = "Desktop application group ID"
  value       = azurerm_virtual_desktop_application_group.desktop.id
}

output "storage_account_id" {
  description = "FSLogix storage account ID"
  value       = azurerm_storage_account.fslogix.id
}

output "storage_account_name" {
  description = "FSLogix storage account name"
  value       = azurerm_storage_account.fslogix.name
}

output "vnet_id" {
  description = "AVD VNet ID"
  value       = azurerm_virtual_network.avd_vnet.id
}

output "log_analytics_workspace_id" {
  description = "Log Analytics workspace ID"
  value       = azurerm_log_analytics_workspace.avd.id
}
