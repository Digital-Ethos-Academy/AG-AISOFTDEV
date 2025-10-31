"""FastAPI router exposing stubbed agent demonstration endpoints.
"""
from __future__ import annotations
from fastapi import APIRouter

from .schemas_agents import (
    CompareAgentsRequest,
    CompareAgentsResponse,
    PlanProjectRequest,
    PlanProjectResponse,
    RunCodeTaskRequest,
    RunCodeTaskResponse,
)
from .service import compare_agents, plan_project, run_code_task

router = APIRouter(prefix="/agents", tags=["Agents"])

@router.post(
    "/demo/compare",
    response_model=CompareAgentsResponse,
    summary="Compare multiple agent frameworks on the same task",
    description="Runs the provided natural language task through each available framework (AutoGen, CrewAI, LangChain, smolagents) concurrently and returns their outputs, traces, and timing metadata. Individual framework failures are isolated and reported without failing the whole request.",
)
async def compare_agents_endpoint(req: CompareAgentsRequest) -> CompareAgentsResponse:
    """Execute cross-framework comparison.

    Returns structured results keyed by framework name along with per-framework timing and aggregated metadata.
    """
    data = await compare_agents(task=req.task, include_trace=req.include_trace)
    return CompareAgentsResponse(**data)

@router.post(
    "/plan/project",
    response_model=PlanProjectResponse,
    summary="Generate a phased project plan",
    description="Produces a hierarchical multi-phase plan for the given objective. Optionally performs an AI reviewer pass to critique and refine phases and risks.",
)
def plan_project_endpoint(req: PlanProjectRequest) -> PlanProjectResponse:
    """Generate project plan with optional reviewer refinement."""
    data = plan_project(
        objective=req.objective,
        depth_level=req.depth_level,
        include_risks=req.include_risks,
        include_reviewer=req.include_reviewer,
    )
    return PlanProjectResponse(**data)

@router.post(
    "/run/code-task",
    response_model=RunCodeTaskResponse,
    summary="Generate and optionally execute Python code for a task",
    description="Uses an AI coding agent to draft Python code, optionally executes it inside a hardened sandbox, and can include a reviewer analysis plus static heuristic checks.",
)
def run_code_task_endpoint(req: RunCodeTaskRequest) -> RunCodeTaskResponse:
    """Run code generation + optional sandboxed execution."""
    data = run_code_task(
        instruction=req.instruction,
        execute=req.execute,
        include_review=req.include_review,
        max_exec_seconds=req.max_exec_seconds,
    )
    return RunCodeTaskResponse(**data)


@router.get(
    "/health",
    summary="Agents subsystem health check",
    description="Lightweight readiness probe for demo / monitoring. Returns static status plus list of logical subcomponents.",
    tags=["Agents"],
)
def agents_health() -> dict:
    return {
        "status": "ok",
        "components": ["compare", "plan", "code-task"],
        "frameworks": ["autogen", "crewai", "langchain", "smolagents"],
    }
