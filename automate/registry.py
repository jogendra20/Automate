from __future__ import annotations

from .models import ToolSpec


TOOLS: dict[str, ToolSpec] = {
    "arxiv_recent": ToolSpec(
        name="arxiv_recent",
        description="Fetch recent arXiv CS.AI papers and optionally summarize them through Nexus.",
        script="scripts/arxiv_papers.py",
        tags=("research", "read-only", "arxiv"),
    ),
    "github_trending": ToolSpec(
        name="github_trending",
        description="Fetch the current GitHub Python trending repositories.",
        script="scripts/github_trending.py",
        tags=("github", "read-only", "trending"),
    ),
    "hackernews_top": ToolSpec(
        name="hackernews_top",
        description="Fetch the top Hacker News posts.",
        script="scripts/hn_top_posts.py",
        tags=("news", "read-only", "hackernews"),
    ),
    "leetcode_daily": ToolSpec(
        name="leetcode_daily",
        description="Fetch the current LeetCode daily challenge and optionally request coaching hints through Nexus.",
        script="scripts/leetcode_daily.py",
        tags=("coding", "read-only", "leetcode"),
    ),
}


def list_tools() -> list[ToolSpec]:
    return list(TOOLS.values())


def get_tool(name: str) -> ToolSpec:
    try:
        return TOOLS[name]
    except KeyError as exc:
        available = ", ".join(sorted(TOOLS))
        raise KeyError(f"Unknown tool {name!r}. Available tools: {available}") from exc
