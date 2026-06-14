**Subject:** The Pinning Trap: Why your Agentic AI architecture is a security disaster waiting to happen

**Body:**

Team,

Real-world architecture is rarely as clean as the Visio diagrams.

In my latest post, I break down:
*   **The Problem:** Engineers are building Agents that bypass security boundaries by hardcoding raw Azure OpenAI and Database API keys directly into Semantic Kernel.
*   **The Reality:** This "Pinning Trap" makes your AI un-auditable and expands your blast radius infinitely. When InfoSec rotates a secret, your agents instantly break in production.
*   **The Fix:** You must treat Agentic traffic like external vendor traffic—forcing all LLM orchestration through a zero-trust API Management (APIM) mediation layer.

👉 [Read the full article here](https://portfolio.upendrakumar.com/blog/2026-03-11-agentic-ai-pinning-trap-api-mediation.html)

Best,
Upendra
