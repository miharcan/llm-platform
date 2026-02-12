# LLM Platform Blueprint

A production-oriented, multi-tenant Retrieval-Augmented Generation (RAG)
platform built with FastAPI and Qdrant.

------------------------------------------------------------------------

## Overview

This project demonstrates a scalable, compliance-aware LLM
infrastructure foundation designed for multi-tenant environments.

It includes:

-   Dockerized FastAPI service
-   Qdrant vector database with persistent storage
-   Tenant and country-level metadata filtering
-   Vector-based retrieval layer
-   Generation abstraction layer
-   Clean modular architecture
-   Container networking and volume persistence

------------------------------------------------------------------------

## Architecture

    Client
      ↓
    FastAPI Gateway
      ↓
    RAG Orchestrator
      ├── Dense Retrieval (Qdrant)
      ├── Metadata Filtering (tenant + country)
      ├── Generator Layer
      ↓
    Persistent Vector Storage (Docker Volume)

------------------------------------------------------------------------

## Key Features

### Multi-Tenant Isolation

Each document is stored with: - `tenant_id` - `country`

All queries enforce strict metadata filtering to prevent cross-tenant
data leakage.

### Persistent Storage

Qdrant runs with a Docker volume:

    volumes:
      - qdrant_data:/qdrant/storage

Vector data survives container restarts.

### Modular Design

    app/
      api/
      rag/
      retrieval/
      embeddings/
      cost/
      monitoring/

Clear separation between ingestion, retrieval, and generation.

------------------------------------------------------------------------

## Running the Project

### 1. Start Services

    docker compose up --build

### 2. Open Swagger

    http://localhost:8000/docs

### 3. Ingest Example

``` json
{
  "tenant_id": "acme",
  "country": "PL",
  "documents": [
    "Poland probation period is 3 months"
  ]
}
```

### 4. Query Example

``` json
{
  "tenant_id": "acme",
  "country": "PL",
  "query": "probation"
}
```

Expected response:

``` json
{
  "tenant": "acme",
  "country": "PL",
  "answer": "Based on retrieved documents: Poland probation period is 3 months",
  "sources": [
    "Poland probation period is 3 months"
  ]
}
```

------------------------------------------------------------------------

## Production Considerations

-   Replace stub embeddings with sentence-transformers or OpenAI
    embeddings
-   Add structured logging and request IDs
-   Add cost tracking per tenant
-   Add evaluation pipeline for retrieval accuracy
-   Implement RBAC and authentication middleware
-   Add observability (Prometheus / tracing)

------------------------------------------------------------------------

## Roadmap

-   Hybrid retrieval (BM25 + dense)
-   Re-ranking layer
-   Streaming responses
-   Audit logging
-   LLM-based evaluation endpoint

------------------------------------------------------------------------

## License

MIT