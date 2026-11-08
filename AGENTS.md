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
repos; keep it identical.

1. **Acceptance criteria**: run the `trello-acceptance-criteria` skill on the card.
   If the acceptance file already exists for that card, reuse it instead of rewriting it.
   - Stop and ask only if **CONFLICTS AND OPEN QUESTIONS** has anything other than
     "None". Those are product decisions. Continue once the user answers.
2. **Implement**: run the `trello-implement` skill: the card's PNG/ZIP attachments,
   code, tests in every affected repo, the checklist ticks and the result comment.
3. **Commit and push**, only if all of this is true:
   - every acceptance criterion is **PASS** (none FAIL or NOT VERIFIED), and
   - the full test suites, type check and lint of every repo you touched are green.

   Then run the `commit-push` skill once per repo you touched, backend repos first
   and `crown-trade-front` last. For this workflow, the user's request is the
   confirmation to commit and push: don't ask again.
   If any condition is false, don't commit or push. Report what fails or couldn't be
   verified and what is needed, and leave the card in **Doing**.
4. **Report**: give the `trello-implement` final report and add the commit hash and
   branch pushed for each repo. Then ask whether to move the card to **Done**.

Never use `--force` or `--no-verify`, and never commit secrets or `.trello-attachments/`.
