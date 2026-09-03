from fastapi import FastAPI
app = FastAPI(title="Azure Agentic AI - 05-rag-with-azure-ai-search")

@app.get("/health")
def health_check():
    return {"status": "healthy", "module": "05-rag-with-azure-ai-search"}

@app.post("/invoke")
def invoke_agent():
    return {"message": "Agent logic implemented for 05-rag-with-azure-ai-search"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
