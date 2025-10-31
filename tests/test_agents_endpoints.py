import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_compare_agents_stub():
    payload = {"task": "Explain quantum computing simply", "include_trace": True}
    resp = client.post("/agents/demo/compare", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["task"] == payload["task"]
    # Check presence of frameworks
    for fw in ["autogen", "crewai", "langchain", "smolagents"]:
        assert fw in data["results"], f"Missing {fw} in results"
        assert "final_answer" in data["results"][fw]


def test_plan_project_stub():
    payload = {"objective": "Build a markdown sync tool", "depth_level": 2, "include_risks": True}
    resp = client.post("/agents/plan/project", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["objective"] == payload["objective"]
    assert len(data["plan"]["phases"]) == payload["depth_level"]
    if payload["include_risks"]:
        assert data["plan"]["risks"] is not None


def test_run_code_task_stub():
    payload = {"instruction": "Return hello", "execute": True, "include_review": True, "max_exec_seconds": 5}
    resp = client.post("/agents/run/code-task", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["instruction"] == payload["instruction"]
    assert data["execution"]["ran"] is True
    assert "code" in data
    assert data["framework"] == "autogen"
