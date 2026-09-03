# Secure AI Gateway Reference Architecture

This architecture demonstrates how to implement a secure, governed gateway for Azure OpenAI services using Azure API Management (APIM).

## Architecture Diagram (Mermaid)

```mermaid
graph TD
    UserApp[User Application] --> APIM[Azure API Management]
    
    subgraph "AI Security & Governance"
        APIM --> Policy[Token Limit / Rate Limiting]
        APIM --> Auth[Entra ID / Managed Identity]
        APIM --> ContentSafety[Azure AI Content Safety]
    end
    
    subgraph "Load Balancing & Failover"
        APIM --> AOAI_Hub[Azure OpenAI Hub Load Balancer]
        AOAI_Hub --> Region1[AOAI Region 1]
        AOAI_Hub --> Region2[AOAI Region 2]
    end
    
    APIM --> Logs[Azure Monitor / App Insights]
```

## Key Components

1.  **Azure API Management**: Acts as the single entry point for all AI requests, enforcing policies.
2.  **Azure AI Content Safety**: Detects and blocks harmful content in prompts and completions.
3.  **Managed Identity**: Ensures secure, passwordless authentication to Azure OpenAI.
4.  **Token-based Throttling**: Limits usage based on TPM (Tokens Per Minute) to prevent cost overruns.

## Implementation References

- [Azure API Management AI Gateway](https://learn.microsoft.com/en-us/azure/api-management/gen-ai-gateway-overview)
- [Secure Azure OpenAI](https://learn.microsoft.com/en-us/azure/architecture/guide/ai/openai-security)
