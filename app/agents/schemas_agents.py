from __future__ import annotations

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# ---- Request Schemas ----

class CompareAgentsRequest(BaseModel):
    task: str = Field(
        ...,
        description="Natural language task to run across agent frameworks",
        examples=["Summarize the benefits of using async concurrency in Python."]
    )
    include_trace: bool = Field(
        True,
        description="Include per-framework trace list where available",
        examples=[True]
    )
    timeout_seconds: int = Field(
        30,
        ge=1,
        le=300,
        description="Soft timeout per framework in seconds (best-effort)",
        examples=[30]
    )

class PlanProjectRequest(BaseModel):
    objective: str = Field(
        ...,
        description="High-level project objective to plan",
        examples=["Build a minimal FastAPI microservice with CI pipeline"]
    )
    depth_level: int = Field(
        2,
        ge=1,
        le=5,
        description="Depth of hierarchical breakdown (phases -> tasks -> sub-tasks)",
        examples=[2]
    )
    include_risks: bool = Field(
        True,
        description="Include a risk register section",
        examples=[True]
    )
    include_reviewer: bool = Field(
        False,
        description="If true, run optional reviewer/critic refinement",
        examples=[False]
    )

class RunCodeTaskRequest(BaseModel):
    instruction: str = Field(
        ...,
        description="Instruction for code generation task",
        examples=["Write a Python function fib(n) returning the first n Fibonacci numbers"]
    )
    execute: bool = Field(
        False,
        description="If true, attempt to execute generated Python code in sandbox",
        examples=[True]
    )
    include_review: bool = Field(
        True,
        description="If true, include AI reviewer feedback",
        examples=[True]
    )
    max_exec_seconds: int = Field(
        5,
        ge=1,
        le=60,
        description="Max sandbox execution time in seconds",
        examples=[5]
    )

# ---- Response Schemas ----

class FrameworkResult(BaseModel):
    final_answer: Optional[str] = None
    trace: Optional[List[str]] = None
    error: Optional[str] = None
    meta: Dict[str, Any] = Field(default_factory=dict)

class CompareAgentsResponse(BaseModel):
    task: str
    results: Dict[str, FrameworkResult]
    timings_ms: Dict[str, int]
    token_usage: Dict[str, Any]
    executed_at: str
    meta: Dict[str, Any] = Field(default_factory=dict, description="High-level metadata (version, total_duration_ms, frameworks)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "task": "Summarize async benefits",
                "results": {
                    "autogen": {
                        "final_answer": "Async enables concurrent I/O improving throughput without extra threads.",
                        "trace": ["task_received:Summarize async benefits"],
                        "error": None,
                        "meta": {"duration_ms": 812, "framework": "autogen", "mode": "real", "rounds": 1}
                    },
                    "crewai": {
                        "final_answer": "CrewAI agent summary ...",
                        "trace": ["phase:analysis"],
                        "error": None,
                        "meta": {"duration_ms": 1045, "framework": "crewai", "mode": "real"}
                    }
                },
                "timings_ms": {"autogen": 812, "crewai": 1045, "langchain": 690, "smolagents": 950},
                "token_usage": {"autogen": {"input_tokens": 45, "output_tokens": 68}},
                "executed_at": "2025-10-31T12:00:00Z",
                "meta": {"version": "1.0", "total_duration_ms": 3500, "frameworks": ["autogen", "crewai", "langchain", "smolagents"]}
            }
        }
    }

class PlanPhase(BaseModel):
    name: str
    tasks: List[str]
    deliverables: List[str]

class RiskItem(BaseModel):
    risk: str
    mitigation: str

class ProjectPlan(BaseModel):
    phases: List[PlanPhase]
    risks: Optional[List[RiskItem]] = None
    assumptions: List[str] = Field(default_factory=list)
    reviewer_notes: Optional[str] = None

class PlanProjectResponse(BaseModel):
    objective: str
    plan: ProjectPlan
    meta: Dict[str, Any] = Field(default_factory=dict, description="Metadata including timing_ms, agents_used, version")

    model_config = {
        "json_schema_extra": {
            "example": {
                "objective": "Build a FastAPI microservice",
                "plan": {
                    "phases": [
                        {"name": "Design", "tasks": ["Clarify requirements", "Define data model"], "deliverables": ["ADR", "Data schema"]},
                        {"name": "Implementation", "tasks": ["Set up FastAPI app", "Add endpoints", "Write tests"], "deliverables": ["Code", "Test suite"]}
                    ],
                    "risks": [
                        {"risk": "Scope creep", "mitigation": "Lock requirements in ADR"}
                    ],
                    "assumptions": ["Team has API experience"],
                    "reviewer_notes": "Consider adding rate limiting early."
                },
                "meta": {"timing_ms": 1200, "agents_used": ["crewai", "autogen_reviewer"], "version": "1.0"}
            }
        }
    }

class CodeExecutionResult(BaseModel):
    ran: bool
    stdout: str
    stderr: str
    duration_ms: int
    error: Optional[str] = None

class RunCodeTaskResponse(BaseModel):
    instruction: str
    code: str
    execution: CodeExecutionResult
    review: Optional[Dict[str, Any]] = None
    analysis: Dict[str, Any]
    trace: List[str]
    timing_ms: int
    framework: str = "autogen"
    meta: Dict[str, Any] = Field(default_factory=dict, description="Metadata (duration, safety flags, version)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "instruction": "Write a function fib(n) returning list of first n Fibonacci numbers",
                "code": "def fib(n):\n    seq=[0,1]\n    for i in range(2,n):\n        seq.append(seq[-1]+seq[-2])\n    return seq[:n]",
                "execution": {"ran": True, "stdout": "[0, 1, 1, 2, 3]\n", "stderr": "", "duration_ms": 4, "error": None},
                "review": {"summary": "Code is correct; consider input validation for n <= 0"},
                "analysis": {"complexity": "O(n)", "security_flags": []},
                "trace": ["generate_code", "review_pass"],
                "timing_ms": 950,
                "framework": "autogen",
                "meta": {"duration_ms": 950, "sandbox": {"timeout_sec": 5}, "version": "1.0"}
            }
        }
    }
