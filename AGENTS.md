# Fantasy Store

## Context
Service of the **Crown & Trade** fantasy web game (users own heroes, heroes own items and
move between cities). This store handles **unique items** with limited quantity and
**auctions**. Users can only register, log in, buy or bid. It must be fully async to
handle spikes of ~1000 users buying the same item at once; concurrent bids must resolve to a
single winner, rejecting the others and informing them of the new value.

Consumed by `../rol-game` (Django backend, via `FANTASY_STORE_URL`) and `../crown-trade-front`.

## Technologies
- Python, FastAPI, Uvicorn (async)
- MongoDB via Motor (async) / PyMongo — schema-less items (weapon, armor, potion with different fields)
- pytest, pytest-asyncio, pytest-repeat
- Docker / docker-compose (port 8005)

## Architecture
Layered monolith with Hexagonal architecture (see `docs/architecture.md`):
- `src/domain/` — entities and ports
- `src/application/` — use cases
- `src/infrastructure/` — adapters (routes: users, items, auctions), Mongo repositories, auction scheduler
- `main.py` — FastAPI app, CORS, routers, auction refresh loop
- `tests/` — `unit/`, `integration/`, `e2e/` (e.g. `pytest -s tests/integration/test_item_service.py`)

## Business rules
Read `docs/BUSINESS_RULES.md` before changing game logic: it is the product source of truth (no technology, only business rules). The "Game rules" section is identical in all three repos — keep it so.

## Testing
Every time new code is written or existing code is changed, use the `testing` skill
(`.claude/skills/testing/SKILL.md`): add or update the tests in `tests/` (unit, integration,
e2e), run them, and fix the code and/or tests until the whole suite passes before calling the
work done.

## Trello task workflow
When the user asks to implement/develop/build/do a Trello task or card
("implement trello task {card title}"), run these steps in order, without waiting
for a new prompt between them. The same workflow is in the AGENTS.md of all three
repos; keep it identical. Each skill below exists in every repo with that repo's own
test commands: use the copy of the repo you are working in.

1. **Criteria and tests**: run the `write-tests` skill on the card. It writes the spec
   `docs/acceptance/<shortLink>-<name>.txt`, posts the criteria to the card as a
   checklist and a comment, writes the acceptance tests in every affected repo
   (failing for the right reason), adds the COVERAGE table and makes one local
   `test: add acceptance tests for <card name>` commit per repo, without pushing.
   If the spec and that commit already exist for the card, reuse them instead of
   rewriting them.
   - Stop and ask only if **CONFLICTS AND OPEN QUESTIONS** has anything other than
     "None". Those are product decisions. Continue once the user answers.
2. **Implement**: move the card to **Doing**, then run the `implement` skill
   with the spec: the card's PNG/ZIP attachments and the minimal code, backend repos
   first, until the task's tests pass. It never edits those tests.
3. **Verify**: run the `verify` skill on the spec. It judges the work without fixing
   it and gives a PASS/FAIL verdict per criterion.
   - On FAIL, run `implement` again with verify's **TO FIX** list, then
     `verify` again. After 2 failed rounds, stop and report.
4. **Update the card**: tick the `Acceptance criteria` checklist items whose
   criterion verify marked **PASS** (leave FAIL, NOT VERIFIED and MANUAL unticked),
   and add a comment with verify's verdict, criteria table and manual checks.
5. **Commit and push**, only if verify's verdict is **PASS**: every automated
   criterion PASS (none FAIL or NOT VERIFIED), test integrity PASS, and the full test
   suites, type check, lint and build of every repo you touched green.

   Then run the `commit-push` skill once per repo you touched, backend repos first
   and `crown-trade-front` last; the push includes the `test:` commit from step 1.
   For this workflow, the user's request is the confirmation to commit and push:
   don't ask again.
   If any condition is false, don't commit or push. Report what fails or couldn't be
   verified and what is needed, and leave the card in **Doing**.
6. **Report**: give the `implement` summary and the `verify` verdict, add the
   commit hash and branch pushed for each repo, and list the manual checks left for
   the human. Then ask whether to move the card to **Done**.

**Trello attachments**: the user-level `~/.claude/settings.json` sets the env vars
`TRELLO_API_KEY` and `TRELLO_TOKEN`. The Trello MCP only lists a card's attachments
(`trelloReadCard`, `action: "list_attachments"`); use these vars to download them into
`.trello-attachments/<shortLink>/` instead of asking the user:
`curl -sL -H "Authorization: OAuth oauth_consumer_key=\"$TRELLO_API_KEY\", oauth_token=\"$TRELLO_TOKEN\"" "<attachment url>" -o .trello-attachments/<shortLink>/<file>`.
Never print, echo or commit their values.

Never use `--force` or `--no-verify`, and never commit secrets or `.trello-attachments/`.
