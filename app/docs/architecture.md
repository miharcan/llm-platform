# Platform Architecture

## Authentication
- Stateless JWT authentication (HTTPBearer)
- Token expiration enforced
- Explicit 401 / 403 separation

## Multi-Tenant Isolation
- Tenant ID embedded in JWT
- Request tenant validated against token
- Prevents cross-tenant data access

## Role-Based Access Control
- Role claim in JWT
- Endpoint-level role enforcement

## RAG Pipeline
Client
→ JWT Authentication
→ Tenant Validation
→ Role Enforcement
→ Retrieval (Qdrant)
→ Generation
→ Audit Logging (Postgres)

## Observability
- Request ID tracing
- Structured logging
- Cost estimation tracking
- Latency tracking
