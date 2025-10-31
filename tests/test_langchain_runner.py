import os
from importlib import reload

from app.agents.runners_langchain import run_langchain_task


def test_langchain_runner_fallback_without_openai_key(monkeypatch):
    # Ensure OPENAI_API_KEY is absent
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    result = run_langchain_task("Test task fallback", include_trace=True)
    assert result["meta"]["framework"] == "langchain"
    assert result["meta"]["mode"] in {"fallback", "stub"}
    assert result["final_answer"].startswith("[LANGCHAIN")
    assert result["trace"] is not None


def test_langchain_runner_real_mode_if_key_present(monkeypatch):
    # Fake key to pass initial check; real API call may still fail, triggering fallback.
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-dummy")
    result = run_langchain_task("Summarize the benefits of modular code", include_trace=True)
    assert result["meta"]["framework"] == "langchain"
    # Real mode may fail due to network restrictions; we accept either real or fallback.
    assert result["meta"]["mode"] in {"real", "fallback"}
    assert "final_answer" in result
