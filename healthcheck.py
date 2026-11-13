"""Check Nexus configuration and the /ask endpoint without printing secrets."""
from __future__ import annotations

import json
import sys
from nexus_client import NexusClient, NexusError


def main() -> int:
    try:
        client = NexusClient.from_env()
        response = client.ask("Health check. Reply with the single word OK.", task="healthcheck")
        print(json.dumps({"status": "healthy", "ask_response_chars": len(response)}))
        return 0
    except NexusError as exc:
        print(json.dumps({"status": "unhealthy", "error": str(exc)}))
        return 1
    except Exception as exc:
        print(json.dumps({"status": "unhealthy", "error": f"unexpected error: {exc}"}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
