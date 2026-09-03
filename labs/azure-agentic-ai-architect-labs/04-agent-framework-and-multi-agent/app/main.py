from fastapi import FastAPI
app = FastAPI(title="Azure Agentic AI - 04-agent-framework-and-multi-agent")

@app.get("/health")
def health_check():
    return {"status": "healthy", "module": "04-agent-framework-and-multi-agent"}

@app.post("/invoke")
def invoke_agent():
    return {"message": "Agent logic implemented for 04-agent-framework-and-multi-agent"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
