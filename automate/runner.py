from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path

from .models import ToolResult
from .registry import get_tool

ROOT = Path(__file__).resolve().parent.parent


def run_tool(name: str, *, timeout: int | None = None, env: dict[str, str] | None = None) -> ToolResult:
    spec = get_tool(name)
    run_id = uuid.uuid4().hex
    script = ROOT / spec.script
    if not script.is_file():
        return ToolResult("failed", name, run_id, error=f"script not found: {spec.script}")

    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    started = time.time()
    try:
        completed = subprocess.run(
            [sys.executable, str(script)],
            cwd=ROOT,
            env=merged_env,
            capture_output=True,
            text=True,
            timeout=timeout or spec.timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        return ToolResult(
            "timeout",
            name,
            run_id,
            data={"duration_seconds": round(time.time() - started, 3)},
            error=f"tool exceeded {timeout or spec.timeout_seconds} seconds",
        )

    stdout = (completed.stdout or "").strip()
    stderr = (completed.stderr or "").strip()
    data = {
        "output": stdout,
        "exit_code": completed.returncode,
        "duration_seconds": round(time.time() - started, 3),
        "sources": [],
    }
    if completed.returncode == 0:
        return ToolResult("success", name, run_id, data=data)
    return ToolResult("failed", name, run_id, data=data, error=stderr or stdout or "tool failed")


def run_tool_json(name: str, **kwargs: object) -> str:
    return json.dumps(run_tool(name, **kwargs).to_dict(), ensure_ascii=False)
