---
description: Manage the github-mcp-server Docker container — status, logs, stop, pull, clean
argument-hint: <status|logs|stop|pull|clean>
allowed-tools: Bash
---

Run a lifecycle operation on the local `ghcr.io/github/github-mcp-server` container that backs the `github` MCP server. Argument: `$ARGUMENTS` selects the action.

If `$ARGUMENTS` is empty or not one of the known actions, list the actions below and stop. Do not guess.

**Hard rule:** never read, ls, stat, cat, or `docker inspect` anything that reveals the contents of `/home/dungnguyen/.config/github-mcp/.env` or the container's `GITHUB_PERSONAL_ACCESS_TOKEN` env var. If an action would expose them, redact or skip the field.

**Lifecycle reality:** The container is spawned by Claude Code itself at session startup (`docker run -i --rm`) and its stdio is owned by this process. There is no useful `start` or `restart` from inside Claude Code — to restart, the user must exit and relaunch the session, which respawns the container with a fresh env load. Surface this when asked.

## Actions

### `status`
Report a 3-line snapshot:
1. Registration: parse `claude mcp list` for the `github:` line — show ✓/✗ Connected.
2. Container: `wsl -d Ubuntu -- docker ps --filter ancestor=ghcr.io/github/github-mcp-server --format 'table {{.ID}}\t{{.Status}}\t{{.RunningFor}}'`.
3. Image: `wsl -d Ubuntu -- docker images --format '{{.Repository}}:{{.Tag}}\t{{.CreatedSince}}\t{{.Size}}' ghcr.io/github/github-mcp-server`.

### `logs`
Find the running container ID with `wsl -d Ubuntu -- docker ps -q --filter ancestor=ghcr.io/github/github-mcp-server`. If empty, report "no running container" and stop. Otherwise, show the last 50 lines: `wsl -d Ubuntu -- docker logs --tail 50 <id>`. Note: MCP servers log to stderr; stdout is the JSON-RPC stream and will look like noise — that's expected.

### `stop` ⚠️ destructive
**Confirm with the user first.** This kills the container the current Claude Code session is talking to — `mcp__github__*` tools will fail until the session is relaunched. State this explicitly and wait for a yes.

On confirmation:
- Find the container ID as above.
- `wsl -d Ubuntu -- docker kill <id>` (faster than `stop`; the MCP server has no shutdown work to flush).
- Remind the user to `/exit` and relaunch Claude Code to get MCP back.

### `pull`
**Confirm with the user first** (network op, can take a minute, also pulls a new image that will be used by the *next* session — does not affect the running container).

`wsl -d Ubuntu -- docker pull ghcr.io/github/github-mcp-server`. After it completes, report the new image digest and remind the user that the change only takes effect after relaunching Claude Code.

### `clean`
Prune dangling resources tied to this image. Two steps, both safe:
1. `wsl -d Ubuntu -- docker container prune -f --filter 'label=org.opencontainers.image.source=https://github.com/github/github-mcp-server'` (removes stopped containers from this image).
2. `wsl -d Ubuntu -- docker image prune -f` (removes dangling images — only `<none>` tagged ones, never named images in use).

Report what was reclaimed. Does NOT touch the running container or the `:latest` tag.

### `restart` / `start` (informational only)
If the user asks for these: explain that Claude Code owns the container lifecycle. To restart: `/exit` this session and relaunch — the next session spawns a fresh container with the current env file. To force a clean slate: run `/poc-mcp stop` first, then exit + relaunch.

## Output

Match the action: `status` → 3-line table; `logs` → raw tail; `stop`/`pull` → action confirmation + next step. Keep all output under ~15 lines.
