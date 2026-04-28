## What this directory is

`MCP_POC` is **not a software project** — it has no source files, build, or tests. It is a working directory used to exercise the **GitHub MCP server** (official `ghcr.io/github/github-mcp-server`, run locally via Docker in WSL Ubuntu) from Claude Code on Windows. The goal is to drive create-branch / commit / open-PR flows through the `mcp__github__*` tools.

If you're asked to "build", "test", or "run" something here, push back — there is nothing to build. The work happens *against a remote GitHub repo* via MCP tools.

## Target repository for write operations

All write operations (branches, commits, PRs, issues) default to **`NguyenTanDung-2004/claude-poc`** (https://github.com/NguyenTanDung-2004/claude-poc). Do not operate on other repos without explicit confirmation from the user.

Read-only calls (`get_me`, `list_*`, `search_*`) against other repos are fine when the user asks.

## MCP server runtime

The `github` MCP server is registered at **user scope** (in `~/.claude.json`), launched as:

```
wsl -d Ubuntu -- docker run -i --rm --env-file /home/dungnguyen/.config/github-mcp/.env ghcr.io/github/github-mcp-server
```

- The PAT lives in `/home/dungnguyen/.config/github-mcp/.env` **inside WSL** (mode 600, single line `GITHUB_PERSONAL_ACCESS_TOKEN=...`). To rotate, edit that file — no Claude Code reconfiguration needed.
- Verify the server is up with `claude mcp list` (expect `github: … ✓ Connected`).
- After (re)registering the server, `mcp__github__*` tools only appear in **new** Claude Code sessions. The registering session must exit and relaunch.

## Operational rules learned from prior sessions

- **Never paste the PAT value back into chat.** A previous PAT was leaked into chat and had to be revoked. Refer to the env-file location instead. If you need to see the token, ask the user to read it themselves.
- **Git Bash path-translation gotcha:** when running `claude mcp add` from Git Bash on Windows, any arg starting with `/` (e.g. `/home/dungnguyen/...`) gets MSYS-rewritten to `C:/Program Files/Git/home/...`. Prefix with `MSYS_NO_PATHCONV=1`, or run from PowerShell/cmd. Re-add command:
  ```
  MSYS_NO_PATHCONV=1 claude mcp add github -s user -- wsl -d Ubuntu -- docker run -i --rm --env-file /home/dungnguyen/.config/github-mcp/.env ghcr.io/github/github-mcp-server
  ```
- **Local Docker, not remote MCP** — the user explicitly chose this over the hosted GitHub MCP. Don't suggest switching to the remote server.

## Tool selection

Prefer `mcp__github__*` tools over shelling out to `gh` for this POC — the whole point is to exercise MCP. `gh` is acceptable as a fallback only if an MCP tool is missing or behaving incorrectly, and flag the discrepancy when you do.

## Slash commands

Project-scoped commands live in `.claude/commands/` (`/poc-branch`, `/poc-commit`, `/poc-pr`, `/poc-status`, `/poc-flow`). Full reference: `docs/commands.md`. They are thin wrappers around single MCP calls — prefer extending them over building larger commands.
