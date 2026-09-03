output "shared_pe_subnet_id" {
  value = azurerm_subnet.shared_pe.id
}

output "openai_dns_zone_id" {
  value = azurerm_private_dns_zone.openai.id
}

output "vnet_id" {
  value = azurerm_virtual_network.hub.id
}

output "vnet_name" {
  value = azurerm_virtual_network.hub.name
}

output "resource_group_name" {
  value = azurerm_resource_group.hub.name
}
