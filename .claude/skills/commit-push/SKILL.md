---
name: commit-push
description: Review the current code changes, write a typed commit message (feat, fix or bug) from them, then commit and push to the remote. Use when the user asks to commit, push, or "commit and push" their work.
model: claude-haiku-5-5
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Bash(git branch:*), Bash(git rev-parse:*)
---

# Commit and push

## 1. Gather context
Run these in parallel:
- `git status --short`
- `git diff HEAD` (staged and unstaged changes)
- `git log --oneline -5` (to match the repo's message style)
- `git rev-parse --abbrev-ref HEAD` (current branch)

If there are no changes, say "Nothing to commit." and stop.

Never stage `.env`, `.env.*`, keystores, credentials or other secrets. If any of them show up as changed, leave them out and mention it in one line.

## 2. Choose the commit type
Read the diff and pick exactly one type:

| Type    | Use when the change...                                                  |
|---------|-------------------------------------------------------------------------|
| `feat`  | adds new functionality, a screen, an endpoint, a model or a game system |
| `fix`   | adjusts or improves existing behavior (tweaks, styling, config, refactors, small corrections) |
| `bug`   | repairs a defect that made something crash or behave wrongly            |

If the changes mix types, pick the one that covers most of the change.

## 3. Write the message
Format:

```
<type>: <short summary in imperative mood, lowercase, max ~72 chars>

<optional body: 1-4 bullet lines on what changed and why, only if the summary isn't enough>

Co-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>
```

Describe what the change does for the app (e.g. `feat: add hero travel between cities`), not the files touched.

## 4. Commit and push
1. Stage the relevant files: `git add <paths>` (or `git add -A` if every change belongs to the commit and none are secrets).
2. Commit using a HEREDOC so formatting is preserved:
   ```
   git commit -m "$(cat <<'EOF'
   <message>
   EOF
   )"
   ```
3. Push: `git push`. If the branch has no upstream, run `git push -u origin <branch>`.

Never use `--force`, `--no-verify` or amend existing commits unless the user asks.

## 5. Report
Reply with one line: the commit hash, the message summary, and the branch pushed to. If a hook or the push fails, report what failed and why in one line, and don't retry with bypass flags.
