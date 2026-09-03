# Quick Start

This quick start is intentionally narrow. It focuses on the **current golden path** in `09-end-to-end-reference-implementation` rather than claiming the whole repo is production-ready.

## Goal

By the end of this quick start you will:

- install the Python dependencies for module 09
- run the local test baseline
- execute the local validation script
- understand the limits of the current repo state

## Prerequisites

- Python 3.10 or 3.11
- PowerShell 7+ on Windows, or adapt the commands for your shell
- Git
- Azure CLI only if you plan to try the Bicep deployment flow

## 1. Open the Repo

```powershell
git clone https://github.com/appliedailearner/azure-agentic-ai-architect-labs.git
cd azure-agentic-ai-architect-labs
```

## 2. Create a Virtual Environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r .\09-end-to-end-reference-implementation\requirements.txt
```

## 3. Run the Golden Path Tests

```powershell
$env:PYTHONPATH = (Resolve-Path .\09-end-to-end-reference-implementation).Path
pytest .\09-end-to-end-reference-implementation\app\tests -q
```

Expected result:

- the module 09 unit and integration baseline passes locally

## 4. Run the Repo Validation Script

```powershell
.\09-end-to-end-reference-implementation\validate.ps1
```

Expected result:

- the script confirms required files exist
- the tests run successfully
- the repo prints the current support boundary

## 5. Review the Architecture Before Deployment

Read these before using Azure resources:

- [REFERENCE-ARCHITECTURE.md](./REFERENCE-ARCHITECTURE.md)
- [ARCHITECTURE.md](./ARCHITECTURE.md)
- [09-end-to-end-reference-implementation/DEPLOYMENT-GUIDE.md](./09-end-to-end-reference-implementation/DEPLOYMENT-GUIDE.md)

## 6. Optional: Validate Bicep Prerequisites

If you want to inspect the deployment path:

```powershell
az login
cd .\09-end-to-end-reference-implementation\deployment
$env:VALIDATE_ONLY = "true"
bash ./deploy.sh dev eastus
```

This is optional and not required for the week-one baseline.

## What This Quick Start Does Not Promise

This quick start does **not** currently guarantee:

- a full production deployment
- completed security and governance controls
- validated environment promotion across dev, test, and prod
- that every module in the repo is runnable today

## Next Documents

- [MODULE-STATUS.md](./MODULE-STATUS.md)
- [docs/repo-map.md](./docs/repo-map.md)
- [09-end-to-end-reference-implementation/README.md](./09-end-to-end-reference-implementation/README.md)
