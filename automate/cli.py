from __future__ import annotations

import argparse
import json

from .registry import list_tools
from .runner import run_tool


def main() -> int:
    parser = argparse.ArgumentParser(prog="automate")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("tools", help="list registered tools")
    run = sub.add_parser("run", help="run a registered tool")
    run.add_argument("name")
    run.add_argument("--timeout", type=int)
    args = parser.parse_args()

    if args.command == "tools":
        print(json.dumps([tool.to_dict() for tool in list_tools()], indent=2))
        return 0

    result = run_tool(args.name, timeout=args.timeout)
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    return 0 if result.status == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
