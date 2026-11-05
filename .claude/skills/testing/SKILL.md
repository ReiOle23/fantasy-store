---
name: testing
description: How to write and run the tests of the fantasy-store FastAPI + MongoDB service (unit, integration and end to end) so Claude can check that a change works. Use when writing or changing tests, after changing code to verify it, or when the user asks to run, add or fix tests.
---

# Testing (fantasy-store)

Tests use **pytest** + **pytest-asyncio** (everything is async) and **pytest-repeat** for
concurrency checks. HTTP tests use `httpx` (comes with `fastapi[standard]`).

## Where tests live

**Every test always goes inside the `tests/` directory at the project root**
(`fantasy-store/tests/`). Split it by kind:

```
tests/
  __init__.py
  conftest.py      # shared fixtures (test DB, services, factories)
  unit/            # domain entities and pure logic, no DB
    __init__.py
    test_item.py
  integration/     # application services / repositories against MongoDB
    __init__.py
    test_auction_service.py
  e2e/             # HTTP requests to the FastAPI app (routes in src/infrastructure/adapters)
    __init__.py
    test_auction_api.py
```

- Every folder needs an `__init__.py`. Files `test_<thing>.py`, functions `test_<behaviour>`.
- Kind-specific fixtures can go in a `conftest.py` inside that folder.
- The old `tests/domain.tests/` and `tests/application.tests/` folders are legacy: don't add
  tests there; move them to `unit/` and `integration/` when you touch them.

## What goes in each kind

**Unit** — `tests/unit/`
- Entities in `src/domain/` (Item, User, Auction...) and any pure logic.
- No MongoDB, no network. Note: the root `conftest.py` has an `autouse` DB fixture; unit
  tests don't need it, but they must not depend on it either.

**Integration** — `tests/integration/`
- Use cases in `src/application/` and the Mongo repositories in `src/infrastructure/`.
- Run against the real test database `fantasy_back_test` (the root `conftest.py` switches to it
  with `MongoDB.using_database(...)` and clears it before and after every test).
- Use the fixtures from `conftest.py` (`user_service`, `item_service`, `auction_service`,
  `create_user`, `create_item`, `auction_init_user`) instead of building data by hand.
- Cover the concurrency rules: many users buying the last unit of an item, or bidding at the
  same time, must end with exactly one winner and the rest rejected. Fire them together with
  `asyncio.gather(...)` and add `@pytest.mark.repeat(n)` to catch race conditions.

**End to end** — `tests/e2e/`
- Real HTTP calls to the app in `main.py`: register/login, list items, buy, create auction, bid.
- Use `httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test")`
  with the same test database; check status codes, response JSON and the stored state.

## Writing a test

```python
import asyncio, pytest
from datetime import datetime, timedelta


@pytest.mark.asyncio
async def test_only_one_bid_wins(auction_service, auction_init_user):
    owner = await auction_init_user("owner")
    bidders = [await auction_init_user(f"user{i}") for i in range(10)]
    auction = await auction_service.create_auction(
        owner.items[0].id, owner.id, datetime.now() + timedelta(minutes=1))

    results = await asyncio.gather(
        *(auction_service.make_bid(auction.id, b.id, 100) for b in bidders),
        return_exceptions=True)

    assert sum(not isinstance(r, Exception) for r in results) == 1
```

Rules:
- Mark every async test with `@pytest.mark.asyncio`.
- One behaviour per test; test error paths (no money, bid too low, sold out, auction ended).
- Prefer `pytest.raises(<SpecificError>)` over a bare `Exception` when the code raises one.
- Each test creates its own data; never rely on order or on another test's data.

## Running the tests

Integration and e2e tests need MongoDB up (`docker compose -f docker-compose-local.yml up -d`).
Run from the project root:

```bash
pytest                                 # all
pytest tests/unit                      # one kind
pytest tests/integration
pytest tests/e2e
pytest -s tests/integration/test_auction_service.py::test_create_auction   # one test
```

Inside docker instead: `docker compose -f docker-compose-local.yml exec fantasy_store_local pytest`.
Useful flags: `-s` (show prints), `-x` (stop at first failure), `-k <expr>`, `--count=20`
(pytest-repeat, re-run to surface flaky concurrency bugs).

## Checking a change

1. Run the unit tests for the code you touched, then its integration tests.
2. For changes to buying or bidding, also run the concurrency tests with `--count` > 1.
3. Before saying the work is done, run the whole suite once (`pytest`).
4. Report the real result: passed/failed counts and the error output. Don't call it fine if
   anything failed or could not run (e.g. MongoDB was down).

## When tests fail

Don't stop at reporting the failure: fix it until the whole suite passes.

1. Read the failure and decide where the problem is:
   - **The code is wrong** (a bug, a race condition, a broken edge case, a regression): fix
     the code. Don't weaken, skip or delete the test to make it pass.
   - **The behaviour changed on purpose** (new rule, renamed field, new route or response
     shape): update the code *and* the tests that check the old behaviour, and add tests for
     the new one.
   - **The test itself is wrong** (bad data, wrong assumption, depends on test order or timing):
     fix the test.
2. Re-run the failing tests, then the whole suite, and repeat until everything passes. For a
   flaky concurrency failure, re-run with `--count=20` to be sure it is really fixed.
3. Never leave tests skipped, commented out or marked `xfail` to get a green run. If a failure
   can't be fixed (e.g. it needs a decision from the user, or MongoDB is down), stop and
   explain it instead of hiding it.
4. When done, say what was failing, what you changed (code, tests or both) and why.
