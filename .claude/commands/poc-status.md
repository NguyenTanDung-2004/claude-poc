---
description: Show open branches and PRs on claude-poc
allowed-tools: mcp__github__list_branches, mcp__github__list_pull_requests
---

Give a quick read-only snapshot of `NguyenTanDung-2004/claude-poc`:

1. Call `mcp__github__list_branches` (owner `NguyenTanDung-2004`, repo `claude-poc`, `perPage=10`) and list the branches with their head SHAs.
2. Call `mcp__github__list_pull_requests` (same repo, `state=open`, `perPage=10`) and list each open PR's number, title, head→base, and author.

Format as two short markdown sections: **Branches** and **Open PRs**. No other commentary.
