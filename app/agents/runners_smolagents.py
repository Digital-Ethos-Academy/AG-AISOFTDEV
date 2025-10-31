"""smolagents runner (incremental real integration).

Attempts to use a lightweight CodeAgent (or TextAgent fallback) if smolagents
is installed and a model provider key (e.g., OPENAI_API_KEY) is present via LiteLLM.
Falls back to stub data otherwise.

Fallback conditions:
    - ImportError for smolagents or litellm
    - Missing OPENAI_API_KEY (for default OpenAI model)
    - Runtime exception during agent reasoning

Future TODO:
    - Custom tool registry (e.g., small math/search tools)
    - Streaming reasoning via SSE
    - Code execution sandbox for generated Python snippets
    - Token usage & cost metrics
"""
from __future__ import annotations
import os
import time
from typing import List, Dict, Any


def _run_real_smolagents(task: str, include_trace: bool) -> Dict[str, Any]:
    from smolagents import CodeAgent  # type: ignore
    try:
        from smolagents import LiteLLMModel  # type: ignore
    except Exception:
        # fallback: return stub if LiteLLMModel missing
        return {
            "final_answer": f"[SMOLAGENTS FALLBACK] LiteLLMModel missing; stub for: {task}"[:400],
            "trace": ["error: missing LiteLLMModel"] if include_trace else None,
            "meta": {"duration_ms": 0, "framework": "smolagents", "mode": "fallback"},
            "error": "missing_litellm_model",
        }

    start = time.time()
    trace: List[str] = []
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return {
                "final_answer": f"[SMOLAGENTS FALLBACK] Missing OPENAI_API_KEY; stubbed result for: {task}"[:400],
                "trace": ["error: missing OPENAI_API_KEY"] if include_trace else None,
                "meta": {"duration_ms": 0, "framework": "smolagents", "mode": "fallback"},
                "error": "missing_openai_key",
            }

        model = LiteLLMModel(model="gpt-4o-mini", temperature=0.2)
        agent = CodeAgent(model=model, max_steps=4, add_base_tools=False)

        # Provide a prompt that encourages concise structured output
        prompt = (
            "You are a lightweight reasoning agent. Provide a concise structured answer.\n"
            f"TASK: {task}\n"
            "Format output as bullet points when appropriate."
        )
        answer = agent.run(prompt)
        if include_trace and hasattr(agent, "steps"):
            for step in getattr(agent, "steps", [])[:10]:  # limit trace length
                trace.append(f"step:{getattr(step, 'thought', '')[:80]}")
        duration_ms = int((time.time() - start) * 1000)
        return {
            "final_answer": str(answer)[:1200],
            "trace": trace if include_trace else None,
            "meta": {"duration_ms": duration_ms, "framework": "smolagents", "mode": "real", "steps": len(trace)},
            "error": None,
        }
    except Exception as e:
        duration_ms = int((time.time() - start) * 1000)
        return {
            "final_answer": f"[SMOLAGENTS FALLBACK] Exception; stubbed result for: {task}"[:400],
            "trace": [f"error:{e}"] if include_trace else None,
            "meta": {"duration_ms": duration_ms, "framework": "smolagents", "mode": "fallback"},
            "error": str(e),
        }


def run_smolagents_task(task: str, include_trace: bool = True) -> Dict[str, Any]:
    start = time.time()
    try:
        import smolagents  # noqa: F401
    except Exception:
        final_answer = f"[SMOLAGENTS STUB] Lightweight output for: {task}"[:400]
        trace = ["react_step: consider task", "react_step: produce concise answer"] if include_trace else None
        duration_ms = int((time.time() - start) * 1000)
        return {
            "final_answer": final_answer,
            "trace": trace,
            "meta": {"duration_ms": duration_ms, "framework": "smolagents", "mode": "stub"},
            "error": None,
        }
    return _run_real_smolagents(task, include_trace)
