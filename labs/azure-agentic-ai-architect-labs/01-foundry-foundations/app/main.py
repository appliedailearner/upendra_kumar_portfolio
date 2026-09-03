from fastapi import FastAPI
app = FastAPI(title="Azure Agentic AI - 01-foundry-foundations")

@app.get("/health")
def health_check():
    return {"status": "healthy", "module": "01-foundry-foundations"}

@app.post("/invoke")
def invoke_agent():
    return {"message": "Agent logic implemented for 01-foundry-foundations"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
