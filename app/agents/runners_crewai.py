"""CrewAI runner (incremental real integration).

Current behavior: attempts to instantiate simple CrewAI agents & tasks if the
`crewai` package is available; otherwise returns stub data. This is an
intermediate step toward full hierarchical planning.

Fallback conditions:
    - ImportError for crewai
    - Runtime exceptions during crew execution

Future enhancements:
    - Rich role definitions with tools
    - Dynamic depth expansion based on `depth_level`
    - Optional post-processing review agent
    - Concurrency & streaming of intermediate results
"""
from __future__ import annotations
import time
from typing import List, Dict, Any


def _run_real_crewai_task(task: str, include_trace: bool) -> Dict[str, Any]:
    """Attempt a minimal CrewAI execution for a single summarization task."""
    from crewai import Agent, Task, Crew  # type: ignore

    start = time.time()
    trace: List[str] = []
    try:
        # Early key presence check to avoid underlying model client indefinite wait
        import os
        if not os.getenv("OPENAI_API_KEY"):
            return {
                "final_answer": f"[CREWAI FALLBACK] Missing OPENAI_API_KEY; stub for: {task}"[:400],
                "trace": ["error: missing OPENAI_API_KEY"] if include_trace else None,
                "meta": {"duration_ms": 0, "framework": "crewai", "mode": "fallback"},
                "error": "missing_openai_key",
            }
        researcher = Agent(
            role="Researcher",
            goal="Gather concise relevant points",
            backstory="Expert at extracting key facts quickly",
            allow_delegation=False,
            verbose=False,
        )
        synthesizer = Agent(
            role="Synthesizer",
            goal="Compose clear bullet summary",
            backstory="Transforms raw notes into structured insights",
            allow_delegation=False,
            verbose=False,
        )

        research_task = Task(description=f"Research context for: {task}", agent=researcher)
        synth_task = Task(description="Summarize research notes into <=5 bullets", agent=synthesizer)

        crew = Crew(agents=[researcher, synthesizer], tasks=[research_task, synth_task])
        result = crew.run()
        duration_ms = int((time.time() - start) * 1000)
        if include_trace:
            trace = ["agent:Researcher completed research", "agent:Synthesizer produced summary"]
        return {
            "final_answer": str(result)[:1200],
            "trace": trace if include_trace else None,
            "meta": {"duration_ms": duration_ms, "framework": "crewai", "mode": "real"},
            "error": None,
        }
    except Exception as e:
        duration_ms = int((time.time() - start) * 1000)
        return {
            "final_answer": f"[CREWAI FALLBACK] Exception; stub result for: {task}"[:400],
            "trace": [f"error:{e}"] if include_trace else None,
            "meta": {"duration_ms": duration_ms, "framework": "crewai", "mode": "fallback"},
            "error": str(e),
        }


def run_crewai_task(task: str, include_trace: bool = True) -> Dict[str, Any]:
    start = time.time()
    try:
        import crewai  # noqa: F401
    except Exception:
        # Stub fallback
        final_answer = f"[CREWAI STUB] Synthesized outcome for: {task}"[:400]
        trace = [
            "role: Researcher -> produced initial notes",
            "role: Synthesizer -> merged notes",
        ] if include_trace else None
        duration_ms = int((time.time() - start) * 1000)
        return {
            "final_answer": final_answer,
            "trace": trace,
            "meta": {"duration_ms": duration_ms, "framework": "crewai", "mode": "stub"},
            "error": None,
        }
    return _run_real_crewai_task(task, include_trace)


def run_crewai_plan(objective: str, depth_level: int = 2, include_risks: bool = True) -> Dict[str, Any]:
    """Generate a phased project plan.

    Behavior tiers:
        - If crewai not installed: return deterministic stub structure.
        - If installed: instantiate lightweight role agents (Architect, Researcher, ProjectManager)
          and use heuristic composition (still not invoking complex agent loops to keep tests fast).
    """
    start = time.time()
    try:
        from crewai import Agent  # type: ignore
    except Exception:
        phases = []
        for i in range(depth_level):
            phases.append({
                "name": f"Phase {i+1}: Stub Planning Layer",
                "tasks": [
                    f"Draft scope segment {i+1}",
                    f"Identify key components {i+1}",
                    f"List acceptance criteria {i+1}",
                ],
                "deliverables": [f"Stub spec section {i+1}", f"Stub checklist {i+1}"],
            })
        risks = [{"risk": "Scope creep", "mitigation": "Strict acceptance criteria"}] if include_risks else None
        duration_ms = int((time.time() - start) * 1000)
        return {
            "phases": phases,
            "risks": risks,
            "assumptions": ["Stub assumes basic environment setup"],
            "reviewer_notes": "Stubbed plan - real agent review pending",
            "timing_ms": duration_ms,
            "agents_used": ["crewai"],
        }

    # Real (heuristic) role setup - no crew execution to keep deterministic
    architect = Agent(
        role="Architect",
        goal="Break objective into technical phases",
        backstory="Seasoned software architect focusing on modularity",
        allow_delegation=False,
        verbose=False,
    )
    researcher = Agent(
        role="Researcher",
        goal="Add technology choices & references",
        backstory="Finds relevant libs and cloud services",
        allow_delegation=False,
        verbose=False,
    )
    manager = Agent(
        role="ProjectManager",
        goal="Aggregate tasks & highlight risks",
        backstory="Ensures deliverables & mitigations are clear",
        allow_delegation=False,
        verbose=False,
    )

    # Heuristic phase generation based on depth_level
    phases: List[Dict[str, Any]] = []
    for i in range(depth_level):
        phase_name = f"Phase {i+1}: {['Foundations','Core Implementation','Enhancements','Testing & QA','Deployment'][i % 5]}"
        tasks = [
            f"{architect.role}: Outline components for segment {i+1}",
            f"{researcher.role}: Identify libs/tools for segment {i+1}",
            f"{manager.role}: Define timeline & milestones for segment {i+1}",
        ]
        deliverables = [
            f"Architecture sketch {i+1}",
            f"Tech stack decision log {i+1}",
        ]
        phases.append({"name": phase_name, "tasks": tasks, "deliverables": deliverables})

    risks: List[Dict[str, str]] = []
    if include_risks:
        risks = [
            {"risk": "Technology mismatch", "mitigation": "Prototype critical integration early"},
            {"risk": "Timeline slippage", "mitigation": "Buffer each phase by 15%"},
        ][:2]

    assumptions = [
        "Basic dev environment available (Python, Git)",
        "Stakeholder requirements are stable for initial phases",
    ]

    reviewer_notes = "CrewAI roles instantiated heuristically; future iteration may execute actual tasks."
    duration_ms = int((time.time() - start) * 1000)
    return {
        "phases": phases,
        "risks": risks if include_risks else None,
        "assumptions": assumptions,
        "reviewer_notes": reviewer_notes,
        "timing_ms": duration_ms,
        "agents_used": ["crewai"],
    }
