import os
from app.agents.runners_autogen import run_autogen_task


def test_autogen_task_stub_or_fallback(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    result = run_autogen_task("Explain event-driven architecture", include_trace=True)
    assert result["meta"]["framework"] == "autogen"
    assert result["meta"]["mode"] in {"stub", "fallback"}
    assert "final_answer" in result
    if result["trace"]:
        assert isinstance(result["trace"], list)


def test_autogen_task_real_or_fallback(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-dummy")
    result = run_autogen_task("Outline benefits of modular code", include_trace=True)
    assert result["meta"]["framework"] == "autogen"
    # real mode may fail due to network limits; accept fallback
    assert result["meta"]["mode"] in {"real", "fallback"}
    assert "final_answer" in result
