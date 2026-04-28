---
description: Create a branch off main on NguyenTanDung-2004/claude-poc
argument-hint: <branch-name>
allowed-tools: mcp__github__create_branch, mcp__github__list_branches
---

Create a new branch named `$ARGUMENTS` on the GitHub repo `NguyenTanDung-2004/claude-poc`, branched from `main`.

Steps:
1. Call `mcp__github__create_branch` with `owner=NguyenTanDung-2004`, `repo=claude-poc`, `branch=$ARGUMENTS`, `from_branch=main`.
2. Report the new branch name and the commit SHA it points at.
3. If the branch already exists, do NOT overwrite — surface the conflict and stop.

If `$ARGUMENTS` is empty, ask the user for a branch name before doing anything.
