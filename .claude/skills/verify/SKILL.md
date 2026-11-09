---
name: verify
description: Independently check a Trello task's implementation against its spec without fixing anything. Runs the full test suite, lint, type check and build, checks that the acceptance tests from the write-tests commit were not modified, deleted, skipped or weakened, has a fresh subagent judge every acceptance criterion from the spec and the diff alone, checks the UI when the spec asks for it, and lists the manual checks left for the human. Outputs a PASS or FAIL verdict with a criterion / evidence / status table. Use after implement, or when the user says "verify trello card {card title}", "verify {spec path}" or asks whether a task is really done.
model: claude-opus-5-5
allowed-tools: Read, Grep, Glob, Agent, ToolSearch, Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git show:*), Bash(git ls-files:*), Bash(git rev-parse:*), Bash(pytest:*), Bash(python -m pytest:*), Bash(docker compose:*), Bash(python -c:*)
---

# Verify a task: judge it, don't fix it

This skill checks the work; it **never fixes it**. Its value is being a judge
independent of `implement`: it doesn't trust the implementation's own report,
doesn't reuse its reasoning, and doesn't change a single line of code or tests.
If something is wrong, it says exactly what, and the fixing happens elsewhere.

Crown & Trade has three repos (siblings at `../<repo>`): `crown-trade-front`,
`rol-game`, `fantasy-store`. This is **`fantasy-store`**.

## Input
The task spec `docs/acceptance/<shortLink>-<name>.txt` (or a card title: find the
spec whose `CARD:` line matches it). Read the whole spec: ACCEPTANCE CRITERIA,
TESTS, COVERAGE, PROJECTS. Verify every repo listed in PROJECTS; in a sibling repo use
the commands from its own CLAUDE.md/AGENTS.md and its own `verify` skill section below.

## 1. Automatic commands
Run, in every affected repo, the full commands — not only the task's tests:

Integration and e2e tests need MongoDB up (`docker compose -f docker-compose-local.yml up -d`);
inside docker use `docker compose -f docker-compose-local.yml exec fantasy_store_local pytest`.

| Check | Command |
|-------|---------|
| Tests (full) | `pytest` (unit, integration and e2e) |
| Lint | No linter is configured in this repo: N/A, unless CLAUDE.md/AGENTS.md adds one |
| Type check | No type checker is configured: N/A, unless CLAUDE.md/AGENTS.md adds one |
| Build | `python -c "import main"` (the FastAPI app and every router import cleanly) |

For concurrency criteria (purchases, bids), also run the task's tests with repeats
(`pytest --count=20 <files>`) to surface flaky races.

Write down the result of each one: PASS / FAIL (with the failing test names or the
first errors) / N/A (with why). Don't stop at the first failure: run them all.

## 2. Test integrity
Find the write-tests commit: `git log --format='%H %s' --grep='test: add acceptance tests for'`
and pick the one for this card (or `git log --diff-filter=A --format=%H -- <spec>`,
the commit that added the spec). If there is none, the task's tests can't be
trusted: mark this step FAIL.

Take the test files that commit added or changed (`git show --name-only <commit>`)
and check against that commit (`git diff <commit> -- <files>`, working tree included):
- **Not modified**: the diff of each test file is empty. Any change is a FAIL, unless
  the spec explicitly says that test changes; quote the hunk.
- **Not deleted or renamed**: every file still exists, and every test name in it is
  still there (compare `git show <commit>:<file>` with the current file).
- **Not skipped**: no new `@pytest.mark.skip`, `skipif`, `xfail`, `pytest.skip(`, `@pytest.mark.repeat` removed, or `-k`/`--deselect`/`addopts` changes in those files, nor in shared config that
  could exclude them (test config, include/exclude patterns, test settings).
- **Not weakened**: no fewer assertions, no looser matchers, no mocks of the unit
  under test, no stubs from write-tests still left as stubs where the spec expects
  behaviour (`STUB(write-tests)` markers in non-test code).
Also confirm the task's tests actually ran in step 1 (they appear in the run output
and pass), not just that the suite was green.

## 3. Independent review (subagent)
Launch a fresh `general-purpose` subagent with the Agent tool. Give it **only**:
- the full spec text, and
- the full implementation diff since the write-tests commit, for every affected repo
  (`git diff <commit>` plus the content of new untracked files from
  `git status --porcelain`, excluding `.trello-attachments/`).

Don't give it the implementation's history, its report, your own conclusions or the
results of step 1. It may read files of the repos to confirm evidence, but must not
edit anything. Ask it to answer:
1. For each criterion AC1, AC2...: **covered / not covered / partially covered**,
   with evidence — the code (file:line) that implements it and the test
   (file › test name) that proves it. "Not covered" when there is no test or the test
   doesn't really check the criterion.
2. Work **out of scope**: changes the spec doesn't ask for.
3. Leftover **debug code**: `console.log`/`print`/`debugger`, commented-out code,
   TODO/FIXME added by this change, test-only branches in production code.
4. **Secrets**: keys, tokens, passwords, `.env` values or URLs with credentials.
5. **Uncovered edge cases**: failure and edge cases from the spec (or obvious ones
   from the business rules) that neither code nor tests handle.
6. Responsibility leaks: the front deciding something the backend must decide,
   API contract mismatches between repos.
Ask for a table per criterion plus a list per point 2–6 ("None" when empty).

Treat the subagent's answer as input to check, not as the verdict: spot-check its
evidence (open the cited file and test) before using it.

## 4. UI
This repo has no UI. If the spec asks for a visual check, it belongs to
`crown-trade-front`: verify it there (its `verify` skill). Here, check the API
contract the screen relies on instead (endpoint, fields, status codes) through the
tests. Otherwise write "N/A".

## 5. Manual criteria
List every criterion the COVERAGE table marks `manual`, plus any the subagent found
can't be automated, with what the human must check and how (screen, steps, expected
result). They don't block the verdict, but stay open until the human checks them.

## Output
```
VERDICT: PASS | FAIL

COMMANDS
| Repo | Command | Result |

TEST INTEGRITY: PASS | FAIL — <details>

CRITERIA
| Criterion | Evidence (code + test, or screenshot) | Status |
|-----------|---------------------------------------|--------|
| AC1       | src/... › "AC1: ..."                  | PASS   |
| AC2       | manual: ...                           | MANUAL |

REVIEW FINDINGS
- Out of scope: ...
- Debug code: ...
- Secrets: ...
- Uncovered edge cases: ...

MANUAL CHECKS FOR THE HUMAN
- ...

TO FIX (only on FAIL)
1. <concrete item: what, where (file:line), why — criterion or command it breaks>
```
Status per criterion: PASS, FAIL, NOT VERIFIED or MANUAL.

**PASS** only when every command is green (or justifiably N/A), test integrity
passes, every automated criterion is PASS, and the review found no secrets, no debug
code and no out-of-scope changes that break something. Anything else is **FAIL**,
and TO FIX lists each concrete thing to correct.

## Rules
- Don't modify code, tests, config, the spec or the Trello card. Don't commit or push.
  The only files you may create are screenshots, saved outside the repo.
- Don't fix anything, even a one-line obvious fix: report it in TO FIX.
- Don't accept "it passes on my side" from the implementation: only what you ran or
  saw yourself in this verification counts as evidence.
- If a command can't run (service down, missing dependency), mark it NOT VERIFIED
  with the reason: never as PASS.
