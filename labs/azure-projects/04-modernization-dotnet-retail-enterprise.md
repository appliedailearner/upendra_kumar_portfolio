# Modernization of Legacy .NET Apps for a Retail Enterprise

## Executive Summary & Business Value
This modernization blueprint outlines the transformation of legacy on-premises applications to cloud-native Azure PaaS services. This shift enables auto-scaling to handle retail peak seasons (e.g., Black Friday) without over-provisioning hardware.
- **Business Impact:** 50% improvement in application performance and page load times.
- **Strategic Goal:** Enable "Daily" release cycles via CI/CD, moving away from quarterly manual deployments.

## Leadership & Strategic Challenges
- **DevOps Transformation:** Overcame resistance to automation by demonstrating a 90% reduction in deployment errors during a pilot phase.
- **Business Continuity:** Orchestrated the "Black Friday" readiness program, coordinating load testing and capacity planning across infrastructure and application teams.
- **Vendor Management:** Managed the relationship with 3rd-party integration partners to ensure legacy APIs were compatible with the new cloud-native architecture.

## Design Decisions
- Rehost legacy .NET apps to Azure App Service.
- Refactor to .NET 6+ where feasible.
- Use Azure SQL Database for backend.
- Integrate with Azure AD for authentication.
- Enable autoscaling and staging slots.

## Assumptions
- Source code is available for all apps.
- No hard OS dependencies.
- Database schemas are compatible with Azure SQL.
- Client will provide test data and UAT support.

## Azure Bill of Materials (BoM) & Cost Estimate

| Service | SKU / Tier | Quantity | Estimated Monthly Cost | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **App Service Plan** | Premium V3 (P1v3) | 2 | ~$350 | Production & Staging |
| **Azure SQL Database** | vCore General Purpose | 2 | ~$400 | Primary & Secondary |
| **Azure Front Door** | Standard | 1 | ~$35 | Global Load Balancing |
| **Azure Redis Cache** | Standard C1 | 1 | ~$100 | Session State |
| **Azure Key Vault** | Standard | 1 | ~$5 | Secrets |
| **App Insights** | Basic | 10 GB | ~$25 | APM |
| **Container Registry** | Standard | 1 | ~$20 | If containerizing |
| **Total Estimated** | | | **~$935 / month** | *Per application environment* |

## Modernization Architecture

### High-Level Diagram
```mermaid
graph TD
    Client[Client Browser] --> AFD[Azure Front Door]
    AFD --> WebApp[Azure App Service (Web App)]
    
    subgraph Azure_PaaS
        WebApp --> SQL[Azure SQL Database]
        WebApp --> Redis[Azure Redis Cache]
        WebApp --> KV[Key Vault]
        WebApp -.-> AppInsights[Application Insights]
    end
    
    subgraph Identity
        WebApp --> AAD[Azure Active Directory]
    end
```

### Terraform Code Snippet (App Service)
```hcl
resource "azurerm_service_plan" "app_plan" {
  name                = "asp-retail-prod-001"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Windows"
  sku_name            = "P1v3"
}

resource "azurerm_windows_web_app" "web_app" {
  name                = "app-retail-frontend-prod"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_service_plan.app_plan.location
  service_plan_id     = azurerm_service_plan.app_plan.id

  site_config {
    always_on = true
    application_stack {
      current_stack  = "dotnet"
      dotnet_version = "v6.0"
    }
  }

  connection_string {
    name  = "SQLConnection"
    type  = "SQLAzure"
    value = "@Microsoft.KeyVault(SecretUri=${azurerm_key_vault_secret.sql_conn.id})"
  }
}
```

## Implementation Plan

### Phase 1: Analysis & Planning
- [ ] Run App Service Migration Assistant on legacy apps.
- [ ] Analyze code for hardcoded paths, registry dependencies, and GAC usage.
- [ ] Define containerization strategy (Code vs. Container).

### Phase 2: Database Migration
- [ ] Use Data Migration Assistant (DMA) for SQL assessment.
- [ ] Migrate schema and data to Azure SQL Database using DMS.
- [ ] Update connection strings to use Key Vault references.

### Phase 3: App Modernization
- [ ] Upgrade .NET Framework to .NET Core/.NET 6+ (Refactor).
- [ ] Implement Azure AD authentication (remove legacy auth).
- [ ] Configure Redis for session state handling.

### Phase 4: Deployment & Cutover
- [ ] Setup CI/CD pipelines in Azure DevOps/GitHub Actions.
- [ ] Deploy to Staging Slot.
- [ ] Perform UAT and Load Testing.
- [ ] Swap to Production.

## RACI Matrix

| Activity | Cloud Architect | Developer Lead | DB Admin | QA Lead |
| :--- | :---: | :---: | :---: | :---: |
| **App Assessment** | R | A | C | I |
| **DB Migration** | C | I | R/A | I |
| **Code Refactoring** | C | R/A | I | I |
| **Pipeline Setup** | R | R | I | I |
| **UAT Sign-off** | I | C | I | R/A |

*R=Responsible, A=Accountable, C=Consulted, I=Informed*

## Success Metrics (KPIs)
- **Deployment Frequency:** Increase from Quarterly to On-Demand/Daily.
- **Scalability:** Ability to handle 5x traffic spikes without manual intervention.
- **SLA:** Achieve 99.95% availability using PaaS redundancy features.

## Artifact Reusability Guide
- **Pattern Type:** App Modernization (Refactor/Replatform).
- **Usage Scenario:** Standard pattern for any .NET/IIS based application migration.
- **Customization Points:** Swap "Azure SQL" for "Cosmos DB" if the application requires global distribution or non-relational data models.
