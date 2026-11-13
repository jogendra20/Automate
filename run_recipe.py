"""Run one automation recipe with reliable status reporting.

Usage:
    python run_recipe.py scripts/arxiv_papers.py
    python run_recipe.py scripts/arxiv_papers.py --deliver

Delivery is opt-in. Without --deliver this runner only writes output.txt and
exit_code.txt and prints a JSON result; it never calls Telegram or Nexus store
endpoints.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("script", type=Path)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--deliver", action="store_true", help="run send_output.py after success/failure")
    args = parser.parse_args()

    script = args.script if args.script.is_absolute() else ROOT / args.script
    if not script.is_file():
        print(json.dumps({"status": "failed", "error": f"script not found: {script}"}))
        return 2

    started = time.time()
    try:
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=ROOT,
            env=os.environ.copy(),
            capture_output=True,
            text=True,
            timeout=args.timeout,
        )
        output = (result.stdout or "").strip()
        error = (result.stderr or "").strip()
        status = "success" if result.returncode == 0 else "failed"
    except subprocess.TimeoutExpired as exc:
        output = (exc.stdout or "") if isinstance(exc.stdout, str) else ""
        error = f"timed out after {args.timeout}s"
        result = None
        status = "timeout"

    (ROOT / "output.txt").write_text(output or "Script ran but produced no output\n", encoding="utf-8")
    (ROOT / "exit_code.txt").write_text(str(0 if status == "success" else 1), encoding="utf-8")

    payload = {
        "status": status,
        "script": str(script.relative_to(ROOT)) if script.is_relative_to(ROOT) else str(script),
        "exit_code": 0 if status == "success" else 1,
        "duration_seconds": round(time.time() - started, 3),
        "output_chars": len(output),
    }
    if error:
        payload["error"] = error[-2000:]
    print(json.dumps(payload, ensure_ascii=False))

    if args.deliver:
        delivery = subprocess.run([sys.executable, str(ROOT / "send_output.py")], cwd=ROOT, text=True)
        if delivery.returncode != 0:
            return delivery.returncode
    return 0 if status == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
