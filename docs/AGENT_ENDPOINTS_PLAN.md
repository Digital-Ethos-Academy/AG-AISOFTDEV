## 17. Interactive Demo & Postman Usage

### 17.1 Swagger / OpenAPI
Launch the server and open `http://localhost:8000/docs`.
1. Call `/agents/health` to verify readiness.
2. Run `/agents/demo/compare` with a short task (e.g. "Summarize async benefits in Python").
3. Run `/agents/plan/project` and toggle `include_reviewer` to see reviewer notes.
4. Run `/agents/run/code-task` with `execute=true` to exercise the sandbox; inspect `execution` and `meta` fields.

### 17.2 Postman Collection
Files:
- `postman/AgentsDemo.postman_collection.json`
- `postman/AgentsDemo.postman_environment.json`

Import both into Postman. No API keys are required in the Postman environment (they are loaded from the server-side `.env`). Click "Run Collection" to execute all requests; tests assert core fields.

### 17.3 Newman CLI
Install and run:
```bash
npm install -g newman
newman run postman/AgentsDemo.postman_collection.json \
  -e postman/AgentsDemo.postman_environment.json \
  --reporters cli,json \
  --reporter-json-export artifacts/postman_run_report.json
```

Optional iteration data:
```bash
newman run postman/AgentsDemo.postman_collection.json \
  -e postman/AgentsDemo.postman_environment.json \
  -d data/tasks.csv
```

### 17.4 Python Smoke Script
```python
import requests, time
start = time.time()
r = requests.post("http://localhost:8000/agents/demo/compare", json={"task":"List three benefits of async","include_trace":True,"timeout_seconds":30})
print("Status", r.status_code)
data = r.json()
print("Frameworks:", list(data.get("results", {}).keys()))
print("Total ms:", data.get("meta", {}).get("total_duration_ms"))
print("Autogen answer:", data.get("results", {}).get("autogen", {}).get("final_answer"))
```

### 17.5 Troubleshooting
| Symptom | Possible Cause | Fix |
|---------|----------------|-----|
| Autogen returns stub | Missing `OPENAI_API_KEY` | Export key & restart |
| Long latency (>30s) | External API slowness | Reduce frameworks or increase timeout |
| Sandbox execution error | Disallowed import / timeout | Adjust instruction or `max_exec_seconds` |
| Server stops on curl (130) | Manual SIGINT | Avoid Ctrl-C; use Python script |

---
End of document additions.
# Agent Demonstration Endpoints Plan

## 1. Overview
We will extend the existing FastAPI application by adding a small **Agents API surface** whose sole purpose is educational: to showcase why multi-agent / tool-using frameworks (AutoGen, CrewAI, LangChain Agents, smolagents) provide capabilities beyond a single raw LLM completion.

These endpoints are explicitly orthogonal to the onboarding domain; they are self-contained demos. They will:
- Provide side‑by‑side comparisons across frameworks.
- Illustrate orchestration (planning, delegation, refinement loops).
- Expose internal reasoning traces, tool calls, and timing/token metrics for transparency.

## 2. Target Endpoints (Initial Trio)
| Endpoint | Method | Purpose | Frameworks Involved |
|----------|--------|---------|---------------------|
| `/agents/demo/compare` | POST | Run same user task through multiple frameworks and compare outputs, reasoning, latency. | AutoGen, CrewAI, LangChain, smolagents |
| `/agents/plan/project` | POST | Hierarchical / collaborative planning of a software mini-project objective. | CrewAI (primary) + optional post-review via AutoGen |
| `/agents/run/code-task` | POST | Generate & (optionally) execute Python code safely with critique/refinement loop. | AutoGen (Coder + Reviewer + UserProxy) + optional LangChain tool for static analysis |

### 2.1 `/agents/demo/compare`
**Use Case:** "Summarize today’s AI news in 5 concise bullets" (example). Task string provided by client.
**Flow:**
1. Receive `task` + optional flags (`include_trace`, `timeout_seconds`).
2. For each framework, lazily import modules and run a minimal agent configuration:
   - AutoGen: Two-agent (AssistantCoder + UserProxy) with reasoning messages only (no code execution).
   - CrewAI: Simple crew of Researcher → Synthesizer roles.
   - LangChain: Tool-calling agent (Tavily search + summarizer LLM prompt template).
   - smolagents: `CodeAgent` with a lightweight search or hardcoded fact tool.
3. Aggregate results + metrics.
4. Return unified response envelope.

**Response Envelope (Proposed):**
```json
{
  "task": "...",
  "results": {
    "autogen": {"final_answer": "...", "trace": [...]},
    "crewai": {"final_answer": "...", "steps": [...]},
    "langchain": {"final_answer": "...", "tool_calls": [...]},
    "smolagents": {"final_answer": "...", "thoughts": [...]}
  },
  "meta": {
    "timings_ms": {"autogen": 0, "crewai": 0, "langchain": 0, "smolagents": 0},
    "token_usage": {"autogen": {}, "crewai": {}, "langchain": {}, "smolagents": {}},
    "executed_at": "ISO8601"
  },
  "errors": {"autogen": null, "crewai": null, "langchain": null, "smolagents": null}
}
```

### 2.2 `/agents/plan/project`
**Use Case:** User supplies a high-level objective like: "Build a CLI that syncs local markdown notes to an S3 bucket with conflict detection."  Endpoint returns structured plan.
**Flow:**
1. Parse `objective` + optional `depth_level`, `include_risks`.
2. CrewAI crew configuration:
   - Roles: Architect, Researcher, ProjectManager.
   - Sequence: Architect drafts phases; Researcher adds tech details; ProjectManager aggregates & risk register.
3. (Optional) AutoGen Reviewer agent critiques resulting plan for clarity/scoping.
4. Return structured plan object including phases, tasks, risks, clarifications, reviewer notes.

**Response Shape (Proposed):**
```json
{
  "objective": "...",
  "plan": {
    "phases": [
      {"name": "Setup", "tasks": ["Initialize repo", "Configure S3 client"], "deliverables": ["pyproject.toml", "aws credentials profile"]},
      {"name": "Core Sync Logic", "tasks": [...], "deliverables": [...]}
    ],
    "risks": [{"risk": "Rate limits", "mitigation": "Retry with backoff"}],
    "assumptions": ["User has AWS IAM user with proper permissions"],
    "reviewer_notes": "Optional critique text"
  },
  "meta": {"timing_ms": 0, "agents_used": ["crewai", "autogen_reviewer"]}
}
```

### 2.3 `/agents/run/code-task`
**Use Case:** Safe environment for an agent to propose Python code (e.g., "List prime numbers under 200 and compute their average") and optionally execute it in a sandbox.
**Flow:**
1. Receive `instruction` + flags: `execute` (bool), `max_exec_seconds`, `include_review`.
2. AutoGen loop:
   - Coder drafts code snippet.
   - Reviewer suggests improvements (if `include_review`).
   - Final code selected.
3. If `execute = true`, run in constrained sandbox (working directory, resource limits) and capture stdout/stderr (no network, minimal file access).
4. Optionally pass code through a LangChain static analysis tool (regex-based complexity hints) for metadata.
5. Return code, analysis, execution results, reasoning trace.

**Response Shape (Proposed):**
```json
{
  "instruction": "...",
  "code": "def primes(): ...",
  "execution": {"ran": true, "stdout": "2 3 5 ...", "stderr": "", "duration_ms": 42},
  "review": {"suggestions": "Consider using a sieve for efficiency."},
  "analysis": {"cyclomatic_estimate": 3, "lines": 27},
  "trace": [...],
  "meta": {"timing_ms": 0, "framework": "autogen"}
}
```

## 3. Architectural Notes
- Each framework integration isolated in `app/agents/` submodules:
  - `runners_autogen.py`, `runners_crewai.py`, `runners_langchain.py`, `runners_smolagents.py`.
  - Facade file `service.py` orchestrates concurrency & normalization.
- Lazy imports inside runner functions to avoid loading all frameworks per request.
- Use `async def` FastAPI endpoints; blocking framework calls wrapped with `anyio.to_thread.run_sync` or `starlette.concurrency.run_in_threadpool`.
- Introduce shared pydantic schemas in `schemas_agents.py` for request/response validation.

## 4. Data Contracts & Versioning
- Envelope fields: `task|objective|instruction`, `result sections`, `trace`, `meta`, `errors`.
- Include `version: "1.0"` in `meta` for forward compatibility.
- Token usage captured when provider returns usage metadata (may initially be null).

## 5. Error Handling Strategy
- Per-framework try/except; never let one failure abort the entire composite response in `/agents/demo/compare`.
- Return error strings in `errors` map and include partial trace if available.
- For sandbox execution: classify errors (`ImportError`, `TimeoutError`, `RuntimeError`).

## 6. Sandbox & Security (Code Execution)
- Restricted working directory `./sandbox_runs/<uuid>`.
- Disallow network calls (optionally patch `socket` during execution).
- Limit CPU time / wall time (timeout wrapper) and memory (future enhancement).
- Remove dangerous builtins (e.g., `__import__` gating) if necessary.
- Log executed code for auditing but redact secrets.

## 7. Dependencies
Planned additions (subject to existing `requirements.txt`):
- `pyautogen` (AutoGen)
- `crewai`
- `smolagents[litellm]`
- `tavily-python` (for LangChain search) + `langchain`, `langchain-openai`
- (Optional) `python-dotenv` if not already loaded for agent-specific keys.

Lazy import pattern example:
```python
def run_langchain_task(task: str):
    from langchain_openai import ChatOpenAI
    from langchain_community.tools.tavily_search import TavilySearchResults
    ...
```

## 8. Configuration & Environment
- API keys loaded via existing `.env` using `load_dotenv()`.
- Endpoint-level validation: if missing key required for framework, return framework-specific error entry.
- Optional query parameter `frameworks` to subset comparison run (future).

## 9. Observability & Metrics
- Capture start/end monotonic times per framework.
- Structure for token usage, cost estimates (future: integrate with provider usage endpoints).
- Add simple debug logging `INFO` per framework invocation.

## 10. Testing Approach
- Unit tests for each runner (mock LLM/model responses to keep tests fast & deterministic).
- Contract tests for response schema using `pydantic` validation.
- Execution sandbox test injects code raising exception and asserts safe capture.
- Use feature flag / environment variable `AGENTS_ENABLED` to skip tests if deps absent.

## 11. Roadmap (Beyond Initial Trio)
- Streaming reasoning via Server-Sent Events or WebSocket for `/agents/run/code-task`.
- Add `/agents/memory/chat` for conversation continuity demonstration.
- Benchmark endpoint for latency & token comparison.
- RAG curation multi-agent pipeline.
- Safety classifier ensemble.

## 12. Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|-----------|
| Dependency bloat | Larger startup time | Lazy imports, optional install groups |
| API key absence | Fail entire response | Per-framework error entries |
| Code execution exploit | Security breach | Sandboxed FS, timeout, restricted builtins |
| Long-running agent loops | High latency | `timeout_seconds` parameter with graceful abort |
| Token usage unavailable | Incomplete metrics | Mark `null`, add later instrumentation |

## 13. Acceptance Criteria
- All three endpoints mounted and documented in OpenAPI schema.
- Successful response when basic task provided (even if some frameworks missing keys → error map populated).
- Sandbox executes trivial safe code and returns stdout.
- Plan endpoint returns at least 2 phases with tasks and a risk list.
- Compare endpoint returns entries for up to 4 frameworks with timing data.

## 14. Next Steps
1. Add dependency placeholders (no install yet) and create runners scaffold files.
2. Implement `/agents/demo/compare` with stubbed fake outputs first → unit test.
3. Fill real framework integrations progressively.
4. Implement sandbox utilities.
5. Extend README with Agents section.

## 15. Demonstration Curl Commands
Run these against a local FastAPI server (e.g., `uvicorn app.main:app --reload`).

### Compare Endpoint
```bash
curl -s -X POST http://localhost:8000/agents/demo/compare \
  -H 'Content-Type: application/json' \
  -d '{"task":"Summarize today\u2019s AI news in 5 bullets","include_trace":true}' | jq '.meta,.timings_ms'
```

### Plan Project Endpoint (with reviewer)
```bash
curl -s -X POST http://localhost:8000/agents/plan/project \
  -H 'Content-Type: application/json' \
  -d '{"objective":"Build a markdown sync tool","depth_level":2,"include_risks":true,"include_reviewer":true}' | jq '.plan.reviewer_notes,.meta'
```

### Code Task Endpoint (execute & review)
```bash
curl -s -X POST http://localhost:8000/agents/run/code-task \
  -H 'Content-Type: application/json' \
  -d '{"instruction":"Compute factorial of 6","execute":true,"include_review":true,"max_exec_seconds":3}' | jq '.execution,.meta'
```

### Code Task Timeout Demonstration
```bash
curl -s -X POST http://localhost:8000/agents/run/code-task \
  -H 'Content-Type: application/json' \
  -d '{"instruction":"Produce an infinite loop","execute":true,"include_review":false,"max_exec_seconds":1}' | jq '.execution.error,.meta'
```

## 16. Logging & Security Compliance
Implemented items vs initial spec:
- Logging: `app/agents/__init__.py` defines a dedicated `agents` logger; service functions emit INFO logs for start/complete events with timing and modes.
- Sandbox: Working directory isolation (`sandbox_runs/<uuid>` created per execution) and network access blocked by patching `socket.socket`. Timeout produces controlled error string. Restricted builtins loaded; no file or network primitives exposed.
- Error Isolation: Each framework invocation wrapped so failures produce fallback entries (compare endpoint) or error metadata (code-task execution result).
- Versioning: Responses include `meta.version = "1.0"` for forward compatibility.
- Concurrency: Compare endpoint executes framework runners in parallel using asyncio + thread offload.

Pending (future hardening):
- Memory limits & CPU quota for sandbox (subprocess isolation).
- Selective framework filtering (`frameworks` query parameter for compare endpoint).
- Token usage collection and cost estimations.


---
**Version:** 1.0  
**Date:** 2025-10-30  
**Author:** Agents API Planning
