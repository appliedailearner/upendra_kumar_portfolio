# AI Landing Zone - Low-Level Design

**Project**: Azure Landing Zones - Financial Services  
**Component**: AI Landing Zone  
**Version**: 1.0.0  
**Last Updated**: December 2025

---

## 1. Resource Naming and Configuration

### 1.1 Resource Naming Standards

**Format**: `<resource-type>-<environment>-<region>-<workload>-<instance>`

| Resource Type | Prefix | Example |
|--------------|--------|---------|
| Resource Group | rg | rg-prod-eus2-ai-01 |
| Virtual Network | vnet | vnet-prod-eus2-ai-spoke |
| Subnet | snet | snet-prod-eus2-ai-ml |
| Network Security Group | nsg | nsg-prod-eus2-ai-ml |
| Azure ML Workspace | aml | aml-prod-eus2-ai-01 |
| Storage Account | st | stprodeus2aidatalake |
| Key Vault | kv | kv-prod-eus2-ai-01 |
| Azure OpenAI | aoai | aoai-prod-eus2-ai-01 |
| Container Registry | acr | acrprodeus2ai01 |
| Log Analytics | log | log-prod-eus2-ai-01 |

---

## 2. Infrastructure as Code

### 2.1 Terraform Configuration

**Directory Structure**:
```
terraform/
├── environments/
│   ├── prod/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   └── dev/
├── modules/
│   ├── networking/
│   ├── ml-workspace/
│   ├── storage/
│   ├── security/
│   └── monitoring/
└── README.md
```

**Example: ML Workspace Module**:
```hcl
resource "azurerm_machine_learning_workspace" "ml_workspace" {
  name                    = var.workspace_name
  location                = var.location
  resource_group_name     = var.resource_group_name
  application_insights_id = var.application_insights_id
  key_vault_id           = var.key_vault_id
  storage_account_id     = var.storage_account_id
  container_registry_id  = var.container_registry_id

  identity {
    type = "SystemAssigned"
  }

  public_network_access_enabled = false
  
  managed_network {
    isolation_mode = "AllowOnlyApprovedOutbound"
  }

  tags = var.tags
}

resource "azurerm_machine_learning_compute_cluster" "cpu_cluster" {
  name                          = "cpu-cluster-01"
  location                      = var.location
  vm_priority                   = "Dedicated"
  vm_size                       = "Standard_D4s_v3"
  machine_learning_workspace_id = azurerm_machine_learning_workspace.ml_workspace.id
  
  scale_settings {
    min_node_count                       = 0
    max_node_count                       = 50
    scale_down_nodes_after_idle_duration = "PT30M"
  }

  identity {
    type = "SystemAssigned"
  }

  ssh {
    admin_username = var.admin_username
    key_data       = var.ssh_public_key
  }
}
```

---

## 3. Network Configuration Details

### 3.1 Route Tables

**AI-Spoke-RT**:
| Name | Address Prefix | Next Hop Type | Next Hop |
|------|---------------|---------------|----------|
| Default-Route | 0.0.0.0/0 | Virtual Appliance | 10.0.1.4 (Firewall) |
| Hub-Route | 10.0.0.0/16 | VNet Peering | Hub-VNet |
| Internet-Block | Internet | None | - |

### 3.2 NSG Rules (Detailed)

**ML-Workspace-NSG**:
```json
{
  "securityRules": [
    {
      "name": "Allow-Hub-Inbound",
      "priority": 100,
      "direction": "Inbound",
      "access": "Allow",
      "protocol": "Tcp",
      "sourceAddressPrefix": "10.0.0.0/16",
      "sourcePortRange": "*",
      "destinationAddressPrefix": "10.100.1.0/24",
      "destinationPortRange": "443"
    },
    {
      "name": "Allow-AzureLoadBalancer",
      "priority": 110,
      "direction": "Inbound",
      "access": "Allow",
      "protocol": "*",
      "sourceAddressPrefix": "AzureLoadBalancer",
      "sourcePortRange": "*",
      "destinationAddressPrefix": "*",
      "destinationPortRange": "*"
    },
    {
      "name": "Deny-All-Inbound",
      "priority": 4096,
      "direction": "Inbound",
      "access": "Deny",
      "protocol": "*",
      "sourceAddressPrefix": "*",
      "sourcePortRange": "*",
      "destinationAddressPrefix": "*",
      "destinationPortRange": "*"
    }
  ]
}
```

### 3.3 Private Endpoint Configuration

**Azure OpenAI Private Endpoint**:
```bash
# Create private endpoint
az network private-endpoint create \
  --name pe-aoai-prod-eus2-ai-01 \
  --resource-group rg-prod-eus2-ai-01 \
  --vnet-name vnet-prod-eus2-ai-spoke \
  --subnet snet-prod-eus2-ai-pe \
  --private-connection-resource-id /subscriptions/{sub-id}/resourceGroups/{rg}/providers/Microsoft.CognitiveServices/accounts/aoai-prod-eus2-ai-01 \
  --group-id account \
  --connection-name aoai-connection

# Create private DNS zone
az network private-dns zone create \
  --resource-group rg-prod-eus2-ai-01 \
  --name privatelink.openai.azure.com

# Link to VNet
az network private-dns link vnet create \
  --resource-group rg-prod-eus2-ai-01 \
  --zone-name privatelink.openai.azure.com \
  --name aoai-dns-link \
  --virtual-network vnet-prod-eus2-ai-spoke \
  --registration-enabled false
```

---

## 4. Storage Configuration

### 4.1 Data Lake Storage Gen2 Setup

**Storage Account Configuration**:
```json
{
  "name": "stprodeus2aidatalake",
  "sku": {
    "name": "Standard_ZRS"
  },
  "kind": "StorageV2",
  "properties": {
    "isHnsEnabled": true,
    "minimumTlsVersion": "TLS1_3",
    "allowBlobPublicAccess": false,
    "networkAcls": {
      "bypass": "AzureServices",
      "defaultAction": "Deny",
      "virtualNetworkRules": [
        {
          "id": "/subscriptions/{sub-id}/resourceGroups/{rg}/providers/Microsoft.Network/virtualNetworks/vnet-prod-eus2-ai-spoke/subnets/snet-prod-eus2-ai-data"
        }
      ]
    },
    "encryption": {
      "services": {
        "blob": {"enabled": true},
        "file": {"enabled": true}
      },
      "keySource": "Microsoft.Keyvault",
      "keyvaultproperties": {
        "keyvaulturi": "https://kv-prod-eus2-ai-01.vault.azure.net",
        "keyname": "storage-encryption-key"
      }
    }
  }
}
```

**Container Structure**:
```
stprodeus2aidatalake/
├── raw/
│   ├── transactions/
│   ├── customer-data/
│   └── market-data/
├── curated/
│   ├── transactions-clean/
│   ├── customer-profiles/
│   └── features/
├── models/
│   ├── fraud-detection/
│   ├── churn-prediction/
│   └── risk-assessment/
└── inference/
    ├── requests/
    └── responses/
```

### 4.2 Lifecycle Management Policy

```json
{
  "rules": [
    {
      "name": "MoveRawToCool",
      "enabled": true,
      "type": "Lifecycle",
      "definition": {
        "filters": {
          "blobTypes": ["blockBlob"],
          "prefixMatch": ["raw/"]
        },
        "actions": {
          "baseBlob": {
            "tierToCool": {"daysAfterModificationGreaterThan": 30},
            "tierToArchive": {"daysAfterModificationGreaterThan": 90}
          }
        }
      }
    },
    {
      "name": "DeleteOldInference",
      "enabled": true,
      "type": "Lifecycle",
      "definition": {
        "filters": {
          "blobTypes": ["blockBlob"],
          "prefixMatch": ["inference/"]
        },
        "actions": {
          "baseBlob": {
            "delete": {"daysAfterModificationGreaterThan": 30}
          }
        }
      }
    }
  ]
}
```

---

## 5. Azure ML Workspace Configuration

### 5.1 Compute Cluster Specifications

**CPU Cluster**:
```python
from azure.ai.ml.entities import AmlCompute

cpu_cluster = AmlCompute(
    name="cpu-cluster-01",
    type="amlcompute",
    size="Standard_D4s_v3",
    min_instances=0,
    max_instances=50,
    idle_time_before_scale_down=1800,  # 30 minutes
    tier="Dedicated",
)
```

**GPU Cluster**:
```python
gpu_cluster = AmlCompute(
    name="gpu-cluster-01",
    type="amlcompute",
    size="Standard_NC6s_v3",
    min_instances=0,
    max_instances=20,
    idle_time_before_scale_down=600,  # 10 minutes
    tier="Dedicated",
)
```

### 5.2 Environment Configuration

**Custom Environment Dockerfile**:
```dockerfile
FROM mcr.microsoft.com/azureml/openmpi4.1.0-cuda11.8-cudnn8-ubuntu22.04:latest

# Install Python packages
RUN pip install --no-cache-dir \
    azureml-core==1.54.0 \
    azureml-mlflow==1.54.0 \
    scikit-learn==1.3.2 \
    pandas==2.1.4 \
    numpy==1.26.2 \
    matplotlib==3.8.2 \
    seaborn==0.13.0 \
    xgboost==2.0.3 \
    lightgbm==4.1.0 \
    shap==0.44.0 \
    fairlearn==0.9.0

# Set working directory
WORKDIR /workspace

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV AZUREML_COMPUTE_USE_COMMON_RUNTIME=true
```

---

## 6. Azure OpenAI Configuration

### 6.1 Deployment Configuration

**GPT-4 Deployment**:
```bash
az cognitiveservices account deployment create \
  --name aoai-prod-eus2-ai-01 \
  --resource-group rg-prod-eus2-ai-01 \
  --deployment-name gpt-4 \
  --model-name gpt-4 \
  --model-version "0613" \
  --model-format OpenAI \
  --sku-capacity 100 \
  --sku-name "Standard"
```

### 6.2 API Configuration

**Connection String (stored in Key Vault)**:
```
Endpoint=https://aoai-prod-eus2-ai-01.openai.azure.com/;ApiKey={key-from-keyvault}
```

**Python SDK Configuration**:
```python
import openai
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Get API key from Key Vault
credential = DefaultAzureCredential()
kv_client = SecretClient(
    vault_url="https://kv-prod-eus2-ai-01.vault.azure.net",
    credential=credential
)
api_key = kv_client.get_secret("aoai-api-key").value

# Configure OpenAI
openai.api_type = "azure"
openai.api_base = "https://aoai-prod-eus2-ai-01.openai.azure.com/"
openai.api_version = "2024-02-01"
openai.api_key = api_key
```

---

## 7. Security Configuration

### 7.1 Key Vault Setup

**Key Vault Configuration**:
```bash
# Create Key Vault
az keyvault create \
  --name kv-prod-eus2-ai-01 \
  --resource-group rg-prod-eus2-ai-01 \
  --location eastus2 \
  --sku Premium \
  --enabled-for-deployment true \
  --enabled-for-disk-encryption true \
  --enabled-for-template-deployment true \
  --enable-purge-protection true \
  --enable-soft-delete true \
  --soft-delete-retention-days 90 \
  --public-network-access Disabled

# Create encryption key
az keyvault key create \
  --vault-name kv-prod-eus2-ai-01 \
  --name storage-encryption-key \
  --protection hsm \
  --kty RSA-HSM \
  --size 4096
```

### 7.2 Managed Identity Configuration

**System-Assigned Managed Identity for ML Workspace**:
```bash
# Enable system-assigned identity
az ml workspace update \
  --name aml-prod-eus2-ai-01 \
  --resource-group rg-prod-eus2-ai-01 \
  --system-assigned

# Grant permissions to storage
az role assignment create \
  --assignee-object-id <ml-workspace-identity-id> \
  --assignee-principal-type ServicePrincipal \
  --role "Storage Blob Data Contributor" \
  --scope /subscriptions/{sub-id}/resourceGroups/rg-prod-eus2-ai-01/providers/Microsoft.Storage/storageAccounts/stprodeus2aidatalake
```

### 7.3 RBAC Assignments

**Custom Role Definition**:
```json
{
  "Name": "AI Platform Data Scientist",
  "Description": "Can use ML workspace and access training data",
  "Actions": [
    "Microsoft.MachineLearningServices/workspaces/read",
    "Microsoft.MachineLearningServices/workspaces/computes/start/action",
    "Microsoft.MachineLearningServices/workspaces/computes/stop/action",
    "Microsoft.MachineLearningServices/workspaces/experiments/*",
    "Microsoft.MachineLearningServices/workspaces/models/read",
    "Microsoft.MachineLearningServices/workspaces/datasets/*"
  ],
  "NotActions": [
    "Microsoft.MachineLearningServices/workspaces/computes/delete",
    "Microsoft.MachineLearningServices/workspaces/delete"
  ],
  "DataActions": [
    "Microsoft.Storage/storageAccounts/blobServices/containers/blobs/read",
    "Microsoft.Storage/storageAccounts/blobServices/containers/blobs/write"
  ],
  "AssignableScopes": [
    "/subscriptions/{subscription-id}/resourceGroups/rg-prod-eus2-ai-01"
  ]
}
```

---

## 8. Monitoring Configuration

### 8.1 Log Analytics Workspace

**Diagnostic Settings for ML Workspace**:
```json
{
  "name": "ml-diagnostics",
  "properties": {
    "workspaceId": "/subscriptions/{sub-id}/resourceGroups/rg-prod-eus2-ai-01/providers/Microsoft.OperationalInsights/workspaces/log-prod-eus2-ai-01",
    "logs": [
      {"category": "AmlComputeClusterEvent", "enabled": true},
      {"category": "AmlComputeClusterNodeEvent", "enabled": true},
      {"category": "AmlComputeJobEvent", "enabled": true},
      {"category": "AmlComputeCpuGpuUtilization", "enabled": true},
      {"category": "AmlRunStatusChangedEvent", "enabled": true}
    ],
    "metrics": [
      {"category": "AllMetrics", "enabled": true}
    ]
  }
}
```

### 8.2 Alert Rules

**Model Training Failure Alert**:
```bash
az monitor metrics alert create \
  --name "ML-Training-Failure" \
  --resource-group rg-prod-eus2-ai-01 \
  --scopes /subscriptions/{sub-id}/resourceGroups/rg-prod-eus2-ai-01/providers/Microsoft.MachineLearningServices/workspaces/aml-prod-eus2-ai-01 \
  --condition "count FailedRuns > 5" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --action email support@contoso.com \
  --description "Alert when more than 5 training runs fail in 5 minutes"
```

---

## 9. Deployment Scripts

### 9.1 PowerShell Deployment Script

```powershell
# Deploy AI Landing Zone
param(
    [Parameter(Mandatory=$true)]
    [string]$Environment,
    
    [Parameter(Mandatory=$true)]
    [string]$Location,
    
    [Parameter(Mandatory=$true)]
    [string]$SubscriptionId
)

# Set context
Set-AzContext -SubscriptionId $SubscriptionId

# Variables
$rgName = "rg-$Environment-$Location-ai-01"
$vnetName = "vnet-$Environment-$Location-ai-spoke"
$mlWorkspaceName = "aml-$Environment-$Location-ai-01"

# Create resource group
New-AzResourceGroup -Name $rgName -Location $Location

# Deploy networking
New-AzResourceGroupDeployment `
    -ResourceGroupName $rgName `
    -TemplateFile "./templates/networking.bicep" `
    -TemplateParameterFile "./parameters/$Environment/networking.parameters.json"

# Deploy ML workspace
New-AzResourceGroupDeployment `
    -ResourceGroupName $rgName `
    -TemplateFile "./templates/ml-workspace.bicep" `
    -TemplateParameterFile "./parameters/$Environment/ml-workspace.parameters.json"

Write-Host "Deployment completed successfully"
```

### 9.2 Azure CLI Deployment Script

```bash
#!/bin/bash

# Deploy AI Landing Zone
ENVIRONMENT=$1
LOCATION=$2
SUBSCRIPTION_ID=$3

# Set subscription
az account set --subscription $SUBSCRIPTION_ID

# Variables
RG_NAME="rg-${ENVIRONMENT}-${LOCATION}-ai-01"
VNET_NAME="vnet-${ENVIRONMENT}-${LOCATION}-ai-spoke"
ML_WORKSPACE_NAME="aml-${ENVIRONMENT}-${LOCATION}-ai-01"

# Create resource group
az group create --name $RG_NAME --location $LOCATION

# Deploy networking
az deployment group create \
  --resource-group $RG_NAME \
  --template-file ./templates/networking.bicep \
  --parameters @./parameters/${ENVIRONMENT}/networking.parameters.json

# Deploy ML workspace
az deployment group create \
  --resource-group $RG_NAME \
  --template-file ./templates/ml-workspace.bicep \
  --parameters @./parameters/${ENVIRONMENT}/ml-workspace.parameters.json

echo "Deployment completed successfully"
```

---

## 10. Configuration Parameters

### 10.1 Environment-Specific Parameters

**Production Parameters** (`prod.tfvars`):
```hcl
environment = "prod"
location = "eastus2"
location_short = "eus2"

# Networking
vnet_address_space = ["10.100.0.0/16"]
ml_subnet_prefix = "10.100.1.0/24"
compute_subnet_prefix = "10.100.2.0/23"
pe_subnet_prefix = "10.100.4.0/24"

# ML Workspace
ml_workspace_sku = "Enterprise"
cpu_cluster_max_nodes = 50
gpu_cluster_max_nodes = 20

# Storage
storage_account_tier = "Standard"
storage_replication_type = "ZRS"

# Tags
tags = {
  Environment = "Production"
  CostCenter = "AI-Platform"
  Owner = "data-science-team"
  Project = "ai-landing-zone"
  Compliance = "PCI-DSS,SOC2"
}
```

---

## References

- [Azure ML Workspace Configuration](https://learn.microsoft.com/azure/machine-learning/how-to-manage-workspace)
- [Terraform Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Azure CLI Reference](https://learn.microsoft.com/cli/azure/)

---

**Document Owner**: Cloud Architect  
**Reviewers**: DevOps Engineer, Security Engineer  
**Approval Date**: December 2025  
**Next Review**: March 2026
