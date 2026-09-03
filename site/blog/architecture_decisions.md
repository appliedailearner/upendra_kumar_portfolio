# Architectural Decisions: App Gateway & Redis

## 1. Why App Gateway in Prod/Non-Prod Subscriptions?
**Verdict: Essential.**

*   **Role:** It acts as the **Ingress Controller (AGIC)** for your AKS clusters.
*   **Why not just Front Door?**
    *   Front Door is Global (Layer 7). It gets traffic *to* the region.
    *   App Gateway is Regional (Layer 7). It lives *inside* your VNet.
    *   **The Critical Gap:** You need something to talk "Kubernetes" (Ingress resources) to route traffic to specific pods/services. App Gateway does this natively via AGIC.
    *   **Security:** It provides the last-mile WAF protection specific to the application limitations.

## 2. Should we use App Gateway in Shared (Hub)?
**Verdict: No.** (In this specific Dual-APIM design).

*   **Reasoning:**
    *   Your **External APIM** is already in the Hub. It acts as the robust API Gateway for external consumers.
    *   Adding App Gateway *in front* of APIM in the Hub is often redundant if you are already using **Front Door Premium** (which has WAF).
    *   **Flow:** Internet -> Front Door (WAF) -> External APIM (Hub) -> Private Link -> App Gateway/AKS (Spoke).
    *   *Exception:* If you were NOT using Front Door, you would need App Gateway in the Hub to act as the regional WAF for APIM. But you are using Front Door.

## 3. Should we use Redis Cache?
**Verdict: YES, Critical for AI.**

*   **Use Case 1: Semantic Caching (internal APIM)**
    *   Enabling "Semantic Caching" in APIM requires an external Redis Cache.
    *   **Benefit:** If User A asks "What is the policy?" and User B asks the same 1 minute later, the AI model is **never touched**. Redis serves the answer.
    *   **Impact:** Saves **PTU capacity**, reduces latency by 90%, and saves money.
*   **Use Case 2: Application State**
    *   Your AKS microservices need a place to store session data/fast-access data off the cluster.

### Recommendation for Diagram
I will update the **Architecture Diagram (v3)** to explicitly show **Azure Redis Cache** connected to the **Internal APIM** to visualize this critical "Token Saving" pattern.
