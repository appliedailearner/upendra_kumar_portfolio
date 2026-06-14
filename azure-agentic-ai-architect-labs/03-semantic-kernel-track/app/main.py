import logging
from fastapi import FastAPI
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

app = FastAPI(title="Azure Agentic AI - Semantic Kernel Track")
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("Initializing Semantic Kernel instance...")
    # This demonstrates the initialization of SK with Azure OpenAI
    # In a full flow, kernel.add_plugin() would be called here.
    global kernel
    kernel = Kernel()

@app.get("/health")
def health_check():
    return {
        "status": "healthy", 
        "module": "03-semantic-kernel-track",
        "description": "Demonstrates Semantic Kernel integration with Azure OpenAI."
    }

@app.post("/invoke")
async def invoke_agent(prompt: str = "Hello, SK!"):
    """Mock execution of a Semantic Kernel prompt."""
    return {
        "framework": "Semantic Kernel",
        "mock_response": f"Semantic Kernel received: {prompt}",
        "status": "Complete"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
