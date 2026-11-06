# fantasy-store

This is a project which recreates a store with unique items and auctions
Theres users which buy or bid on items.
Users can only register,log,buy,or bid.

For the Unique items, every one has a limit quantity and when that item hasn't quantity
the other users can't get it.

The system needs to be totally async because we have pics of 1000 people simultaneously buying the same item

For the Auction, the system needs to handle multiple bids simultaneously and care of the values of the bids. 
If two bids at the same time, only one is selected, the other is rejected and informed about the new item value.

## Database
The database will be a mongoDB as we have a large set of items and they have different fields depending on the object type
Example: An Item can be a weapon or an armor or a potion. weapon has durability, potion has time expense.
<!-- Usefull -->
MongoDB could be used as a complement for highly variable product catalogs or review/comment systems, but not as a primary database.
<!--  -->
In this example we don't have payment nor inventory so mongoDB is best option

To enter Mongo instance:
- docker exec -it fantasy_mongodb mongosh "mongodb://fantasy:fantasy@localhost:27017/fantasy_back?authSource=admin"
- use fantasy_back_test

## Arquitecture
Arquitecture used is a monolitic by layers and using Hexagonal

<!-- Usefull -->
Celery(orquestrator of tasks) with Redis(database cache memory, very fast) you can have sincronous system that
replicates an async by executing tasks of the celery in order and by getting the info from the Redis.
<!--  -->

## Tests
To run single tests:
- pytest -s tests/integration/test_item_service.py

docker exec -it fantasy_mongodb mongosh -u fantasy -p fantasy --authenticationDatabase admin
---

# Task workflow with Trello + Claude Code

Every task or new feature goes through the **rol-game** Trello board
(https://trello.com/b/esa1DfSe/rol-game), which tracks all three repos
(`crown-trade-front`, `rol-game`, `fantasy-store`). Claude Code does steps 2 and 3
with two project skills. The skills are the same in all three repos, so you can run
them from any of them.

## 1. Create the card in Trello
Add the card to **To do**. Write in the description what the task or feature must do.
The clearer the description, the better the criteria. If it is too vague, Claude asks
you questions first.

## 2. Write the acceptance criteria
In Claude Code:

```
acceptance criteria for trello card <card title>
```

Skill `trello-acceptance-criteria`:
- reads the card and `docs/BUSINESS_RULES.md` (the product source of truth),
- writes requirements, testable acceptance criteria (AC1, AC2...) and the tests that
  must exist to `docs/acceptance/<shortLink>-<card-name>.txt`,
- posts them to the card as an `Acceptance criteria` checklist and a comment,
- lists any conflicts with the business rules or open questions. **You decide these**
  before going on.

Review the .txt. Change it if something is wrong, because it is the contract for step 3.

## 3. Implement the card
```
implement trello card <card title>
```

Skill `trello-implement`:
- loads the acceptance .txt (runs step 2 first if it doesn't exist),
- moves the card to **Doing**,
- writes the code and tests in every affected repo (backend first, then front),
- runs the full test suites and marks each criterion **PASS**, **FAIL** or
  **NOT VERIFIED**,
- ticks only the passing criteria on the card's checklist, and writes the result to
  the .txt and as a card comment.

## 4. Read the report
At the end Claude prints:
- how many acceptance criteria pass, each with the test that proves it,
- the **new features**: what the player can do now that they couldn't before,
- what fails or couldn't be verified, and why,
- the test results and the files changed.

If every criterion passes, Claude asks whether to move the card to **Done** and
whether to commit and push (`commit-push` skill). It never does either without your
confirmation. If something fails, the card stays in **Doing**. Fix it or answer
Claude's questions, then run step 3 again: criteria that already pass are only
re-checked, not rebuilt.

## Notes
- Cypress e2e tests in the front need the app and both backends running. Otherwise
  they are reported as **not run**, never as passed.
- If a game rule changes, `docs/BUSINESS_RULES.md` must be updated in all three repos
  (the "Game rules" section is identical in all of them).
