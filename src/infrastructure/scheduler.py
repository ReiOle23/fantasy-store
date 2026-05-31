import os
import asyncio
import logging

import httpx

from src.application.adapters.auction_service import AuctionService
from src.infrastructure.adapters.controllers.auction_controller import AuctionController

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REFRESH_INTERVAL_SECONDS = 10
ROL_GAME_URL = os.getenv("ROL_GAME_URL", "http://localhost:59600").rstrip("/")
ROL_GAME_SETTLE_PATH = "/api/v1/auctions/settle"
SERVICE_TOKEN = os.getenv("AUCTION_SERVICE_TOKEN", "local-auction-service-token")


async def _notify_rol_game(client: httpx.AsyncClient, payload: dict) -> bool:
    """POST a settled auction to rol-game so it creates the winner/seller mails. Idempotent on its side."""
    try:
        response = await client.post(
            f"{ROL_GAME_URL}{ROL_GAME_SETTLE_PATH}",
            json=payload,
            headers={"X-Service-Token": SERVICE_TOKEN},
            timeout=10,
        )
    except httpx.HTTPError as error:
        logger.warning("Could not reach rol-game to settle auction: %s", error)
        return False
    if response.status_code in (200, 201):
        return True
    logger.warning("rol-game rejected settlement (%s): %s", response.status_code, response.text)
    return False


async def _refresh_once(service: AuctionService, controller: AuctionController, client: httpx.AsyncClient):
    for auction in await service.pending_settlements():
        payload = (await controller._return_auction_object(auction)).model_dump(mode="json")
        if await _notify_rol_game(client, payload):
            await service.claim_settled(auction.id)
            logger.info("✓ Auction %s settled and mailed to rol-game", auction.id)


async def auction_refresh_loop():
    """Every REFRESH_INTERVAL_SECONDS: finish ended auctions and push their settlement mails to rol-game.

    The auction is only marked settled_in_game after rol-game confirms, so a failed push is retried
    on the next tick. rol-game dedupes by auction_id, making retries safe.
    """
    service = AuctionService()
    controller = AuctionController()
    async with httpx.AsyncClient() as client:
        while True:
            try:
                await _refresh_once(service, controller, client)
            except Exception:
                logger.exception("Auction refresh loop iteration failed")
            await asyncio.sleep(REFRESH_INTERVAL_SECONDS)
