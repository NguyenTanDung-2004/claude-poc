---
description: Create or update a single file on a branch of claude-poc
argument-hint: <branch> <path> <commit-message>
allowed-tools: mcp__github__create_or_update_file, mcp__github__get_file_contents
---

Create or update one file on `NguyenTanDung-2004/claude-poc`. Arguments in `$ARGUMENTS`:

- First whitespace-separated token = branch name
- Second token = file path in the repo
- Remainder = commit message (may contain spaces)

Steps:
1. Parse `$ARGUMENTS` into `branch`, `path`, `message`. If any are missing, ask the user.
2. Ask the user for the file content (do NOT invent content).
3. Call `mcp__github__create_or_update_file` with `owner=NguyenTanDung-2004`, `repo=claude-poc`, `branch`, `path`, `message`, `content`.
4. Report the resulting commit SHA and a link to the file on that branch.

If the file already exists on the branch, the MCP tool requires the existing blob SHA — fetch it via `mcp__github__get_file_contents` first and pass it through.
