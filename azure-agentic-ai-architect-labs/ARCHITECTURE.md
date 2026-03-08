# Architecture Overview

This file is the short-form architecture summary for the current repo baseline.

For the authoritative target shape of the current golden path, use [REFERENCE-ARCHITECTURE.md](./REFERENCE-ARCHITECTURE.md).

## Current Architectural Position

The repo is converging on an Azure-first reference pattern with these design choices:

- Azure AI Foundry or Azure-hosted model endpoints for model execution
- Azure AI Search for retrieval
- explicit tool boundaries for enterprise integrations
- Bicep as the primary infrastructure-as-code direction
- a staged move toward secure-by-default deployment patterns

## Current Scope

At week-one stabilization, only module 09 should be treated as the primary architectural path:

- [09-end-to-end-reference-implementation](./09-end-to-end-reference-implementation/README.md)

The remaining modules are still curriculum assets under review and should not be treated as equal implementation proof.

## Architecture Rules for This Repo

- do not claim production readiness without matching code and operations evidence
- prefer Azure-native services and current terminology
- keep one canonical golden path rather than several partial ones
- separate educational breadth from enterprise implementation depth

## Next-Level Artifacts Still Needed

- threat model
- security baseline
- governance model
- environment overlays
- observability standard
- evaluation harness
