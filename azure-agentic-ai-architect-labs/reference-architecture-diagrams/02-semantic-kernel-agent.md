# Semantic Kernel Agent Reference Architecture

This reference architecture illustrates how to build intelligent agents using Semantic Kernel on Azure, leveraging planners, plugins, and memory.

## Architecture Diagram (Mermaid)

```mermaid
graph TD
    UserApp[User Application] --> SK[Semantic Kernel SDK]
    
    subgraph "Semantic Kernel Core"
        SK --> Plugins[Plugins / Functions]
        SK --> Planner[Planner / Orchestrator]
        SK --> Memory[Semantic Memory / Vector Store]
    end
    
    subgraph "Azure Services"
        SK --> AOAI[Azure OpenAI Service]
        Planner --> AOAI
        Memory --> AISEARCH[Azure AI Search]
    end
    
    Plugins --> ExternalAPI[External Data/APIs]
    UserApp --> Telemetry[Azure Monitor / App Insights]
```

## Key Components

1.  **Semantic Kernel SDK**: The orchestration engine.
2.  **Plugins/Skills**: Encapsulated logic for specific tasks.
3.  **Planners**: Automatically create a plan to achieve user goals.
4.  **Vector Store**: Provides long-term memory for the agent.

## Implementation References

- [Semantic Kernel Documentation](https://learn.microsoft.com/en-us/semantic-kernel/)
- [Agentic AI Design Patterns](https://azure.microsoft.com/en-us/solutions/ai/)
