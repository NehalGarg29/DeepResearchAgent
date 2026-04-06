import httpx
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.agent.research_agent import research_agent
from loguru import logger

router = APIRouter()

class ResearchRequest(BaseModel):
    query: str

class ResearchResponse(BaseModel):
    query: str
    sub_queries: List[str]
    answer: str
    evaluation: Dict[str, Any]
    usage_status: Dict[str, Any]

class WorkflowTriggerRequest(BaseModel):
    query: str
    webhook_url: str

@router.post("/research", response_model=ResearchResponse)
async def perform_research(request: ResearchRequest):
    try:
        result = await research_agent.perform_research(request.query)
        return ResearchResponse(**result)
    except Exception as e:
        logger.error(f"Error in research API: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/workflows/trigger")
async def trigger_workflow(request: WorkflowTriggerRequest, background_tasks: BackgroundTasks):
    """Trigger an external workflow (e.g., n8n) and return immediately."""
    async def _call_webhook(url: str, data: dict):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=data)
                logger.info(f"Workflow triggered: {response.status_code}")
        except Exception as e:
            logger.error(f"Failed to trigger workflow: {str(e)}")

    background_tasks.add_task(_call_webhook, request.webhook_url, {"query": request.query})
    return {"status": "Workflow trigger initiated", "webhook_url": request.webhook_url}

@router.get("/health")
async def health():
    return {"status": "ok"}
