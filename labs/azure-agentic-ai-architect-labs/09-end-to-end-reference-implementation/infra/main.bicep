@description('Environment name')
@allowed([
  'dev'
  'staging'
  'prod'
])
param environment string = 'dev'

@description('Azure region for resource deployment')
param location string = resourceGroup().location

@description('Project name for resource naming')
param projectName string = 'agentic-ai'

@description('Azure Search service SKU')
@allowed([
  'free'
  'basic'
  'standard'
  'standard2'
  'standard3'
])
param searchSku string = 'standard'

@description('Cosmos DB provisioned throughput (RU/s)')
@minValue(100)
@maxValue(1000000)
param cosmosdbThroughput int = 400

@description('Principal ID of the user executing the deployment to grant KeyVault access')
param principalId string

// Local variables
var resourceSuffix = '${projectName}-${environment}'
var commonTags = {
  Environment: environment
  Project: projectName
  ManagedBy: 'Bicep'
}

// Azure AI Foundry Services
resource aiServices 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: 'aih-${resourceSuffix}'
  location: location
  tags: commonTags
  kind: 'AIServices'
  sku: {
    name: 'S0'
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    customSubDomainName: 'aih-${resourceSuffix}'
    publicNetworkAccess: 'Enabled'
  }
}

// Azure OpenAI Deployment
resource openAI 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: 'oai-${resourceSuffix}'
  location: location
  tags: commonTags
  kind: 'OpenAI'
  sku: {
    name: 'S0'
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    customSubDomainName: 'oai-${resourceSuffix}'
    publicNetworkAccess: 'Enabled'
  }
}

// Azure Search Service for RAG
resource searchService 'Microsoft.Search/searchServices@2023-11-01' = {
  name: 'search-${resourceSuffix}'
  location: location
  tags: commonTags
  sku: {
    name: searchSku
  }
  properties: {
    publicNetworkAccess: 'enabled'
  }
}

// Azure Cosmos DB for agent state
resource cosmosDbAccount 'Microsoft.DocumentDB/databaseAccounts@2023-11-15' = {
  name: 'cosmos-${resourceSuffix}'
  location: location
  tags: commonTags
  kind: 'GlobalDocumentDB'
  properties: {
    databaseAccountOfferType: 'Standard'
    locations: [
      {
        locationName: location
        failoverPriority: 0
      }
    ]
    consistencyPolicy: {
      defaultConsistencyLevel: 'Session'
      maxStalenessPrefix: 100
      maxIntervalInSeconds: 5
    }
  }
}

// Key Vault for secrets management
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: 'kv-${resourceSuffix}'
  location: location
  tags: commonTags
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    enableSoftDelete: true
    enablePurgeProtection: false // Matching TF
    accessPolicies: [
      {
        tenantId: subscription().tenantId
        objectId: principalId
        permissions: {
          secrets: [
            'get'
            'list'
            'set'
            'delete'
            'recover'
            'backup'
            'restore'
          ]
        }
      }
    ]
  }
}

// Store OpenAI key in Key Vault
resource openaiKeySecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'openai-api-key'
  properties: {
    value: openAI.listKeys().key1
  }
}

// Store Search key in Key Vault
resource searchKeySecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'search-api-key'
  properties: {
    value: searchService.listAdminKeys().primaryKey
  }
}

output openAIEndpoint string = openAI.properties.endpoint
output searchEndpoint string = 'https://${searchService.name}.search.windows.net'
output cosmosDbEndpoint string = cosmosDbAccount.properties.documentEndpoint
output keyVaultUri string = keyVault.properties.vaultUri

// ==========================================
// API Mediation Layer (L67 Architecture)
// ==========================================

// Application Insights for monitoring
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'appins-${resourceSuffix}'
  location: location
  tags: commonTags
  kind: 'web'
  properties: {
    Application_Type: 'web'
  }
}

// Hosting Plan for Azure Functions
resource hostingPlan 'Microsoft.Web/serverfarms@2022-09-01' = {
  name: 'plan-${resourceSuffix}'
  location: location
  tags: commonTags
  sku: {
    name: 'Y1'
    tier: 'Dynamic'
  }
  properties: {}
}

// Storage Account for Azure Functions
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: replace('st${resourceSuffix}', '-', '') // Storage accounts cannot have hyphens
  location: location
  tags: commonTags
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    supportsHttpsTrafficOnly: true
  }
}

// Function App (Tool Execution Backend)
resource functionApp 'Microsoft.Web/sites@2022-09-01' = {
  name: 'func-${resourceSuffix}'
  location: location
  tags: commonTags
  kind: 'functionapp'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: hostingPlan.id
    siteConfig: {
      appSettings: [
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};EndpointSuffix=${environment().suffixes.storage};AccountKey=${storageAccount.listKeys().keys[0].value}'
        }
        {
          name: 'WEBSITE_CONTENTAZUREFILECONNECTIONSTRING'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};EndpointSuffix=${environment().suffixes.storage};AccountKey=${storageAccount.listKeys().keys[0].value}'
        }
        {
          name: 'WEBSITE_CONTENTSHARE'
          value: toLower('func-${resourceSuffix}')
        }
        {
          name: 'FUNCTIONS_EXTENSION_VERSION'
          value: '~4'
        }
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'python'
        }
        {
          name: 'APPINSIGHTS_INSTRUMENTATIONKEY'
          value: appInsights.properties.InstrumentationKey
        }
      ]
      ftpsState: 'FtpsOnly'
      minTlsVersion: '1.2'
    }
    httpsOnly: true
  }
}

// API Management (Zero-Trust Gateway)
resource apiManagement 'Microsoft.ApiManagement/service@2023-05-01-preview' = {
  name: 'apim-${resourceSuffix}'
  location: location
  tags: commonTags
  sku: {
    name: 'Consumption'
    capacity: 0
  }
  properties: {
    publisherEmail: 'admin@${projectName}.com'
    publisherName: '${projectName} Admin'
  }
}

// ==========================================
// Managed Identity & RBAC (Keyless Auth)
// ==========================================

// User Assigned Identity for the Python Agent App
resource agentIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: 'id-agent-${resourceSuffix}'
  location: location
  tags: commonTags
}

// Cognitive Services OpenAI User -> Agent Identity
resource openAIRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(openAI.id, agentIdentity.id, '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd') // Cognitive Services OpenAI User role ID
  scope: openAI
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd')
    principalId: agentIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// Search Index Data Reader -> Agent Identity (For RAG)
resource searchRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(searchService.id, agentIdentity.id, '1407120a-92aa-4202-b7e9-c0e197c71c8f') // Search Index Data Reader
  scope: searchService
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '1407120a-92aa-4202-b7e9-c0e197c71c8f')
    principalId: agentIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// Key Vault Secrets User -> Agent Identity
resource kvRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(keyVault.id, agentIdentity.id, '4633458b-17de-408a-b874-0445c86b69e6') // Key Vault Secrets User
  scope: keyVault
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '4633458b-17de-408a-b874-0445c86b69e6')
    principalId: agentIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

output agentManagedIdentityClientId string = agentIdentity.properties.clientId
