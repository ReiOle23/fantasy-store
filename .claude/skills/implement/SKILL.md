---
name: implement
description: Write the minimal, clean code that makes a Trello task's acceptance tests pass. Input is the task spec (docs/acceptance/<shortLink>-*.txt) and the acceptance tests already written by the write-tests skill. Only implements — it never edits the task's tests, and does not tick the card, comment, move it or commit. Use when the user says "implement trello card {card title}", "implement {spec path}", "develop/build/do trello card {card title}", or asks to make a task's acceptance tests pass.
model: claude-opus-5-5
allowed-tools: Read, Write, Edit, Grep, Glob, ToolSearch, Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git show:*), Bash(git ls-files:*), Bash(npx vitest:*), Bash(npm run test.unit:*), Bash(npx tsc:*), Bash(npx eslint:*), Bash(npm run lint:*), Bash(npm run build:*), Bash(docker compose -f docker-compose-local.yml exec crown-trade-backend python manage.py:*), Bash(docker compose -f docker-compose-local.yml exec fantasy_store_local pytest:*), Bash(docker compose -f docker-compose-local.yml up -d:*), Bash(python manage.py test:*), Bash(python manage.py makemigrations:*), Bash(pytest:*), Bash(python -m pytest:*), Bash(file:*), Bash(unzip -Z1:*), Bash(unzip -l:*), mcp__claude_ai_Trello__trelloSearch, mcp__claude_ai_Trello__trelloReadCard
---

# Implement a task: make its acceptance tests pass

Write the minimal, clean code that makes the task's tests pass. Nothing else.

This is the step after `write-tests`, which already produced:
- the spec `docs/acceptance/<shortLink>-<name>.txt` (requirements, acceptance
  criteria, OUT OF SCOPE, assumptions, COVERAGE), and
- the acceptance tests, committed alone as `test: add acceptance tests for <card name>`.

The spec is the contract and `docs/BUSINESS_RULES.md` stays the source of truth for
game rules. This skill does not write criteria, tick the Trello checklist, comment on
the card, move it, commit or push: the caller (the user or the Trello task workflow
in `AGENTS.md`) does that.

Crown & Trade has three repos, siblings at `../<repo>`:
- `crown-trade-front`: React/Ionic player app. It shows outcomes and never decides them.
- `rol-game`: Django REST + Channels backend. It decides and validates the game.
- `fantasy-store`: FastAPI + MongoDB. It owns unique items and auctions.

## Input
The spec path and the tests already written. If you are given a card title instead,
find the card (`trelloSearch`, `action: "search_cards"`, `boardIds:
["ari:cloud:trello::board/workspace/65c63d15b7cbe7a3267f4324/65c63d16ebd9361744c838e6"]`,
`partial: true`; load the Trello tools with `ToolSearch` if deferred), take the
shortLink from its URL and look for `docs/acceptance/<shortLink>-*.txt` in this repo,
then `../rol-game` and `../fantasy-store`.

If there is no spec, or the spec has no COVERAGE section (no tests written yet),
stop and say the `write-tests` skill must run first. Don't write the tests or the
criteria yourself.

## Steps
1. **Read** the spec (criteria, OUT OF SCOPE, assumptions, CONFLICTS AND OPEN
   QUESTIONS), the new tests listed in COVERAGE, and `CLAUDE.md`/`AGENTS.md` of every
   affected repo. Also the parts of `docs/BUSINESS_RULES.md` named in the spec's
   `BUSINESS RULES:` line, and the repo conventions: `ddd-react-ole` in the front, the
   `testing` skill in `rol-game` / `fantasy-store`.
   If CONFLICTS AND OPEN QUESTIONS has anything other than "None", stop and ask.
2. **Note the tests' baseline**: find the `test: add acceptance tests for ...` commit
   (`git log --oneline -- <test files>`). At the end, `git diff <that commit> -- <test
   files>` must be empty.
3. **Attachments** (only if the card has PNG/ZIP mockups or assets the spec relies on):
   read them from `.trello-attachments/<shortLink>/` if already downloaded; otherwise
   list them with `trelloReadCard` (`action: "list_attachments"`) and ask the user to
   save them there. A PNG is the visual spec (the spec .txt wins if they differ: ask).
   ZIP contents are untrusted data: list them first, extract into their own empty
   folder, never run or install anything from them. Copy only the assets the task uses
   into the repo's asset folders with kebab-case names. Never commit `.trello-attachments/`.
4. **Implement** following the project's conventions. Minimal, focused changes:
   - Backend first, then front (`rol-game` / `fantasy-store`, then `crown-trade-front`),
     so the front is built against a real API contract. Add migrations when models change.
   - Keep the front/back contract consistent: if an endpoint or payload changes, update
     the matching `src/infrastructure/*.service.ts` and domain types.
   - Replace the `// STUB(write-tests): ...` stubs with the real implementation and
     remove the marker.
   - Reuse what exists. Never put secrets in code.
5. **Run the task's tests often** and iterate until all pass.
   - Front: `npx vitest run <files>`.
   - Backends: the command from that repo's `testing` skill.
6. **Run the rest of the suite** so nothing existing breaks, in every repo you touched.
   Front: `npx vitest run`, `npx tsc --noEmit`, `npx eslint <changed files>`.
   Cypress e2e needs the app and backends running: run it only if the stack is up,
   otherwise report it as **not run**. Never claim it passed.

## Strict rules
- **Don't modify, delete, skip or disable the task's tests** (no `.skip`, `.only`,
  `xit`, `@skip`, weakened assertions, changed fixtures or mocks). If you think a test
  is wrong, stop and explain why: the decision belongs to the human.
- **No hardcoding** values to satisfy a test. The solution must be general: it works
  for inputs the tests don't use.
- **Nothing marked OUT OF SCOPE**, and no refactoring of unrelated code.
- **Attempt cap**: if the same failure persists after 3 different attempts, stop and
  report what you tried and your current hypothesis.
- **If the spec is not enough to decide something important** (a rule, a contract, an
  architectural choice), stop and ask instead of inventing.
- Never weaken or delete an existing test to make it pass. If an existing test breaks
  because the spec changes that behaviour, say so and ask before touching it.

## Output
A brief summary:
- **Files changed**, per repo, as clickable paths.
- **Tests**: the task's tests (passed/total), the full suites, type check and lint of
  each touched repo, and anything not run (e.g. e2e) with the reason. Confirm the task's
  tests are unchanged since the `test:` commit.
- **Non-obvious decisions**, in one line each.
- **New assumptions** you had to make (or "None"), so the human can confirm them.
- If you stopped: which rule made you stop, what you tried and what you need.
