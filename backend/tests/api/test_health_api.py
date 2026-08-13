from fastapi.testclient import TestClient

from qwos.main import app

client = TestClient(app)


def test_health_endpoint_returns_healthy() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
    }