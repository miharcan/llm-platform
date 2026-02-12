from fastapi import APIRouter
from pydantic import BaseModel
from app.rag.orchestrator import ingest_documents, retrieve
from app.retrieval.dense import ensure_collection


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
async def ingest_endpoint(request: IngestRequest):
    ensure_collection()
    ingest_documents(request.tenant_id, request.country, request.documents)
    return {"status": "ingested"}


from app.rag.generator import generate_answer

@router.post("/query")
async def query_endpoint(request: QueryRequest):
    ensure_collection()
    docs = retrieve(request.tenant_id, request.country, request.query)
    answer = generate_answer(request.query, docs)

    return {
        "tenant": request.tenant_id,
        "country": request.country,
        "answer": answer,
        "sources": docs,
    }
