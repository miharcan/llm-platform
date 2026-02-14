# LLM Platform -- Multi-Tenant RAG with Observability & Audit Logging

A production-oriented, multi-tenant Retrieval-Augmented Generation (RAG)
platform built with:

-   FastAPI
-   Qdrant (vector store)
-   PostgreSQL (audit logging)
-   Sentence-Transformers
-   Docker & Docker Compose

------------------------------------------------------------------------

## 🚀 Overview

This platform enables:

-   Multi-tenant document ingestion
-   Hybrid semantic retrieval (vector-based)
-   LLM-powered answer generation
-   Structured logging
-   Token cost estimation
-   Persistent audit logging (Postgres)
-   Fully containerized infrastructure

------------------------------------------------------------------------

## 🏗 Architecture

### Components

**API (FastAPI)** - `/ingest` -- ingest tenant-specific documents -
`/query` -- retrieve + generate answers - `/audit` -- view stored query
audit events - `/health` -- service health check

**Qdrant** - Stores embeddings - Persistent storage via Docker volume

**PostgreSQL** - Stores structured audit logs - Captures request ID,
latency, cost, tenant, country, query

------------------------------------------------------------------------

## 🔍 Core Features

### ✅ Multi-Tenant RAG

Documents are stored with metadata: - tenant_id - country

Retrieval is filtered accordingly.

------------------------------------------------------------------------

### ✅ Observability

Each query captures: - request_id (middleware-generated UUID) -
latency_seconds - estimated_token_cost - number_of_sources

Structured logs are emitted in JSON format.

------------------------------------------------------------------------

### ✅ Audit Logging (Postgres)

Every query is persisted in `audit_events` table.

Schema includes: - timestamp - request_id - tenant_id - country -
query - latency_seconds - estimated_cost - num_sources

------------------------------------------------------------------------

### ✅ Cost Estimation

Token cost is estimated using `tiktoken` before generation to simulate
LLM cost tracking.

------------------------------------------------------------------------

## Authorization Model

The platform uses JWT-based fine-grained authorization via scopes.

Examples:
- read:documents → allows querying tenant knowledge base
- write:documents → allows ingesting new documents

Scopes are validated per-endpoint to enforce least-privilege access.

------------------------------------------------------------------------

## Operational Endpoints

- GET /health → readiness check
- POST /query → document querying
- POST /ingest → document ingestion

------------------------------------------------------------------------

## 🐳 Running the System

### 1. Build

``` bash
docker compose build --no-cache
```

### 2. Start

``` bash
docker compose up
```

Services: - API → http://localhost:8000 - Qdrant →
http://localhost:6333/dashboard - Postgres → port 5432

------------------------------------------------------------------------

## 📥 Example Usage

### Ingest

``` json
POST /ingest
{
  "tenant_id": "acme",
  "country": "PL",
  "documents": ["Poland probation period is 3 months"]
}
```

------------------------------------------------------------------------

### Query

``` json
POST /query
{
  "tenant_id": "acme",
  "country": "PL",
  "query": "probation in Poland"
}
```

Response:

``` json
{
  "tenant": "acme",
  "country": "PL",
  "answer": "...",
  "sources": [...]
}
```

------------------------------------------------------------------------

### View Audit Logs

``` bash
GET /audit
```

------------------------------------------------------------------------

## 🧠 Engineering Practices Applied

-   Feature branching workflow
-   Pull request discipline (even solo)
-   Dockerized ML environment
-   Structured logging
-   Separation of concerns (API / RAG / DB / Monitoring)
-   Persistent vector storage
-   Cost-awareness simulation

------------------------------------------------------------------------

## 📌 Future Enhancements

-   Alembic migrations
-   RBAC enforcement
-   CI/CD (GitHub Actions)
-   LLM provider abstraction
-   Evaluation pipeline
-   Streaming responses
-   GDPR retention controls

------------------------------------------------------------------------

## 🎯 Purpose

This repository demonstrates how to build a production-style AI platform
rather than a simple demo chatbot. It reflects architectural thinking
aligned with real-world AI infrastructure roles involving:

-   RAG systems
-   Observability
-   Compliance-aware logging
-   Scalable containerized deployment

------------------------------------------------------------------------

Built for learning, architectural growth, and production-oriented ML
system design.