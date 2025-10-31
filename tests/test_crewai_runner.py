from app.agents.runners_crewai import run_crewai_task, run_crewai_plan


def test_crewai_task_stub_or_real():
    result = run_crewai_task("Analyze modular architecture", include_trace=True)
    assert result["meta"]["framework"] == "crewai"
    assert result["meta"]["mode"] in {"stub", "real", "fallback"}
    assert "final_answer" in result
    if result["trace"]:
        assert isinstance(result["trace"], list)


def test_crewai_plan_structure():
    plan = run_crewai_plan("Build event-driven ingestion pipeline", depth_level=2, include_risks=True)
    assert len(plan["phases"]) == 2
    assert plan["agents_used"] == ["crewai"]
    if plan.get("risks"):
        assert isinstance(plan["risks"], list)
