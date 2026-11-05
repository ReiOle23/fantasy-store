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
- `tests/` — `domain.tests/`, `application.tests/` (e.g. `pytest -s tests/application.tests/test_item.py`)
