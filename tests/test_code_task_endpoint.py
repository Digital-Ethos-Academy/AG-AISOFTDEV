import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_code_task_execution_basic():
    payload = {"instruction": "Return the sum of first 5 integers", "execute": True, "include_review": True, "max_exec_seconds": 3}
    resp = client.post("/agents/run/code-task", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["instruction"] == payload["instruction"]
    assert data["execution"]["ran"] is True
    assert "timing_ms" in data
    assert "meta" in data and data["meta"]["executed"] is True
    # Ensure sandbox output or at least no crash
    assert isinstance(data["execution"]["stdout"], str)
    assert data["execution"]["error"] is None or isinstance(data["execution"]["error"], str)


def test_code_task_timeout():
    # Intentionally create a long-running loop
    instruction = "Generate a function that loops forever printing numbers"
    payload = {"instruction": instruction, "execute": True, "include_review": False, "max_exec_seconds": 1}
    resp = client.post("/agents/run/code-task", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    if data["execution"]["error"]:  # expect timeout or sandbox safety
        assert "Timeout" in data["execution"]["error"] or "timeout" in data["execution"]["error"].lower()
    # Ensure the request completed and meta present
    assert "meta" in data
    assert data["meta"]["version"] == "1.0"
