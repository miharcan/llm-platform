from qdrant_client.models import PointStruct
from app.retrieval.dense import client, COLLECTION_NAME
from app.embeddings.provider import embed_text
import uuid
from qdrant_client.models import Filter, FieldCondition, MatchValue

def ingest_documents(tenant_id: str, country: str, documents: list[str]):
    points = []

    for doc in documents:
        vector = embed_text(doc)
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "tenant_id": tenant_id,
                    "country": country,
                    "text": doc,
                },
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

def retrieve(tenant_id: str, country: str, query: str, top_k: int = 3):
    vector = embed_text(query)

    dense_results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=vector,
        limit=top_k,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="tenant_id",
                    match=MatchValue(value=tenant_id),
                ),
                FieldCondition(
                    key="country",
                    match=MatchValue(value=country),
                ),
            ]
        ),
    )

    dense_docs = [hit.payload["text"] for hit in dense_results.points]

    # Simple hybrid: merge unique
    return list(set(dense_docs))
