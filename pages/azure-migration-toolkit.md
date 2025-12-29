---
layout: page
title: Azure Migration Toolkit
permalink: /pages/azure-migration-toolkit.html
---

# Azure Migration Toolkit

This toolkit accompanies the insights from my article, ["The Azure Migration That Almost Failed"](/blog/2025-12-29-azure-migration-that-almost-failed.html). It provides the practical artifacts, templates, and structures we used to turn the program around.

These resources are designed to be "forkable"—take them, adapt them to your organization, and use them to drive clarity and execution.

## 1. Portfolio Assessment Matrix (Excel Template)

A structured approach to analyzing your application portfolio before moving a single bit. This matrix moves beyond simple inventory to actionable "Move Groups."

### Key Columns
*   **Application ID & Name**: Unique identifiers.
*   **Business Criticality (Tier 1-4)**: Defines RTO/RPO requirements.
*   **Data Classification**: Public, Internal, Confidential, Restricted.
*   **Technical Complexity Score (1-5)**: Based on dependencies, legacy protocols, and hardcoded configs.
*   **Migration Strategy (The 6 Rs)**: Rehost, Refactor, Rearchitect, Rebuild, Replace, Retire.
*   **Move Group ID**: Logical grouping of apps that must move together.
*   **Target Landing Zone**: Subscription/Resource Group destination.

[**View Template Structure**](/docs/azure-migration-specs.html#portfolio-assessment-matrix)

---

## 2. Right-Sizing & TCO Calculator

Don't lift-and-shift waste. This model helps you calculate the true cost of migration by factoring in right-sizing, Hybrid Benefit, and Reservations.

### Features
*   **Baseline Cost**: Current on-prem hardware/licensing cost.
*   **Azure List Price**: Raw cost of equivalent Azure resources.
*   **Optimized Cost**: Cost after applying:
    *   **Right-Sizing**: Adjusting vCPU/RAM based on 95th percentile usage.
    *   **AHB (Azure Hybrid Benefit)**: Reusing on-prem Windows/SQL licenses.
    *   **Reserved Instances (RI)**: 1-year or 3-year commitments.
*   **ROI Projection**: 3-year total cost of ownership comparison.

[**View Calculation Logic**](/docs/azure-migration-specs.html#right-sizing--tco-calculator)

---

## 3. Migration Runbook (Word/Markdown Template)

The "boring" checklist that saves weekends. This runbook details the minute-by-minute execution plan for a cutover event.

### Phases
1.  **T-Minus 4 Weeks (Planning)**: Stakeholder comms, freeze windows, prerequisite checks.
2.  **T-Minus 1 Week (Staging)**: Data replication sync, initial testing, connectivity validation.
3.  **T-Minus 24 Hours (Go/No-Go)**: Final sign-offs, rollback plan verification.
4.  **T-Zero (Cutover)**: Service stop, final sync, DNS switch, smoke testing.
5.  **Post-Migration (Hypercare)**: Monitoring, issue tracking, stakeholder updates.

[**View Runbook Template**](/docs/azure-migration-specs.html#migration-runbook)

---

## 4. Operating Model Repository Structure

Infrastructure as Code (IaC) is not enough. You need "Policy as Code" and "Decisions as Code." This repository structure organizes your cloud operating model.

### Recommended Structure
*   `/decisions`: RFCs and Architecture Decision Records (ADRs).
*   `/policies`: Azure Policy definitions (JSON/Bicep).
*   `/governance`: Naming conventions, tagging standards, RBAC models.
*   `/patterns`: Approved reference architectures (e.g., "Standard Web App", "AKS Cluster").
*   `/automation`: Scripts for bootstrapping subscriptions and governance.

[**View Repo Structure**](/docs/azure-migration-specs.html#operating-model-repository)

---

## 5. Architecture Diagrams

Visualizing the target state is critical for alignment.

### Hub-and-Spoke Network Topology
Illustrates the central connectivity hub (Firewall, ExpressRoute, VPN) and the segregated spoke subscriptions for workloads, enforcing traffic inspection and isolation.

### Identity & Access Management (IAM) Model
Depicts the hierarchy of Management Groups, Subscriptions, and Resource Groups, mapped to Entra ID groups and Custom Roles for "Least Privilege" access.

[**View Diagram Descriptions**](/docs/azure-migration-specs.html#architecture-diagrams)
