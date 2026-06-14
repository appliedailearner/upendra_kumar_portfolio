# Azure OpenAI Foundations Reference Architecture

This reference architecture illustrates the hub-and-spoke networking pattern for secure enterprise deployment of Azure OpenAI.

## Architecture Diagram (Mermaid)

```mermaid
graph TD
    subgraph HubVNet [Hub VNet]
        FW[Azure Firewall]
        DNS[Private DNS Zones]
    end

    subgraph SpokeVNet [Spoke VNet - AI Workload]
        App[AI Application / Web App]
        PE[Private Endpoint: OpenAI]
    end

    User[User / Client] --> APIM[Azure API Management]
    APIM --> FW
    FW --> App
    App --> PE
    PE --> OpenAI[Azure OpenAI Service]
    
    DNS -.-> PE
```

## Key Considerations
- **Private Link**: All traffic to Azure OpenAI stays within the Microsoft backbone network.
- **Hub-Spoke Topology**: Centralizes security management (Firewall, DNS) in the hub.
- **Managed Identity**: Authenticates between App and OpenAI without secrets.
