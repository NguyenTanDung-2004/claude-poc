---
description: Open a PR from a branch into main on claude-poc
argument-hint: <branch> <title>
allowed-tools: mcp__github__create_pull_request, mcp__github__list_pull_requests
---

Open a pull request on `NguyenTanDung-2004/claude-poc` from the given branch into `main`. Arguments in `$ARGUMENTS`:

- First whitespace-separated token = head branch
- Remainder = PR title

Steps:
1. Parse `$ARGUMENTS` into `head` and `title`. If either is missing, ask.
2. Before opening, call `mcp__github__list_pull_requests` with `head=NguyenTanDung-2004:<head>` and `state=open` to confirm no PR already exists for this branch. If one exists, surface its number/URL and stop.
3. Call `mcp__github__create_pull_request` with `owner=NguyenTanDung-2004`, `repo=claude-poc`, `head`, `base=main`, `title`, and a short auto-generated body summarizing the head branch's diff against main (use `mcp__github__list_commits` if useful).
4. Return the PR number and URL.
