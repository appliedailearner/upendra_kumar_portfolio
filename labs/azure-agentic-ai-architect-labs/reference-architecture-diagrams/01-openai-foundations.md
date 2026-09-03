# Azure OpenAI Foundations Reference Architecture

This reference architecture illustrates the Enterprise Hub pattern for Azure OpenAI, focusing on central governance, security, and scalability.

## Architecture Diagram (Mermaid)

```mermaid
graph TD
    User([User/App]) --> Gateway[Azure API Management / App Gateway]
    Gateway --> HubVNet[Hub VNet]
    
    subgraph HubVNet
        Firewall[Azure Firewall]
        PrivateDNS[Private DNS Zones]
    end
    
    Gateway --> SpokeVNet[Spoke VNet - AI Workload]
    
    subgraph SpokeVNet
        AppService[App Service / AKS]
        PE_AOAI[Private Endpoint: OpenAI]
        PE_KV[Private Endpoint: Key Vault]
    end
    
    AppService --> PE_AOAI
    AppService --> PE_KV
    
    subgraph AI_Services[Azure AI Services]
        AOAI[Azure OpenAI Service]
    end
    
    PE_AOAI -.-> AOAI
```

## Key Components
- **Azure API Management**: Provides throttling, caching, and token management.
- **Private Link / Endpoints**: Ensures all traffic stays within the Azure backbone.
- **Hub-Spoke Topology**: Separates shared network services from AI workloads.

## Reference Links
- [Azure OpenAI Landing Zone Accelerator](https://github.com/Azure/azure-openai-landing-zone)
- [Baseline OpenAI Architecture](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/architecture/baseline-openai)
