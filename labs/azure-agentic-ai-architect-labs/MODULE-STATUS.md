# Module Status

This file is the source of truth for module maturity. The goal is to replace assumption-based claims with explicit status.

Status definitions:

- `Draft`: content exists but is not yet validated end to end
- `Runnable Baseline`: a local execution path exists
- `Validated`: reviewed and executed against the documented path
- `Archive Candidate`: duplicate or legacy content that should be merged, renamed, or retired

| Module | Purpose | Status | Recommended Use | Owner | Last Reviewed |
| --- | --- | --- | --- | --- | --- |
| `01-foundry-foundations` | Foundational Azure AI and Foundry concepts | Draft | Read-only until standardized | Repo maintainer | 2026-03-08 |
| `02-foundry-agent-service` | Foundry agent service exploration | Draft | Read-only until standardized | Repo maintainer | 2026-03-08 |
| `03-semantic-kernel-track` | Semantic Kernel-oriented patterns | Draft | Read-only until standardized | Repo maintainer | 2026-03-08 |
| `04-agent-framework-and-multi-agent` | Multi-agent and orchestration experiments | Draft | Read-only until standardized | Repo maintainer | 2026-03-08 |
| `05-rag-with-azure-ai-search` | Retrieval and knowledge grounding patterns | Draft | Read-only until standardized | Repo maintainer | 2026-03-08 |
| `06-mcp-and-enterprise-tooling` | MCP and enterprise tool integration patterns | Draft | Read-only until standardized | Repo maintainer | 2026-03-08 |
| `07-secure-reference-architecture` | Security-focused reference assets | Draft | Read-only until standardized | Repo maintainer | 2026-03-08 |
| `08-observability-and-evaluation` | Evaluation and observability assets | Draft | Read-only until standardized | Repo maintainer | 2026-03-08 |
| `09-end-to-end-reference-implementation` | Current golden path | Runnable Baseline | Primary execution path | Repo maintainer | 2026-03-08 |
| `reference-architecture-diagram` | Duplicate diagram folder | Archive Candidate | Do not extend | Repo maintainer | 2026-03-08 |
| `reference-architecture-diagrams` | Diagram source folder under review | Draft | Keep until consolidation | Repo maintainer | 2026-03-08 |

## Week-One Decision

Until more modules are validated, only module 09 should be presented as the working baseline.

## Promotion Rule

A module should not move from `Draft` to `Runnable Baseline` until it has:

- a setup path
- a run path
- a validation step
- expected output
- troubleshooting notes

A module should not move to `Validated` until someone executes those steps successfully and updates this file.
