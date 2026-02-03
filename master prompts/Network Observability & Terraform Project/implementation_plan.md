# Implementation Plan: Azure Landing Zone Network Observability

## Goal
Create a "Realist Architect" blog post and a functional Terraform code repository for an Azure Landing Zone Network Observability solution using Azure Firewall Premium, App Gateway WAF, and Traffic Analytics.

## Team Roles & Responsibilities
*   **Lead Cloud Architect:** Overall design (Hub-Spoke in UK South/Central), blog narrative structure.
*   **Security Architect:** Firewall Premium SKU justification, WAF Policy strictness, IDPS configuration.
*   **Network Architect:** IP Addressing (CIDRs), UDRs to force inspection, Peering topology.
*   **DevOps Engineer:** Terraform modular structure, state management, provider configuration.

## User Context
*   **Subscription ID:** `87cf2b93-5e52-4533-9e6b-7182cd7dbde6`
*   **Tenant ID:** `5f51e0e9-4a52-494f-8068-27a3527967de`
*   **Region:** UK South (Primary), UK Central (DR)
*   **Repo Name:** `AzureLandingZoneNetworkObservability` (Local path to be created)

## Proposed Changes

### 1. Terraform Codebase (`C:\MyResumePortfolio\AzureLandingZoneNetworkObservability\`)
We will create a structured Terraform project.

#### [NEW] `provider.tf`
*   AzureRM Provider (Latest)
*   User's Tenant/Sub IDs

#### [NEW] `variables.tf`
*   `location_primary` = "uksouth"
*   `location_dr` = "ukwest" (or ukcentral if preferred, usually UK West is the pair for UK South)
*   `hub_vnet_cidr` = "10.0.0.0/16"
*   `firewall_subnet_cidr` = "10.0.1.0/24"

#### [NEW] Modules
*   `modules/core`: Resource Groups, Log Analytics Workspace
*   `modules/networking`: VNets (Hub), Subnets (AzureFirewallSubnet, GatewaySubnet), Peering
*   `modules/security`: Azure Firewall Premium, Firewall Policies (Rule Collection Groups), App Gateway WAF v2
*   `modules/observability`: Network Watcher, NSG Flow Logs, Traffic Analytics

### 2. Blog Post (`C:\MyResumePortfolio\blog\`)

#### [NEW] `2026-02-01-azure-landing-zone-network-observability.html`
*   **Voice:** "Realist Architect" (Upendra).
*   **Structure:**
    *   **Hook:** "Most cloud incidents are not 'Azure went down'."
    *   **The Trap:** "The Enterprise-Scale Blindfold" (Deploying LZ without eyes).
    *   **The Fix:** "The Observability Trinity" (Firewall, WAF, Flow Logs).
    *   **Architecture:** Diagrams + Terraform snippets.
    *   **CTA:** Link to the Github Repo (we will link to the one we are "creating").

#### [MODIFY] `blog.html`
*   Add the new post card to the index.

## Verification Plan
1.  **Terraform:** Run `terraform init` and `terraform plan` (if credentials allow, otherwise simple syntax check).
2.  **Blog:** Verify HTML rendering locally and deploy via `deploy-both.ps1`.

## Documentation
*   **Archival:** Copy `task.md` and `implementation_plan.md` to `C:\MyResumePortfolio\master prompts\Network Observability & Terraform Project`.
