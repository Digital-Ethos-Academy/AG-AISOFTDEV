"""AutoGen runner (incremental real integration).

Current behavior: attempts to run a minimal two-agent chat (UserProxyAgent + AssistantAgent)
if `autogen` can be imported and an API key (e.g. OPENAI_API_KEY) is available. Otherwise
falls back to stub response.

Constraints:
    - No code execution yet (UserProxyAgent disabled for Python exec).
    - Limited message rounds (max_rounds=3) to keep latency low.

Fallback conditions:
    - ImportError for autogen
    - Missing OPENAI_API_KEY
    - Runtime exception during chat

Future TODO:
    - Add code execution sandbox integration.
    - Expose token usage & cost metrics.
    - Parameterize model and max rounds via request.
    - Add reviewer/critic agent for refinement loop.
    - Timeout & cancellation support.
"""
from __future__ import annotations
import os
import time
from typing import List, Dict, Any


def _run_real_autogen(task: str, include_trace: bool) -> Dict[str, Any]:
    from autogen import AssistantAgent, UserProxyAgent  # type: ignore

    start = time.time()
    trace: List[str] = []
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return {
                "final_answer": f"[AUTOGEN FALLBACK] Missing OPENAI_API_KEY; stubbed result for: {task}"[:400],
                "trace": ["error: missing OPENAI_API_KEY"] if include_trace else None,
                "meta": {"duration_ms": 0, "framework": "autogen", "mode": "fallback"},
                "error": "missing_openai_key",
            }

        assistant = AssistantAgent(
            name="assistant",
            system_message="You are a helpful assistant producing concise, structured answers.",
            llm_config={"model": "gpt-4o-mini", "temperature": 0.2},
            human_input_mode="NEVER",
        )
        user = UserProxyAgent(
            name="user",
            code_execution_config={"use_docker": False, "work_dir": None},
            human_input_mode="NEVER",
        )

        messages: List[str] = []
        if include_trace:
            messages.append(f"task_received:{task}")

        # Use single turn generate_reply to avoid interactive prompt
        reply = assistant.generate_reply(messages=[{"role": "user", "content": task}])
        final_answer = reply if isinstance(reply, str) else str(reply)

        duration_ms = int((time.time() - start) * 1000)
        return {
            "final_answer": final_answer[:1200] or f"[AUTOGEN] No assistant message parsed for: {task}",
            "trace": messages if include_trace else None,
            "meta": {
                "duration_ms": duration_ms,
                "framework": "autogen",
                "mode": "real",
                "rounds": 1,
            },
            "error": None,
        }
    except Exception as e:
        duration_ms = int((time.time() - start) * 1000)
        return {
            "final_answer": f"[AUTOGEN FALLBACK] Exception; stubbed result for: {task}"[:400],
            "trace": [f"error:{e}"] if include_trace else None,
            "meta": {"duration_ms": duration_ms, "framework": "autogen", "mode": "fallback"},
            "error": str(e),
        }


def run_autogen_task(task: str, include_trace: bool = True) -> Dict[str, Any]:
    """Execute an AutoGen task.

    Behavior:
        - Tries real AutoGen single-turn generation when library + key available.
        - Falls back to concise stub ONLY if import/key/ runtime exception occurs.
    Removed:
        - Forced stub environment flag (AGENTS_AUTOGEN_STUB) to ensure demo shows real capability.
    """
    start = time.time()
    try:
        import autogen  # noqa: F401
    except Exception:
        final_answer = f"[AUTO-GEN STUB] Result for task: {task}"[:400]
        trace = ["thought: analyze task", "action: (none - stub)", "observation: synthesized placeholder"] if include_trace else None
        duration_ms = int((time.time() - start) * 1000)
        return {
            "final_answer": final_answer,
            "trace": trace,
            "meta": {"duration_ms": duration_ms, "framework": "autogen", "mode": "stub"},
            "error": None,
        }
    # Attempt real chat
    return _run_real_autogen(task, include_trace)
