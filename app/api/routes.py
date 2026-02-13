from fastapi import HTTPException
from fastapi import APIRouter, Request
from pydantic import BaseModel
from app.rag.orchestrator import ingest_documents, retrieve
from app.retrieval.dense import ensure_collection
from app.rag.generator import generate_answer
from time import time
from app.monitoring.logger import logger
from app.monitoring.audit import record_query_event
from app.cost.tracker import estimate_token_cost
from app.monitoring.audit import audit_log
from fastapi import Depends
from app.security.dependencies import get_current_user


router = APIRouter()


class QueryRequest(BaseModel):
    tenant_id: str
    country: str
    query: str


@router.get("/")
def root():
    return {"message": "LLM Platform API running"}


class IngestRequest(BaseModel):
    tenant_id: str
    country: str
    documents: list[str]


@router.post("/ingest")
async def ingest_endpoint(request: IngestRequest,
                          user=Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Insufficient permissions",
        )
    ensure_collection()
    ingest_documents(request.tenant_id, request.country, request.documents)
    return {"status": "ingested"}


@router.post("/query")
async def query_endpoint(request: QueryRequest, req: Request,
                         user=Depends(get_current_user)):
    if user.get("tenant_id") != request.tenant_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: tenant mismatch",
        )

    ensure_collection()

    estimated_cost = estimate_token_cost(request.query)

    start_time = time()

    docs = retrieve(request.tenant_id, request.country, request.query)
    answer = generate_answer(request.query, [d["text"] for d in docs])

    latency = time() - start_time

    event_data = {
        "request_id": req.state.request_id,
        "tenant_id": request.tenant_id,
        "country": request.country,
        "query": request.query,
        "latency_seconds": latency,
        "estimated_cost": estimated_cost,
        "num_sources": len(docs),
    }

    logger.info(
        "query_executed",
        extra={"extra_data": event_data}
    )

    record_query_event(event_data)

    return {
        "tenant": request.tenant_id,
        "country": request.country,
        "answer": answer,
        "sources": docs,
    }


@router.get("/audit")
def get_audit():
    return audit_log
