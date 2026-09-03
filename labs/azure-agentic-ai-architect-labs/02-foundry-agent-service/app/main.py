from fastapi import FastAPI
app = FastAPI(title="Azure Agentic AI - 02-foundry-agent-service")

@app.get("/health")
def health_check():
    return {"status": "healthy", "module": "02-foundry-agent-service"}

@app.post("/invoke")
def invoke_agent():
    return {"message": "Agent logic implemented for 02-foundry-agent-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
