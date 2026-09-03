# Agent Enterprise Integration

This architecture demonstrates how to integrate AI agents into enterprise systems using Azure API Management, Managed Identities, and private networking.

## Architecture Diagram (Mermaid)

```mermaid
graph LR
    User[User/Client] --> APIM[Azure API Management]
    APIM --> App[Azure Container Apps / Functions]
    App --> Kernel[Semantic Kernel / Agent Framework]
    Kernel --> Search[Azure AI Search]
    Kernel --> SQL[Azure SQL / Cosmos DB]
    Kernel --> OpenAI[Azure OpenAI]
    SQL -.-> ManagedID[Managed Identity]
    OpenAI -.-> ManagedID
    Search -.-> ManagedID
```

## Key Components
- **Azure API Management**: Governs and secures agent endpoints.
- **Managed Identities**: Eliminates the need for API keys in code.
- **Private Link**: Ensures data never traverses the public internet.
