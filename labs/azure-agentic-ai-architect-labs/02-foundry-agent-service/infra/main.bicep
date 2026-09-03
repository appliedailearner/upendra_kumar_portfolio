targetScope = 'resourceGroup'
param location string = resourceGroup().location
param environment string = 'dev'

resource appServicePlan 'Microsoft.Web/serverfarms@2022-09-01' = {
  name: 'plan-02-foundry-agent-service-\'
  location: location
  sku: { name: 'B1' }
}

resource webApp 'Microsoft.Web/sites@2022-09-01' = {
  name: 'app-02-foundry-agent-service-\-\'
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: { linuxFxVersion: 'PYTHON|3.11' }
  }
}
