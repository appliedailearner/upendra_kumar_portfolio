"""FastAPI Application for Azure Agentic AI.

Main application entry point with REST API endpoints for agent interaction.
Refactored for L67 Architect Standards: Multi-Agent Coordinator/Worker pattern using Azure AI Projects SDK.
"""

import os
import logging
from contextlib import asynccontextmanager
from typing import Dict, Any, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from azure.identity.aio import DefaultAzureCredential
from azure.ai.projects.aio import AIProjectClient
from azure.ai.projects.models import MessageRole, RunStatus, AsyncAgentEventHandler

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# ==========================================
# Configuration Models
# ==========================================

class AgentRequest(BaseModel):
    """Request model for agent execution."""
    prompt: str
    target_agent: str = "coordinator" # 'coordinator' or 'worker'

class AgentResponse(BaseModel):
    """Response model from agent."""
    status: str
    response: str
    agent_id: str
    thread_id: str

class ErrorResponse(BaseModel):
    """Sanitized Error Response for external consumption."""
    error_code: str
    message: str

# ==========================================
# Agent Orchestration State
# ==========================================
class AgentState:
    project_client: AIProjectClient = None
    coordinator_agent: Any = None
    worker_agent: Any = None
    credential: DefaultAzureCredential = None

state = AgentState()

# ==========================================
# Lifespan & Initialization
# ==========================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: Initialize the AI Project Client and Agents."""
    logger.info("Starting Azure Agentic AI Service (Foundry SDK Edition)...")
    
    project_connection_string = os.environ.get("PROJECT_CONNECTION_STRING")
    if not project_connection_string:
        logger.warning("PROJECT_CONNECTION_STRING not set. Agents will not be initialized on startup.")
    else:
        try:
            state.credential = DefaultAzureCredential()
            state.project_client = AIProjectClient.from_connection_string(
                credential=state.credential,
                conn_str=project_connection_string
            )
            
            # 1. Initialize Coordinator Agent
            state.coordinator_agent = await state.project_client.agents.create_agent(
                model=os.environ.get("COORDINATOR_MODEL_DEPLOYMENT", "gpt-4o"),
                name="coordinator-agent",
                instructions="You are the Lead Coordinator Agent. Evaluate tasks. If a task requires data computation, processing, or data lookup, delegate it to the worker."
            )
            logger.info(f"Coordinator Agent Created: {state.coordinator_agent.id}")

            # 2. Initialize Worker Agent
            state.worker_agent = await state.project_client.agents.create_agent(
                model=os.environ.get("WORKER_MODEL_DEPLOYMENT", "gpt-4o-mini"),
                name="worker-agent",
                instructions="You are a specialist Worker Agent. Execute specific data processing tasks precisely and concisely."
            )
            logger.info(f"Worker Agent Created: {state.worker_agent.id}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Azure AI Project Client: {e}")
            
    yield
    
    # Teardown
    logger.info("Shutting down Agentic AI Service...")
    if state.project_client:
        if state.coordinator_agent:
            await state.project_client.agents.delete_agent(state.coordinator_agent.id)
        if state.worker_agent:
            await state.project_client.agents.delete_agent(state.worker_agent.id)
        await state.project_client.close()
    if state.credential:
        await state.credential.close()

# ==========================================
# App Definition & Middleware
# ==========================================

app = FastAPI(
    title="Azure Agentic AI Service",
    description="Multi-Agent Azure AI Foundry Reference Implementation (L67 Standard)",
    version="2.0.0",
    lifespan=lifespan,
    responses={500: {"model": ErrorResponse}} # Force sanitized error schema
)

# [CIO REMEDIATION]: Strict CORS Policy
# Do NOT use allow_origins=["*"] in production.
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8080").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

# ==========================================
# Endpoints
# ==========================================

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "foundry_connected": str(state.project_client is not None)
    }

@app.post("/agents/invoke", response_model=AgentResponse)
async def invoke_agent(request: AgentRequest) -> AgentResponse:
    """Invoke an agent (Coordinator or Worker) on a new thread."""
    if not state.project_client:
        return ErrorResponse(error_code="SVC_001", message="Azure AI Project Client not initialized.")
        
    try:
        # Determine target agent
        target_agent = state.coordinator_agent if request.target_agent.lower() == "coordinator" else state.worker_agent
        if not target_agent:
             raise ValueError("Requested agent is not available.")

        # Create a new thread
        thread = await state.project_client.agents.create_thread()
        
        # Add user message to thread
        await state.project_client.agents.create_message(
            thread_id=thread.id,
            role=MessageRole.USER,
            content=request.prompt
        )
        
        # Run the agent
        # Note: In a real L67 production scenario, we'd use event streams and tool handlers here
        run = await state.project_client.agents.create_and_poll_run(
            thread_id=thread.id,
            assistant_id=target_agent.id
        )
        
        if run.status == RunStatus.COMPLETED:
            # Fetch messages
            messages = await state.project_client.agents.list_messages(thread_id=thread.id)
            # The most recent message from the assistant is idx 0
            latest_msg = messages.data[0]
            
            return AgentResponse(
                status="success",
                response=latest_msg.content[0].text.value if latest_msg.content else "No response generated.",
                agent_id=target_agent.id,
                thread_id=thread.id
            )
        else:
            return AgentResponse(
                 status="failed",
                 response=f"Run ended with status: {run.status}",
                 agent_id=target_agent.id,
                 thread_id=thread.id
            )

    except Exception as e:
        # [CIO REMEDIATION]: Sanitized Error handling (no stack traces)
        logger.error(f"Internal Orchestration Error: {e}")
        return ErrorResponse(error_code="SVC_500", message="An internal orchestration error occurred.")

@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint."""
    return {
        "message": "Welcome to Azure Agentic AI (Multi-Agent Edition)",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run("app.agent-service:app", host="0.0.0.0", port=port, reload=False)
