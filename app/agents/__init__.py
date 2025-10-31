"""Agents module: provides educational agent demonstration endpoints.

Real framework integrations (AutoGen, CrewAI, LangChain, smolagents) are added incrementally.
This package configures a lightweight logger for observability of agent orchestration calls.
"""

from __future__ import annotations
import logging

logger = logging.getLogger("agents")
if not logger.handlers:
	handler = logging.StreamHandler()
	formatter = logging.Formatter("%(asctime)s [%(levelname)s] agents: %(message)s")
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	logger.setLevel(logging.INFO)

__all__ = ["logger"]
