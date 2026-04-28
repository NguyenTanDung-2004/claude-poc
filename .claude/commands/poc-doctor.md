---
description: Diagnose the GitHub MCP server — connectivity, WSL/Docker, image, PAT auth
allowed-tools: Bash, mcp__github__get_me
---

Run a top-to-bottom health check of the GitHub MCP server stack and report what's broken (if anything). Do NOT attempt to write to GitHub.

**Hard rule:** never touch `/home/dungnguyen/.config/github-mcp/.env` (no `cat`, `ls`, `stat`, `head`, etc.) — not even metadata. Steps 1 and 5 below give indirect proof that the env file is functional; if either fails for a reason that *might* be the env file, ask the user to inspect it themselves.

Run the checks **in order** and stop reporting individual successes — only call out failures and the one-line remediation. Each check that passes can be a single ✓ line.

## Checks

1. **Claude knows the server.** Run `claude mcp list`. Expect a line `github: … ✓ Connected`.
   - If absent: server isn't registered. Re-register per `CLAUDE.md` (`MSYS_NO_PATHCONV=1 claude mcp add github -s user -- wsl -d Ubuntu -- docker run -i --rm --env-file /home/dungnguyen/.config/github-mcp/.env ghcr.io/github/github-mcp-server`) and tell the user to relaunch the session.
   - If present but `✗ Failed to connect`: continue with the lower-level checks below to find the cause.

2. **WSL distro is reachable.** Run `wsl -d Ubuntu -- echo ping`. This also wakes the distro if it was stopped.
   - If it fails: report the error verbatim. Likely WSL is not installed or the `Ubuntu` distro doesn't exist (`wsl -l -v` to confirm).

3. **Docker daemon responds inside WSL.** Run `wsl -d Ubuntu -- docker info --format '{{.ServerVersion}}'`.
   - If it fails: Docker isn't running. Tell the user to start Docker Desktop on Windows (most common setup) or `sudo service docker start` inside WSL. Do NOT attempt sudo automatically.

4. **MCP image is present locally.** Run `wsl -d Ubuntu -- docker images --format '{{.Repository}}:{{.Tag}}' ghcr.io/github/github-mcp-server`.
   - If empty: pull it with `wsl -d Ubuntu -- docker pull ghcr.io/github/github-mcp-server` (this is safe — confirm with user first since it's a network op that can take a minute).

5. **PAT authenticates.** Call `mcp__github__get_me` and report the `login` and `name`.
   - If it errors with 401: token is invalid or expired. Ask the user to rotate it (do NOT touch the env file yourself).
   - If `login` is not `NguyenTanDung-2004`: warn that the token belongs to a different account, which means write ops on `claude-poc` will likely 403 unless that account is a collaborator.

## Output

End with a single-line verdict:
- `✅ All checks passed — MCP write path should work.`
- `⚠️  <N> warning(s) — see above.` (e.g. wrong account, image missing)
- `❌ Blocked at step <N>: <one-sentence summary>.` (any hard failure)

Keep the whole report under ~20 lines. No prose explanations — the user wants a status board, not an essay.
