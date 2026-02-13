from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from app.embeddings.provider import embed_text

client = QdrantClient(host="qdrant", port=6333)

COLLECTION_NAME = "documents"

def ensure_collection():
    vector = embed_text("test")
    vector_size = len(vector)

    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )