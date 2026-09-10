import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}

def test_generate_missing_prompt(client):
    response = client.post("/api/generate", json={})
    assert response.status_code == 400
    assert "Prompt text is required" in response.json["message"]

def test_generate_success_mock(client):
    response = client.post("/api/generate", json={"prompt": "Test Prompt"})
    assert response.status_code == 200
    assert response.json["status"] == "success"

def test_prompt_too_long(client):
    response = client.post("/api/generate", json={"prompt": "x" * 3000})
    assert response.status_code == 400
    assert "too long" in response.json["message"].lower()

def test_history_endpoint_exists(client):
    response = client.get("/api/history")
    assert response.status_code == 200
    assert "history" in response.json

def test_stats_endpoint_exists(client):
    response = client.get("/api/stats")
    assert response.status_code == 200
    assert "total_requests" in response.json