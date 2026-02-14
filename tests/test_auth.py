from fastapi.testclient import TestClient
from app.main import app
from jose import jwt
from datetime import datetime, timedelta
from unittest.mock import patch

client = TestClient(app)

SECRET_KEY = "dev-secret"
ALGORITHM = "HS256"


def generate_token(tenant="acme", scopes=None):
    payload = {
        "sub": "user1",
        "tenant_id": tenant,
        "scopes": scopes or ["read:documents"],
        "exp": datetime.utcnow() + timedelta(hours=1),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def test_query_without_token_returns_401():
    response = client.post("/query", json={
        "tenant_id": "acme",
        "country": "PL",
        "query": "probation"
    })
    assert response.status_code == 403 or response.status_code == 401


def test_query_with_mismatched_tenant_returns_403():
    token = generate_token(tenant="acme")

    response = client.post(
        "/query",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "tenant_id": "other",
            "country": "PL",
            "query": "probation"
        }
    )

    assert response.status_code == 403


@patch("app.api.routes.ensure_collection")
@patch("app.api.routes.retrieve")
@patch("app.api.routes.generate_answer")
def test_query_with_valid_token_returns_200(
    mock_generate,
    mock_retrieve,
    mock_ensure,
):
    mock_retrieve.return_value = [{"text": "test", "score": 0.9}]
    mock_generate.return_value = "test answer"

    token = generate_token(tenant="acme")

    response = client.post(
        "/query",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "tenant_id": "acme",
            "country": "PL",
            "query": "probation"
        }
    )

    assert response.status_code == 200