# Task List: Network Observability & Terraform Project

- [x] **Phase 1: Planning & Design**
  - [x] Analyze input files (Blog MD, Requirements) <!-- id: 0 -->
  - [x] Create Implementation Plan (Team Roles, Component Specs) <!-- id: 1 -->

- [x] **Phase 2: Terraform Development (The "Engine Room")**
  - [x] Initialize `AzureLandingZoneNetworkObservability` directory <!-- id: 2 -->
  - [x] Create `main.tf` (Providers, Backend) <!-- id: 3 -->
  - [x] Create `variables.tf` (Regions, CIDRs, Sub/Tenant IDs) <!-- id: 4 -->
  - [x] Implement `modules/networking` (Hub VNets, Subnets for Firewall/Gateway) <!-- id: 5 -->
  - [x] Implement `modules/firewall` (Azure Firewall Premium, Policies) <!-- id: 6 -->
  - [x] Implement `modules/app_gateway` (WAF v2, Public IP) <!-- id: 7 -->
  - [x] Implement `modules/observability` (Log Analytics, NSG Flow Logs, Traffic Analytics) <!-- id: 8 -->
  - [x] Create `terraform.tfvars` with user's specific IDs <!-- id: 9 -->

- [x] **Phase 2.5: Documentation & Archival**
  - [x] Save artifacts to `master prompts` directory <!-- id: 10 -->

- [x] **Phase 3: Blog Post Creation (The "Story")**
  - [x] Generate HTML content using "Realist Architect" persona <!-- id: 11 -->
  - [x] Create/Place placeholders for diagrams <!-- id: 12 -->
  - [x] Write `blog/2026-02-01-azure-landing-zone-network-observability.html` <!-- id: 13 -->
  - [x] Update `blog.html` index <!-- id: 14 -->

- [/] **Phase 4: Deployment & Verification**
  - [ ] Deploy Terraform (Dry Run / Plan) <!-- id: 15 -->
  - [/] Deploy Blog Post (GitHub/Azure) <!-- id: 16 -->
  - [ ] Verify Live Site <!-- id: 17 -->
