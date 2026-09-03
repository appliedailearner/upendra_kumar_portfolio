# Module 09: End-to-End Reference Implementation

This module is the **current golden path** for the repository. It is the only module that should currently be used as the recommended execution path.

## Current Scope

This module provides:

- a Python agent baseline
- supporting tests
- a Bicep deployment baseline
- a local validation script

It does **not** yet prove full enterprise readiness. It is the week-one implementation baseline that the rest of the repo will be hardened around.

## Module Layout

```text
09-end-to-end-reference-implementation/
├── app/
│   ├── agent.py
│   ├── config.py
│   ├── agents/
│   ├── tools/
│   └── tests/
├── deployment/
├── infra/
├── .env.example
├── requirements.txt
├── validate.ps1
└── DEPLOYMENT-GUIDE.md
```

## Local Validation Path

### 1. Install dependencies

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r .\requirements.txt
```

### 2. Run tests

```powershell
$env:PYTHONPATH = (Resolve-Path .).Path
pytest .\app\tests -q
```

### 3. Run the validation script

```powershell
.\validate.ps1
```

## Expected Outcome

The current local baseline is considered healthy when:

- tests pass locally
- the validation script confirms required files exist
- the support boundary is understood before any Azure deployment attempt

## Deployment Note

The deployment scripts and Bicep are still part of the repo evolution. Treat Azure deployment here as a baseline for iteration, not as a finished production landing zone.

Use [DEPLOYMENT-GUIDE.md](./DEPLOYMENT-GUIDE.md) only after reading the repo-level architecture docs.
