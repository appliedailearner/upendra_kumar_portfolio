from fastapi import FastAPI
app = FastAPI(title="Azure Agentic AI - 07-secure-reference-architecture")

@app.get("/health")
def health_check():
    return {"status": "healthy", "module": "07-secure-reference-architecture"}

@app.post("/invoke")
def invoke_agent():
    return {"message": "Agent logic implemented for 07-secure-reference-architecture"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
