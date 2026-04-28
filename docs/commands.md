# POC slash commands

Project-scoped slash commands for exercising the GitHub MCP server against `NguyenTanDung-2004/claude-poc`. All commands live in `.claude/commands/` and run only when this folder is the working directory.

Every command targets the same repo (`NguyenTanDung-2004/claude-poc`) and the same base branch (`main`) — these are hard-coded by design, since this is a single-repo POC. To retarget, edit the command files.

## Prerequisites

- The `github` MCP server is registered (user scope) and shows `✓ Connected` via `claude mcp list`.
- `mcp__github__*` tools are visible in the current session (a session started **before** registration won't see them — relaunch).
- The PAT in `/home/dungnguyen/.config/github-mcp/.env` (inside WSL) has `repo` scope.

See `CLAUDE.md` at the repo root for the full MCP runtime details.

## Commands

### `/poc-branch <name>`

Create a branch named `<name>` off `main`.

- **MCP tool**: `create_branch`
- **Args**: `<name>` — the new branch name (required).
- **Fails on**: branch already exists (no overwrite).

Example: `/poc-branch feature/hello`

---

### `/poc-commit <branch> <path> <message>`

Create or update one file on `<branch>`. The command will prompt you for the file content — it does not invent content.

- **MCP tool**: `create_or_update_file` (with `get_file_contents` for blob SHA when updating).
- **Args**: branch, path-in-repo, commit message (rest of the line).

Example: `/poc-commit feature/hello docs/hello.md add hello doc`

---

### `/poc-pr <branch> <title>`

Open a PR from `<branch>` → `main`.

- **MCP tool**: `create_pull_request` (with a `list_pull_requests` pre-check to avoid duplicates for the same head).
- **Args**: head branch, then PR title (rest of the line).

Example: `/poc-pr feature/hello Add hello doc`

---

### `/poc-status`

Read-only snapshot — lists up to 10 branches and 10 open PRs. Useful for sanity-checking what's on the repo before/after running the other commands.

- **MCP tools**: `list_branches`, `list_pull_requests`.
- **Args**: none.

---

### `/poc-mcp <action>`

Manage the local `github-mcp-server` Docker container. Actions:

| Action | What it does | Safety |
|---|---|---|
| `status` | Show registration, running container, image | read-only |
| `logs` | Tail last 50 lines of container stderr | read-only |
| `stop` | Kill the running container | ⚠️ breaks MCP for current session — needs confirm |
| `pull` | Pull latest image (takes effect next session) | network, needs confirm |
| `clean` | Prune stopped containers + dangling images | safe |

**`start` and `restart` aren't real actions** — Claude Code owns the container lifecycle. To restart: `/exit` this session and relaunch. To force a clean slate: `/poc-mcp stop` then exit + relaunch.

- **Tools**: `Bash`.
- **Args**: required action (one of the above).

---

### `/poc-doctor`

Health check of the MCP stack — Claude registration, WSL, Docker, image, PAT auth. Read-only; never writes to GitHub and never touches the env file. Run this **first** if any other `/poc-*` command fails unexpectedly (e.g. 403 on a write).

- **Tools**: `Bash`, `mcp__github__get_me`.
- **Args**: none.
- **Output**: per-step ✓/✗ lines and a one-line verdict.

---

### `/poc-flow <slug>`

End-to-end smoke test that chains the three write steps for a fresh `<slug>`:

1. branch `poc/<slug>` off `main`
2. commit `poc/<slug>.md` (one-line content)
3. open PR `POC: <slug>` → `main`

Stops at the first failing step. Use this to verify the whole MCP write path works after registering or restarting the server.

Example: `/poc-flow smoke-001`

## Adding a new command

1. Create `.claude/commands/<name>.md`.
2. Frontmatter: `description`, optional `argument-hint`, optional `allowed-tools` (restrict which MCP/Bash tools the command may invoke).
3. Body: prompt-style instructions referencing `$ARGUMENTS` (the full argument string).
4. Reload — the command appears under `/<name>` in the slash menu.

Keep new commands thin wrappers around individual MCP tools so failures are easy to localize. If a flow needs more than ~3 steps, prefer chaining slash commands over building one mega-command.
