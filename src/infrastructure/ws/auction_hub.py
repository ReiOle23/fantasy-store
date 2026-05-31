import asyncio
import json
import logging

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class AuctionHub:
    """In-memory fan-out of auction events (bids, finishes) to every connected list viewer."""

    def __init__(self):
        self._connections: set[WebSocket] = set()
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        async with self._lock:
            self._connections.add(websocket)

    async def disconnect(self, websocket: WebSocket):
        async with self._lock:
            self._connections.discard(websocket)

    async def broadcast(self, message: dict):
        data = json.dumps(message, default=str)
        async with self._lock:
            targets = list(self._connections)
        for websocket in targets:
            try:
                await websocket.send_text(data)
            except Exception:
                await self.disconnect(websocket)


auction_hub = AuctionHub()
