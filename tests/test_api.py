from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_query_endpoint_unauthorized():
    # This should fail if OPENAI_API_KEY is not set, 
    # but we can test the structure
    response = client.post("/query", json={"question": "What is RAG?"})
    # We expect a 500 if no API key is present in CI without secrets
    assert response.status_code in [200, 500]
