"""Sandboxed code execution utilities for /agents/run/code-task endpoint.

Design Goals:
    - Restrict available builtins (remove file/network/dangerous modules by default).
    - Enforce wall-clock timeout.
    - Capture stdout/stderr cleanly.
    - Avoid writing to arbitrary filesystem paths (no persistence yet).

Security Notes:
    This is a minimal educational sandbox. It does NOT yet implement full process isolation
    (no separate OS process, seccomp, or memory limits). Future enhancements could spawn a
    subprocess with a locked-down environment or leverage containerization.
"""
from __future__ import annotations
import io
import os
import time
import threading
import uuid
from contextlib import redirect_stdout, redirect_stderr
from typing import Optional, Dict, Any
import socket

SAFE_BUILTINS = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "dict": dict,
    "enumerate": enumerate,
    "float": float,
    "int": int,
    "len": len,
    "list": list,
    "max": max,
    "min": min,
    "print": print,
    "range": range,
    "str": str,
    "sum": sum,
}

class SandboxResult:
    def __init__(self, stdout: str, stderr: str, duration_ms: int, error: Optional[str]):
        self.stdout = stdout
        self.stderr = stderr
        self.duration_ms = duration_ms
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stdout": self.stdout,
            "stderr": self.stderr,
            "duration_ms": self.duration_ms,
            "error": self.error,
        }


def execute_code(code: str, timeout_seconds: int = 5) -> SandboxResult:
    start = time.time()
    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()
    error: Optional[str] = None

    # Working directory isolation
    run_id = uuid.uuid4().hex
    base_dir = os.path.abspath(os.path.join(os.getcwd(), "sandbox_runs"))
    os.makedirs(base_dir, exist_ok=True)
    work_dir = os.path.join(base_dir, run_id)
    os.makedirs(work_dir, exist_ok=True)

    # Patch socket to disallow network
    original_socket = socket.socket
    def blocked_socket(*args, **kwargs):  # noqa: D401
        raise RuntimeError("Network access disabled in sandbox")
    socket.socket = blocked_socket  # type: ignore

    globals_dict = {"__builtins__": SAFE_BUILTINS, "__name__": "__sandbox__"}
    locals_dict: Dict[str, Any] = {}

    def thread_runner():
        nonlocal error
        try:
            with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
                exec(code, globals_dict, locals_dict)  # noqa: S102
        except Exception as e:  # noqa: BLE001
            error = f"{type(e).__name__}: {e}"[:800]

    thread = threading.Thread(target=thread_runner, daemon=True)
    thread.start()
    thread.join(timeout_seconds)
    if thread.is_alive():
        error = f"TimeoutError: execution exceeded {timeout_seconds}s"
        # Not forcibly killing thread; marked daemon so process exit cleans it.
    duration_ms = int((time.time() - start) * 1000)
    # Restore socket
    socket.socket = original_socket  # type: ignore
    return SandboxResult(stdout_buf.getvalue(), stderr_buf.getvalue(), duration_ms, error)

