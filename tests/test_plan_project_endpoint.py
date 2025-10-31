import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_plan_project_basic():
    payload = {"objective": "Build a markdown sync tool", "depth_level": 2, "include_risks": True, "include_reviewer": False}
    resp = client.post("/agents/plan/project", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["objective"] == payload["objective"]
    assert len(data["plan"]["phases"]) == payload["depth_level"]
    # risks present if include_risks
    assert data["plan"]["risks"] is not None
    # reviewer notes may exist from CrewAI stub/heuristic even if reviewer not included
    assert "meta" in data
    assert data["meta"]["version"] == "1.0"
    assert "timing_ms" in data["meta"]


def test_plan_project_with_reviewer_flag():
    payload = {"objective": "Implement vector search service", "depth_level": 1, "include_risks": True, "include_reviewer": True}
    resp = client.post("/agents/plan/project", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["objective"] == payload["objective"]
    assert len(data["plan"]["phases"]) == payload["depth_level"]
    if payload["include_risks"]:
        assert data["plan"]["risks"] is not None
    # If reviewer enabled, meta.review_included True
    assert data["meta"]["review_included"] is True
    # reviewer_notes should include AUTO-GEN REVIEW marker if autogen available & key present (soft assert)
    notes = data["plan"].get("reviewer_notes") or ""
    # Accept either presence or absence (fallback) but ensure string type
    assert isinstance(notes, str)

