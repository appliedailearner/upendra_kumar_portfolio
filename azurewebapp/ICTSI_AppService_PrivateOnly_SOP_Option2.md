# ICTSI App Service Private-Only SOP
Option 2: Disable Public Network Access and use Private Endpoint (Singapore example)
Date: 25 Feb 2026

## Revision history
| Version | Date        | Author    | Notes                                                                                                    |
| :---    | :---        | :---      | :---                                                                                                     |
| v3.4    | 25 Feb 2026 | Generated | PDF baseline (Option 2 only), formatting QA complete                                                     |
| v3.5    | 25 Feb 2026 | Generated | Word editable. Fixes screenshots ambiguity, adds per-app checklist, strengthens APIM dependency clarity. |
| v3.6    | 25 Feb 2026 | Generated | Architecture upgrades (IaC, APIM Trace, CI/CD Patterns, Monitoring, TLS details, Troubleshooting).       |
| v4.0    | 25 Feb 2026 | Generated | Added "Appendix D: Advanced Architecture Scenarios & Use Cases" based on Official Azure Quickstarts.     |

---

## 1. Purpose and scope
This SOP shows how to restrict Azure App Service Web Apps to private access only using Private Endpoint (Private Link) and by disabling public network access. After completion, the web apps cannot be reached from the public internet. Only clients that can reach the target VNet can access the apps.

**Why this exists (problem statement)**
If Public network access is enabled, the default `https://<app>.azurewebsites.net` URL is reachable on the internet. That allows direct access to the backend API and Swagger, bypassing API Management (APIM) policies such as auth, rate limit, and WAF controls. Microsoft Support recommended Option 2 as the stronger long-term fix: disable public access and/or use a private endpoint.

## 2. Target web apps

| Web App name            | Private Endpoint name (example)  | Private IP (example) |
| :---                    | :---                             | :---                 |
| ictsi-restapi-v1        | pe-ictsi-restapi-v1              | 10.50.10.4           |
| ictsi-restapi-test-002  | pe-ictsi-restapi-test-002        | 10.50.10.5           |
| ictsi-event-grid-viewer | pe-ictsi-event-grid-viewer       | 10.50.10.6           |

## 3. Simple mental model (analogy)
Think of your Web App as a building with two doors:
* **Door 1: Public door (internet)**. Anyone can try it if it is unlocked.
* **Door 2: Private door (inside your VNet)**. Only people inside the building campus can reach it.

A Private Endpoint creates the private door. Disabling public network access locks the public door.

## 4. Architecture overview
High-level flow (private-only):
*(Figure: Private Endpoint places App Service behind a private IP in the VNet.)*

## 5. Prerequisites and constraints
Before you start, confirm:
1. App Service plan supports Private Endpoint (not Free/Shared).
2. You have RBAC rights to create Private Endpoints, Private DNS zones, and to approve private endpoint connections.
3. APIM (or any caller) must have private network reachability to `vnet-ictsi-sea-01` (same VNet, peering, or VPN/ExpressRoute).
4. You have a VM/jumpbox or self-hosted agent inside the VNet for testing and (if needed) deployments.

> [!WARNING]
> CI/CD and SCM (Kudu) impact (do not skip)
> When you disable public network access, public GitHub/Azure DevOps hosted agents will not be able to deploy using Kudu/ZipDeploy.
> **Architectural Upgrade:** Use self-hosted runners/agents inside the private network (e.g., Azure Container Apps or VMSS agents joined to `vnet-ictsi-sea-01`). Alternatively, use Azure DevOps Service Tags or Run From Package (URL).
> DNS must include both records: `<app>` and `<app>.scm` in the private DNS zone.

## 6. Example naming and parameters

| Item                      | Example value                              |
| :---                      | :---                                       |
| Region                    | Southeast Asia (Singapore)                 |
| Resource group            | rg-ictsi-prod-sea-01                       |
| Virtual network           | vnet-ictsi-sea-01                          |
| Private endpoint subnet   | snet-private-endpoints (10.50.10.0/24)     |
| Private DNS zone (required) | privatelink.azurewebsites.net            |

## 7. Go/No-Go checklist (before cutover)
Do not disable public network access until all items are TRUE.

| App                     | PE created | Connection state | DNS (app+scm) | Private test | APIM test | Public access disabled |
| :---                    | :---       | :---             | :---          | :---         | :---      | :---                   |
| ictsi-restapi-v1        | Yes/No     | Approved         | Yes/No        | Yes/No       | Yes/No    | Yes/No                 |
| ictsi-restapi-test-002  | Yes/No     | Approved         | Yes/No        | Yes/No       | Yes/No    | Yes/No                 |
| ictsi-event-grid-viewer | Yes/No     | Approved         | Yes/No        | Yes/No       | Yes/No    | Yes/No                 |

> [!IMPORTANT]
> **APIM dependency (most common outage cause)**
> If APIM is not able to reach the private IP (routing) AND resolve the name to that private IP (DNS), APIM calls will fail after cutover. Validate APIM reachability before disabling public access. 
> 
> **CRITICAL ARCHITECT NOTE:** You *cannot* use a Private Endpoint *on* APIM to route traffic *to* a Private Endpoint on an App Service. If APIM is public-only or using a Private Endpoint today, you must first move APIM into **VNet Integration (External or Internal Mode)**. This is the only Microsoft-supported model to route outbound traffic directly into your virtual network to hit the App Service Private IP.

## 8. Step-by-step procedure (repeat per app)
Perform steps 8.1 to 8.7 for each web app. Recommended approach: complete all Private Endpoints and DNS first, validate privately, then do the public access cutover as the final step.

### 8.1 Capture current state
For each app, record:
1. Current Public network access state (Enabled/Disabled).
2. Any deployment slots in use (each slot needs its own private endpoint).
3. Whether CI/CD uses public Kudu/ZipDeploy.

### 8.2 Create or confirm Private DNS zone and VNet link
Create or confirm the Private DNS zone:
* Private DNS zone name: `privatelink.azurewebsites.net`
* Link it to VNet: `vnet-ictsi-sea-01` (enable auto-registration: No).
* If you use enterprise DNS, configure forwarding so workloads in the VNet can resolve this zone.

### 8.3 Create Private Endpoint for the Web App
**Portal path:** Web App > Networking > Private endpoints > Add.
**Wizard (Virtual Network):** choose the VNet and the private endpoint subnet.

> [!TIP]
> **Subnet note:** A dedicated subnet for private endpoints is recommended for clarity, but not required. Private endpoint network policies are disabled by default.

### 8.4 Approve the private endpoint connection (if Pending)
Portal path: Web App > Networking > Private endpoint connections.
If the connection state is Pending, select the connection row, then click **Approve**.

### 8.5 Validate private name resolution and private connectivity
Run these tests from a VM/jumpbox inside the target VNet (or a peered VNet with the same DNS view).

```bash
# DNS checks (run from inside the VNet)
nslookup ictsi-restapi-v1.azurewebsites.net
nslookup ictsi-restapi-v1.scm.azurewebsites.net
nslookup ictsi-restapi-test-002.azurewebsites.net
nslookup ictsi-event-grid-viewer.azurewebsites.net

# Connectivity check (HTTPS)
curl -I https://ictsi-restapi-v1.azurewebsites.net
curl -I https://ictsi-restapi-test-002.azurewebsites.net
curl -I https://ictsi-event-grid-viewer.azurewebsites.net
```

**Expected results inside the VNet:**
* `<app>.azurewebsites.net` resolves to a private IP (for example `10.50.10.x`).
* Both `app` and `scm` names resolve privately.
* `curl` succeeds (HTTP 200/302/etc based on your app).

> [!NOTE] 
> **APIM Validation Upgrade:** Use the **APIM Test Console** or enable **Ocp-Apim-Trace**. Verify that APIM can successfully route to the Web App's new Private IP.

### 8.6 Pre-Cutover Metric Monitoring (Architect Upgrade)
Before cutting over, open the App Service Logs & Metrics dashboard. Monitor "HTTP 4xx Errors" and "HTTP 5xx Errors". Ensure you have a baseline for 5-10 minutes prior to the change.

### 8.7 Cutover: disable public network access
This is the step that removes internet reachability. Do this only after Step 8.5 succeeds for the app and APIM reachability is confirmed.

1. Portal path: Web App > Networking > Inbound traffic configuration > Public network access.
2. Set Public network access to Disabled, then click Save.
3. Re-open the blade and confirm it still shows Disabled (save succeeded).

### 8.8 Post-cutover validation
After disabling public network access:
1. **Public Test:** From an internet-connected machine (outside the VNet), `https://<app>.azurewebsites.net` should fail to load (HTTP 403).
2. **Private Test:** From inside the VNet, the app should still respond.
3. **APIM Test:** From APIM, backend calls must succeed (end-to-end test). Check metrics again to ensure no unexpected spike in HTTP 403s.

## 9. Rollback (2-minute recovery)
If production impact occurs:
1. Set Public network access back to Enabled (temporarily) and Save.
2. Confirm service is restored via APIM and direct testing.
3. Fix DNS/routing/approval issues, then repeat Step 8.5 and 8.7.

## 10. Notes and gotchas
* **Slots:** Each deployment slot is treated as a separate target. Create and approve a private endpoint per slot.
* **Access restrictions:** Access restrictions are not evaluated for private endpoint traffic. Public network access is the isolation control.
* **TLS Custom Domains:** Always use `https://<app>.azurewebsites.net` in tests. If APIM uses a custom domain (e.g., `api.ictsi.com`), the custom domain still needs a Public DNS CNAME pointing to the App Service. However, the `privatelink` DNS zone handles the internal routing without breaking the TLS certificate seal.

## 11. Custom Automation Snippets (IaC Appendix)
To avoid manual ClickOps drift in the portal, use these scripts for repeatable execution.

```bash
# Azure CLI Example: Create Private Endpoint
az network private-endpoint create \
  --name pe-<app-name> --resource-group <rg-name> --vnet-name <vnet-name> --subnet <subnet-name> \
  --private-connection-resource-id <app-service-id> --group-id sites --connection-name pe-connection-<app-name>

# Azure CLI Example: Disable Public Network Access
az webapp update --name <app-name> --resource-group <rg-name> --set publicNetworkAccess=Disabled
```

## 12. Troubleshooting Matrix
| Symptom                  | Root Cause & Solution |
| :---                     | :---                  |
| **HTTP 403 (Forbidden)** | Request came from outside the VNet after PNA was disabled, or traffic traversed the public endpoint instead of the private endpoint. |
| **NXDOMAIN**             | DNS Resolution Error: The `privatelink.azurewebsites.net` zone is not linked to the caller's VNet, or DNS forwarding is misconfigured. |
| **HTTP 502/503**         | APIM found the private endpoint but cannot establish a backend connection (Check NSG rules or subnet delegation). |

---

**Appendix A. Per-app execution checklist**
*(Use this table during implementation and attach it to the change record.)*

| App                     | PE created | PE approved | DNS app | DNS scm | Private test | APIM test | PNA disabled |
| :---                    | :---       | :---        | :---    | :---    | :---         | :---      | :---         |
| ictsi-restapi-v1        | []         | []          | []      | []      | []           | []        | []           |
| ictsi-restapi-test-002  | []         | []          | []      | []      | []           | []        | []           |
| ictsi-event-grid-viewer | []         | []          | []      | []      | []           | []        | []           |

**Appendix B. Reference docs**
* Azure App Service Private Endpoint overview: https://learn.microsoft.com/en-us/azure/app-service/overview-private-endpoint
* Create a private endpoint (portal): https://learn.microsoft.com/en-us/azure/private-link/create-private-endpoint-portal
* Private endpoint connection approval: https://learn.microsoft.com/en-us/azure/private-link/manage-private-endpoint

---

**Appendix C: APIM Integration Guide (For Freshers)**

When the App Service goes private, API Management (APIM) is the **only** way external users can reach your API. If APIM is not configured correctly, your API will be completely broken.

Follow these step-by-step instructions:

**Step 1: Ensure APIM is inside the VNet**
1. In the Azure Portal, open your API Management instance.
2. On the left menu under **Security**, click **Network**.
3. Confirm that **Virtual network** is set to either **External** or **Internal** (Not "None").
4. Check the **Virtual network** and **Subnet** listed. It must be `vnet-ictsi-sea-01` (or a VNet that is peered to it).
*(Note: If it says "None", stop here. You must migrate APIM to a VNet first, which is a major architectural change. Consult a senior architect.)*

**Step 2: Link the DNS Zone to the APIM VNet**
If APIM is in a VNet, it needs to know how to translate `ictsi-restapi-v1.azurewebsites.net` into the Private IP (`10.50.10.x`).
1. Search for **Private DNS zones** in the top search bar and open `privatelink.azurewebsites.net`.
2. On the left menu, click **Virtual network links**.
3. Check if the VNet where your APIM lives is listed here.
4. If not, click **+ Add**, name it `link-to-apim-vnet`, and select your APIM's VNet. Click **OK**.

**Step 3: Update the APIM Backend IP (If using Custom DNS)**
If your APIM policy uses `set-backend-service`, make sure the backend URL is still pointing to the `https://<app>.azurewebsites.net` address, NOT a hardcoded public IP address.

**Step 4: Test from APIM (End-to-End)**
Before declaring success, you must prove APIM can talk to the private App Service.
1. Open your API Management instance in the Azure Portal.
2. In the left menu, click **APIs**.
3. Select your API (e.g., `ICTSI REST API v1`).
4. Click on the **Test** tab at the top.
5. Select an operation (like `GET /health` or `GET /users`).
6. Scroll down and click **Send**.
7. Scroll down to the **HTTP response**. Ideally, you should see `HTTP/1.1 200 OK`. 
8. If you get `503 Service Unavailable`, click the **Trace** tab to see exactly where the connection failed.

---

**Appendix D: Advanced Architecture Scenarios & Use Cases**

Depending on your enterprise requirements, separating frontend from backend or injecting WAF/Gateways requires specific Private Endpoint topologies. Microsoft provides official Quickstart templates for the following robust architectural patterns.

### Use Case 1: The Baseline Private Web App
**Scenario:** You need a single Web App entirely isolated from the public internet, accessible only from within the corporate VNet via a Jumpbox, ExpressRoute, or VPN.
* **Architecture:** VNet + Subnet + Private Endpoint attached to the App Service. The Private DNS Zone (`privatelink.azurewebsites.net`) translates the default FQDN to the Private IP.
* **Official Microsoft Lab & Template:** [Deploy Web App with Private Endpoint](https://learn.microsoft.com/en-us/samples/azure/azure-quickstart-templates/private-endpoint-webapp/)

### Use Case 2: Secure N-Tier Architecture (Frontend to Private Backend)
**Scenario:** You have a public-facing Frontend Web App (UI) that needs to securely communicate with a Backend App Service (API/Database logic), ensuring the Backend is never exposed to the internet.
* **Architecture:** The Frontend App Service utilizes **VNet Regional Integration** (outbound routing into a VNet subnet). The Backend App Service has **Public Network Access Disabled** and an inbound **Private Endpoint**. The Frontend routes privately through the VNet to reach the Backend.
* **Official Microsoft Lab & Template:** [Deploy Secure N-Tier Web App](https://learn.microsoft.com/en-us/samples/azure/azure-quickstart-templates/webapp-secure-ntier/)

### Use Case 3: Public Ingress via Application Gateway (WAF) to Private Web App
**Scenario:** You need Enterprise-grade Layer 7 protection (Web Application Firewall). All traffic must hit the Application Gateway first, and users should not be able to bypass the WAF to hit the App Service directly.
* **Architecture:** An Application Gateway v2 is deployed with a Public IP. Its backend pool targets the FQDN of your App Service. The App Service is locked behind a **Private Endpoint**. The App Gateway sits in a peered VNet and resolves the App Service to its private IP using the Private DNS Zone.
* **Official Microsoft Lab & Template:** [Web App + Private Endpoint + Application Gateway v2](https://learn.microsoft.com/en-us/samples/azure/azure-quickstart-templates/webapp-windows-with-privateendpoint-applicationgateway/)

### Use Case 4: App Service Outbound to Private Azure SQL Database
**Scenario:** Your App Service needs to securely query an Azure SQL Database. Compliance dictates that the SQL Database cannot have public endpoints exposed, even if restricted by firewall rules.
* **Architecture:** This is the reverse of traditional Private Endpoint scenarios. The Azure SQL Server gets the **Private Endpoint**. The App Service uses **VNet Regional Integration** to route its outbound SQL queries (`1433`) securely into the VNet, across the Microsoft Backbone, to the SQL Private IP.
* **Official Microsoft Lab & Template:** [App Service uses SQL over Private Endpoint](https://learn.microsoft.com/en-us/samples/azure/azure-quickstart-templates/private-endpoint-sql-from-appservice/)

### Use Case 5: The "Gold Standard" Enterprise APIM + WAF + Private App
**Scenario:** The most secure topology. A public WAF filters malicious traffic, forwards it to an internal API Gateway for rate limiting and JWT validation, which then routes it to a private, isolated backend API.
* **Architecture:** Application Gateway (Public) -> API Management (Internal VNet Mode) -> App Service (Private Endpoint).
* *Note: The official quickstart template for this specific three-tier flow was marked as deprecated by Microsoft, but the architectural pattern remains the enterprise standard for Zero Trust networks.*
* **Reference Template:** [App Gateway + Internal APIM + Web App (Legacy)](https://learn.microsoft.com/en-us/samples/azure/azure-quickstart-templates/private-webapp-with-app-gateway-and-apim/)

### Bonus Use Case: Function App with Secure Storage Backend
**Scenario:** You are using Azure Functions for serverless processing, but the Azure Storage Account holding the Function's core executables and state data must be locked down to prevent data exfiltration.
* **Architecture:** The Function App has VNet Integration to route traffic into the VNet. The Storage account has a **Private Endpoint** (specifically for `blob`, `file`, `queue`, and `table` sub-resources). The Function pulls its code privately.
* **Official Microsoft Lab & Template:** [Function App + Secure Storage Endpoints](https://learn.microsoft.com/en-us/samples/azure/azure-quickstart-templates/function-app-storage-private-endpoints/)
