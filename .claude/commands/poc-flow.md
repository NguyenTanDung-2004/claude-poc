---
description: End-to-end smoke test — branch, commit a sample file, open PR
argument-hint: <slug>
allowed-tools: mcp__github__create_branch, mcp__github__create_or_update_file, mcp__github__create_pull_request
---

Run the full create-branch → commit → open-PR flow on `NguyenTanDung-2004/claude-poc` as a smoke test for the GitHub MCP server. Argument: `$ARGUMENTS` is a slug used to name the branch, file, and PR.

If `$ARGUMENTS` is empty, ask for a slug before doing anything.

Steps:
1. **Branch**: `mcp__github__create_branch` → `branch=poc/<slug>`, `from_branch=main`.
2. **Commit**: `mcp__github__create_or_update_file` → `path=poc/<slug>.md`, `message=poc: add <slug> sample`, `content` = a one-line markdown file: `# <slug>\n\nSmoke test from Claude Code via GitHub MCP on <today's date>.\n`.
3. **PR**: `mcp__github__create_pull_request` → `head=poc/<slug>`, `base=main`, `title=POC: <slug>`, `body=Automated smoke test of the create-branch → commit → PR flow via the github-mcp-server (Docker, WSL).`.
4. Stop after each step if it errors — do NOT continue past a failure. Report which step failed and the raw MCP error.
5. On success, return: branch URL, commit SHA, PR URL.
