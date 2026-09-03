# 🎭 Microsoft Partner/Director (AB-100 Focus) Mock Interview Transcript

**Candidate:** Upendra Kumar (Targeting Principal Director, Agentic AI Business Solutions Architect)
**Interviewer:** "Sarah" (Partner Director of Engineering, Azure AI)
**Focus Areas:** Copilot Studio vs Foundry, Multi-Agent Orchestration, API Mediation, and Enterprise Governance.

---

## 🎙️ Scenario 1: Solution Selection (Deal-Breaker Question)
*Microsoft L67s must know the difference between SaaS low-code agents and PaaS custom orchestration.*

**Sarah (Interviewer):** We have a massive banking client. Their business units want to deploy 50 different "agents" next quarter. The CRM team wants to use Copilot Studio because they don't have python developers, while the Core Banking team wants to build everything custom on Azure AI Foundry using Semantic Kernel. The CIO is looking to you for a platform standard. How do you govern this?

**Upendra (Interviewee):** 
**[Situation]** This is the most common anti-pattern happening right now: "Agent Sprawl" caused by religious debates over build vs. buy. I experienced this when advising an FSI client who had duplicate licensing costs because teams were fighting over tools.

**[Task]** My job is not to pick a winner, but to establish an objective **Architecture Decision Matrix** aligned with the AB-100 strategy.

**[Action]** I brought the application owners into a room and removed technology from the discussion. I mapped their workflows to process ownership and extensibility bounds.
1. For the CRM team, their workflows were predominantly Q&A against SharePoint and Dynamics 365, requiring pre-integrated declarative actions. I anchored them strictly to **Copilot Studio**. It provides massive speed-to-value for business-led automation.
2. For the Core Banking team, their use case involved multi-agent orchestration, complex data grounding demanding custom vector retrieval logic, and direct Model Context Protocol (MCP) integrations with legacy mainframes. Copilot Studio is too rigid for this. I aligned them to a code-first approach using **Semantic Kernel** inside **Azure AI Foundry**.

**[Result]** By mapping the platform choice to the *process requirement* rather than technical preference, we established a clear center of excellence. We avoided millions in custom build costs for basic tasks, while reserving Azure AI Foundry for the tier-1 deterministic workflows. 

---

## 🎙️ Scenario 2: Agent Architecture Mistakes (The Monolith)
*Do you understand how to design resilient agents, or are you just wrapping an OpenAI API call?*

**Sarah (Interviewer):** That's a strong business alignment. Let's look at the Core Banking team's custom build. They built a single "Super Agent" with a massive 15,000-token prompt and gave it 12 different tools. It's supposed to research customer history, calculate risk, and approve loans. It's failing. It hallucinates, loops forever, and is incredibly expensive. What did they do wrong, and how do you fix it?

**Upendra (Interviewee):**
**[Situation]** They fell into the number one agentic architecture trap: treating an LLM like a monolithic application. A single agent trying to plan, research, and execute simultaneously will suffer from "attention collapse" and hallucinate wildly.

**[Task]** I needed to decompose their monolith into a resilient, verifiable system.

**[Action]** 
1. I ripped out the single agent and introduced a **Multi-Agent Orchestration Pattern**. 
2. I created a **Coordinator Agent** (using GPT-4o). Its only job is intent classification and planning. It doesn't do the work; it delegates it.
3. It routes tasks to specialized **Worker Agents** (run on cheaper, faster GPT-4-mini models). We have a "Researcher Agent" that strictly queries Azure AI Search via RAG. We have an "Analyst Agent" that purely runs the risk calculation python scripts. 
4. Crucially, I introduced an **Evaluator Agent** acting as a quality gate to verify the output against the original user intent before presenting it.

**[Result]** By forcing the LLMs into tight, deterministic swimlanes, we eliminated the infinite loops. Token costs dropped by 40% because we weren't sending a 15k prompt on every iteration, and the hallucination rate dropped to near zero because the Coordinator validated every step.

---

## 🎙️ Scenario 3: The API Mediation Layer (Security & Governance)
*How do you prevent an AI from destroying a company?*

**Sarah (Interviewer):** Okay, so your agents are cooperating beautifully. But the Risk calculation agent needs to actually execute a transaction in the core banking ledger. Giving an autonomous LLM write-access to a ledger terrifies me. How do you govern tool-calling so the CISO doesn't shut the whole project down?

**Upendra (Interviewee):**
**[Situation]** They absolutely should be terrified. Developers often expose REST APIs directly to Semantic Kernel plugins as raw OpenAPI specs. If an agent hallucinates a tool call, it hits the production system directly. This is a massive zero-trust violation.

**[Task]** I had to design a zero-trust boundary so the LLM could execute tools without raw system access.

**[Action]** 
I introduced the **API Mediation Layer**.
1. No Semantic Kernel agent or Copilot Studio action is allowed to talk to the core banking API directly. 
2. Instead, all tool calls are routed through **Azure API Management (APIM)** which is placed inside a private VNET.
3. APIM acts as the hardened perimeter. It strips the payload, enforces OAuth 2.0 token validation, validates that the payload schema exactly matches expectations, and applies strict rate limits (e.g., 5 transactions a minute). 
4. I also wired APIM to output every single agent request payload into a Log Analytics workspace for non-repudiation auditing. 

**[Result]** The CISO approved the architecture because the LLM was treated exactly like any other untrusted external third-party system. We decoupled the intelligence layer from the execution layer, ensuring that even a total hallucination breakdown would be blocked safely at the gateway level.

---

## 🎯 Summary of Candidate (Upendra) Feedback:
*   **Strengths:** Demonstrates elite understanding of the AB-100 curriculum. Doesn't just say "we built an agent." Proactively introduces multi-agent orchestration, differentiates between Copilot Studio and Foundry properly, and solves the critical enterprise hurdle: API tool-execution security.
*   **Level:** Strong Hire for Principal/Director Level Agentic Architecture.
