import os
from app.agents.runners_smolagents import run_smolagents_task


def test_smolagents_task_stub_or_fallback(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    result = run_smolagents_task("Explain the purpose of modular design", include_trace=True)
    assert result["meta"]["framework"] == "smolagents"
    assert result["meta"]["mode"] in {"stub", "fallback"}
    assert "final_answer" in result
    if result["trace"]:
        assert isinstance(result["trace"], list)


def test_smolagents_task_real_or_fallback(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-dummy")
    result = run_smolagents_task("Summarize benefits of small focused agents", include_trace=True)
    assert result["meta"]["framework"] == "smolagents"
    assert result["meta"]["mode"] in {"real", "fallback"}
    assert "final_answer" in result
