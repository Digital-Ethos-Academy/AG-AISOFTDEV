"""Service layer orchestrating agent framework stub calls.

CURRENT STATE: All framework calls return stub data. Created 2025-10-30.
REFERENCE: See `docs/AGENT_ENDPOINTS_PLAN.md` for target architecture.

UPCOMING TASKS:
    - Replace sequential loop with concurrent execution (async + threadpool where needed).
    - Inject real runner implementations with error isolation.
    - Populate token_usage map from provider responses.
    - Support selective framework subset via query (frameworks=autogen,langchain,...).
    - Add global timeout & per-framework cancellation.
"""
from __future__ import annotations
import datetime as _dt
import asyncio
from typing import Dict, Callable, Any, Optional

from .runners_autogen import run_autogen_task
from .runners_crewai import run_crewai_task, run_crewai_plan
from .runners_langchain import run_langchain_task
from .runners_smolagents import run_smolagents_task
from .sandbox import execute_code
from . import logger


async def compare_agents(task: str, include_trace: bool = True) -> Dict:
    """Run all framework tasks concurrently.

    Each runner is CPU/network bound; wrap in threadpool to avoid blocking event loop.
    """
    runner_map: Dict[str, Callable[[str, bool], Dict[str, Any]]] = {
        "autogen": run_autogen_task,
        "crewai": run_crewai_task,
        "langchain": run_langchain_task,
        "smolagents": run_smolagents_task,
    }

    async def run_one(name: str, fn: Callable[[str, bool], Dict[str, Any]]):
        return name, await asyncio.to_thread(fn, task, include_trace)

    logger.info(f"compare_agents start task='{task[:60]}' frameworks={list(runner_map.keys())}")
    tasks = [run_one(n, f) for n, f in runner_map.items()]
    results_list = await asyncio.gather(*tasks, return_exceptions=True)

    results: Dict[str, Dict] = {}
    timings: Dict[str, int] = {}
    for item in results_list:
        if isinstance(item, Exception):  # unlikely due to per-call isolation
            # Assign generic error bucket
            name = f"error_{type(item).__name__}"
            results[name] = {"final_answer": None, "trace": [str(item)], "meta": {"framework": name}, "error": str(item)}
            timings[name] = 0
            continue
        name, data = item
        results[name] = data
        timings[name] = data.get("meta", {}).get("duration_ms", 0)

    envelope = {
        "task": task,
        "results": results,
        "timings_ms": timings,
        "token_usage": {},  # TODO: populate when token info available
        "executed_at": _dt.datetime.utcnow().isoformat() + "Z",
        "meta": {"concurrency": True, "framework_count": len(results)},
    }
    logger.info(f"compare_agents complete task='{task[:40]}' timings={timings}")
    return envelope


def _autogen_review(text: str) -> Optional[str]:
    """Attempt lightweight AutoGen critique of the plan text.

    Returns reviewer notes or None if Autogen unavailable.
    """
    try:
        import os
        if not os.getenv("OPENAI_API_KEY"):
            return None
        from autogen import AssistantAgent, UserProxyAgent  # type: ignore
        assistant = AssistantAgent(
            name="critic",
            system_message="You are a senior software reviewer. Provide concise critique and missing considerations.",
            llm_config={"model": "gpt-4o-mini", "temperature": 0.2},
        )
        user = UserProxyAgent(name="plan_author", code_execution_config={"use_docker": False})
        # Send single turn: ask for critique of text
        assistant.initiate_chat(user, message=f"Critique this project plan for clarity, risk coverage, and missing tasks:\n{text}\nRespond in <=120 words.", max_turns=1)
        history = assistant.chat_messages[user]  # type: ignore
        for h in reversed(history):
            if h.get("role") == "assistant":
                return h.get("content", "").strip()[:800]
        return None
    except Exception:
        return None


def plan_project(objective: str, depth_level: int = 2, include_risks: bool = True, include_reviewer: bool = False) -> Dict:
    start = _dt.datetime.utcnow()
    logger.info(f"plan_project start objective='{objective[:60]}' depth={depth_level} risks={include_risks} reviewer={include_reviewer}")
    plan_data = run_crewai_plan(objective, depth_level=depth_level, include_risks=include_risks)
    reviewer_notes = plan_data.get("reviewer_notes")

    autogen_used = False
    if include_reviewer:
        # Flatten plan phases text for critique
        phases_text = "\n".join(
            f"{p['name']}: tasks={', '.join(p['tasks'])}; deliverables={', '.join(p['deliverables'])}" for p in plan_data["phases"]
        )
        critique = _autogen_review(f"Objective: {objective}\nPhases:\n{phases_text}")
        if critique:
            reviewer_notes = (reviewer_notes or "") + ("\nAUTO-GEN REVIEW:\n" + critique)
            autogen_used = True

    agents_used = plan_data.get("agents_used", [])
    if autogen_used:
        agents_used.append("autogen_reviewer")

    duration_ms = plan_data.get("timing_ms", 0)
    meta = {
        "timing_ms": duration_ms,
        "agents_used": agents_used,
        "version": "1.0",
        "review_included": include_reviewer,
    }

    return {
        "objective": objective,
        "plan": {
            "phases": plan_data["phases"],
            "risks": plan_data.get("risks"),
            "assumptions": plan_data.get("assumptions", []),
            "reviewer_notes": reviewer_notes,
        },
        "meta": meta,
    }


def run_code_task(instruction: str, execute: bool, include_review: bool, max_exec_seconds: int) -> Dict:
    start = _dt.datetime.utcnow()
    logger.info(f"run_code_task start instruction='{instruction[:60]}' execute={execute} review={include_review} timeout={max_exec_seconds}")
    trace = []
    framework = "autogen"
    # Attempt autogen code generation minimal pattern; fallback stub.
    generated_code = None
    try:
        import os
        if os.getenv("OPENAI_API_KEY"):
            from autogen import AssistantAgent, UserProxyAgent  # type: ignore
            assistant = AssistantAgent(
                name="coder",
                system_message=(
                    "You generate a single Python function only. No prose. Function must be self-contained and return a result."
                ),
                llm_config={"model": "gpt-4o-mini", "temperature": 0.2},
            )
            user = UserProxyAgent(name="requester", code_execution_config={"use_docker": False})
            prompt = (
                f"Write a Python function fulfilling this instruction: {instruction}.\n"
                "Constraints: no network calls, no file I/O, pure computation, name it solve_task."
            )
            assistant.initiate_chat(user, message=prompt, max_turns=1)
            history = assistant.chat_messages[user]  # type: ignore
            for h in reversed(history):
                if h.get("role") == "assistant":
                    generated_code = h.get("content", "")
                    break
            trace.append("autogen:generated_code")
        else:
            trace.append("autogen:missing_openai_key_stub")
    except Exception as e:
        trace.append(f"autogen:error:{e}")

    if not generated_code:
        # Fallback stub code
        generated_code = (
            "def solve_task():\n    "
            f"return 'Stub result for: {instruction[:60]}'"
        )
        trace.append("stub:used_fallback_code")

    code = generated_code.strip()
    # Basic analysis
    analysis = {
        "lines": code.count("\n") + 1,
        "complexity_estimate": min(10, code.count("if ") + code.count("for ") + 1),
        "chars": len(code),
    }

    review = None
    if include_review:
        # Simple heuristic review
        suggestions = []
        if "solve_task" not in code:
            suggestions.append("Function name should be solve_task per contract.")
        if analysis["lines"] > 40:
            suggestions.append("Consider splitting logic into helper functions.")
        if "import " in code:
            suggestions.append("Avoid imports per sandbox constraint.")
        review = {"suggestions": suggestions or ["Looks concise."]}
        trace.append("review:heuristic_complete")

    execution_dict = {"ran": False, "stdout": "", "stderr": "", "duration_ms": 0, "error": None}
    if execute:
        sandbox_result = execute_code(code, timeout_seconds=max_exec_seconds)
        execution_dict.update({
            "ran": True,
            "stdout": sandbox_result.stdout,
            "stderr": sandbox_result.stderr,
            "duration_ms": sandbox_result.duration_ms,
            "error": sandbox_result.error,
        })
        trace.append("sandbox:executed")
        if sandbox_result.error:
            trace.append(f"sandbox:error:{sandbox_result.error}")

    duration_ms = int((_dt.datetime.utcnow() - start).total_seconds() * 1000)
    meta = {
        "timing_ms": duration_ms,
        "executed": execute,
        "version": "1.0",
        "mode": "real" if "autogen:generated_code" in trace else "stub",
    }

    return {
        "instruction": instruction,
        "code": code,
        "execution": execution_dict,
        "review": review,
        "analysis": analysis,
        "trace": trace,
        "timing_ms": duration_ms,
        "framework": framework,
        "meta": meta,
    }
