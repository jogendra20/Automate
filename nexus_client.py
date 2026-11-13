"""Small, dependency-light client for the Nexus HTTP API.

The client intentionally fails loudly on authentication, HTTP, timeout, and
malformed-response errors so an automation run cannot be reported as healthy
when Nexus is unavailable.
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class NexusError(RuntimeError):
    """Base class for Nexus integration errors."""


class NexusConfigurationError(NexusError):
    """Raised when required Nexus configuration is missing or invalid."""


class NexusHTTPError(NexusError):
    """Raised when Nexus returns a non-success HTTP response."""

    def __init__(self, status: int, message: str):
        super().__init__(f"Nexus HTTP {status}: {message}")
        self.status = status
        self.message = message


@dataclass(frozen=True)
class NexusConfig:
    base_url: str
    api_key: str
    timeout: float = 30.0
    retries: int = 2

    @classmethod
    def from_env(cls) -> "NexusConfig":
        base_url = os.environ.get("NEXUS_URL", "").strip().rstrip("/")
        api_key = os.environ.get("NEXUS_API_KEY", "").strip()
        if not base_url:
            raise NexusConfigurationError("NEXUS_URL is missing")
        if not api_key:
            raise NexusConfigurationError("NEXUS_API_KEY is missing")
        if not base_url.startswith(("http://", "https://")):
            raise NexusConfigurationError("NEXUS_URL must start with http:// or https://")
        return cls(
            base_url=base_url,
            api_key=api_key,
            timeout=float(os.environ.get("NEXUS_TIMEOUT", "30")),
            retries=max(0, int(os.environ.get("NEXUS_RETRIES", "2"))),
        )


class NexusClient:
    def __init__(self, config: NexusConfig):
        self.config = config

    @classmethod
    def from_env(cls) -> "NexusClient":
        return cls(NexusConfig.from_env())

    def request_json(self, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        endpoint = "/" + endpoint.lstrip("/")
        body = json.dumps(payload).encode("utf-8")
        request = Request(
            self.config.base_url + endpoint,
            data=body,
            method="POST",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "X-API-Key": self.config.api_key,
                "User-Agent": "automate-nexus-client/1.0",
            },
        )
        last_error: Exception | None = None
        for attempt in range(self.config.retries + 1):
            try:
                with urlopen(request, timeout=self.config.timeout) as response:
                    raw = response.read().decode("utf-8")
                    try:
                        data = json.loads(raw) if raw else {}
                    except json.JSONDecodeError as exc:
                        raise NexusError(f"Nexus returned invalid JSON: {exc}") from exc
                    if not isinstance(data, dict):
                        raise NexusError("Nexus response must be a JSON object")
                    return data
            except HTTPError as exc:
                detail = exc.read().decode("utf-8", errors="replace")[:500]
                if exc.code in (401, 403):
                    raise NexusHTTPError(exc.code, "authentication or permission failed") from exc
                if exc.code not in (408, 429) and exc.code < 500:
                    raise NexusHTTPError(exc.code, detail or "request rejected") from exc
                last_error = NexusHTTPError(exc.code, detail or "temporary server error")
            except (URLError, TimeoutError, OSError) as exc:
                last_error = NexusError(f"Nexus connection failed: {exc}")
            if attempt < self.config.retries:
                time.sleep(2**attempt)
        raise last_error or NexusError("Nexus request failed")

    def ask(self, prompt: str, task: str = "ask") -> str:
        result = self.request_json("ask", {"prompt": prompt, "task": task})
        response = result.get("response")
        if not isinstance(response, str) or not response.strip():
            raise NexusError("Nexus /ask response did not contain a non-empty 'response'")
        return response

    def store_output(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.request_json("store-output", payload)

    def store_skill_proposal(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.request_json("store-skill-proposal", payload)
