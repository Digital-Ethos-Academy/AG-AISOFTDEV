"""LangChain runner.

Current mode: Attempts real tool + LLM agent if dependencies & API keys are available; otherwise
falls back to stub behavior. This incremental implementation focuses on:
    - Tavily search tool (if installed & API key available)
    - OpenAI Chat model via langchain-openai
    - Simple prompt to summarize task
    - Trace collection of tool calls & final output

Fallback triggers if:
    - Import errors occur
    - Missing OPENAI_API_KEY environment variable
    - Runtime exceptions during agent execution

Future TODO:
    - Support Anthropic / other providers
    - Streaming token output
    - Token usage & cost estimation
    - Configurable tool registry
    - Retry/backoff strategy
"""
from __future__ import annotations
import time
import os
from typing import List, Dict, Any

def _run_real_langchain(task: str, include_trace: bool) -> Dict[str, Any]:
    """Attempt real LangChain execution with Tavily + OpenAI.

    Returns dict with keys: final_answer, trace, meta, error.
    """
    from langchain_openai import ChatOpenAI  # type: ignore
    try:
        # Updated import per deprecation warning: use langchain_tavily package
        from langchain_tavily import TavilySearch  # type: ignore
    except Exception:
        TavilySearch = None  # type: ignore

    trace: List[str] = []
    start = time.time()
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return {
                "final_answer": f"[LANGCHAIN FALLBACK] Missing OPENAI_API_KEY; stubbed response for: {task}"[:400],
                "trace": ["error: missing OPENAI_API_KEY"],
                "meta": {"duration_ms": 0, "framework": "langchain", "mode": "fallback"},
                "error": "missing_openai_key",
            }

        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

        # Prepare tool invocation if Tavily available and API key present
        tool_outputs: List[str] = []
        if TavilySearch and os.getenv("TAVILY_API_KEY"):
            try:
                tavily = TavilySearch(max_results=3)
                q = f"context search for task: {task}"[:200]
                search_res = tavily.invoke(q)
                tool_outputs.append(str(search_res)[:500])
                trace.append("tool:tavily_search invoked")
            except Exception as e:
                trace.append(f"tool:tavily_search error:{e}")

        prompt = (
            "You are an assistant summarizing an input task. \n"  # simple system-like guidance
            f"TASK: {task}\n"
            "If any search context is provided, synthesize it into concise bullet points (<=5)."
        )
        # LangChain ChatOpenAI expects list of messages normally; using invoke with string for simplicity.
        lc_start = time.time()
        response = llm.invoke(prompt)
        lc_duration = int((time.time() - lc_start) * 1000)
        final_answer = getattr(response, "content", str(response))[:1200]
        if include_trace:
            if tool_outputs:
                trace.append("thought: integrate search results")
            trace.append("thought: craft summary")
        duration_ms = int((time.time() - start) * 1000)
        return {
            "final_answer": final_answer,
            "trace": trace if include_trace else None,
            "meta": {
                "duration_ms": duration_ms,
                "framework": "langchain",
                "mode": "real",
                "llm_latency_ms": lc_duration,
                "tools_used": ["tavily_search"] if tool_outputs else [],
            },
            "error": None,
        }
    except Exception as e:  # Broad catch to fallback
        duration_ms = int((time.time() - start) * 1000)
        return {
            "final_answer": f"[LANGCHAIN FALLBACK] Exception; stubbed result for: {task}"[:400],
            "trace": [f"error:{e}"],
            "meta": {"duration_ms": duration_ms, "framework": "langchain", "mode": "fallback"},
            "error": str(e),
        }


def run_langchain_task(task: str, include_trace: bool = True) -> Dict[str, Any]:
    start = time.time()
    try:
        # Try imports first; if they fail we fallback immediately.
        import langchain_openai  # noqa: F401
    except Exception:
        # immediate stub fallback
        final_answer = f"[LANGCHAIN STUB] Response for: {task}"[:400]
        trace = ["tool: tavily_search (stub)", "thought: compose summary"] if include_trace else None
        duration_ms = int((time.time() - start) * 1000)
        return {
            "final_answer": final_answer,
            "trace": trace,
            "meta": {"duration_ms": duration_ms, "framework": "langchain", "mode": "stub"},
            "error": None,
        }

    # Attempt real execution
    return _run_real_langchain(task, include_trace)
    start = time.time()
    final_answer = f"[LANGCHAIN STUB] Response for: {task}"[:400]
    trace: List[str] = []
    if include_trace:
        trace = ["tool: tavily_search (stub)", "thought: compose summary"]
    duration_ms = int((time.time() - start) * 1000)
    return {
        "final_answer": final_answer,
        "trace": trace,
        "meta": {"duration_ms": duration_ms, "framework": "langchain"},
        "error": None,
    }
