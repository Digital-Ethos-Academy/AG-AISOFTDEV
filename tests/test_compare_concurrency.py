from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_compare_agents_concurrency_meta():
    resp = client.post("/agents/demo/compare", json={"task": "List three benefits of modular design", "include_trace": False})
    assert resp.status_code == 200
    data = resp.json()
    assert "results" in data
    # Ensure all expected frameworks are present
    for fw in ["autogen", "crewai", "langchain", "smolagents"]:
        assert fw in data["results"], f"Missing framework {fw} in concurrent results"
    # Concurrency meta flag
    assert data.get("meta", {}).get("concurrency") is True
    assert data.get("meta", {}).get("framework_count") == 4
