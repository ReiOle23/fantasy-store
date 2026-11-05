"""Business rule 15: the auction list updates live for everyone watching it."""
import json
import pytest
from src.infrastructure.ws.auction_hub import AuctionHub


class FakeWebSocket:
    def __init__(self, broken: bool = False):
        self.broken = broken
        self.accepted = False
        self.sent: list[str] = []

    async def accept(self):
        self.accepted = True

    async def send_text(self, data: str):
        if self.broken:
            raise RuntimeError("connection closed")
        self.sent.append(data)


@pytest.mark.asyncio
async def test_broadcast_reaches_every_watcher():
    hub = AuctionHub()
    watchers = [FakeWebSocket() for _ in range(3)]
    for ws in watchers:
        await hub.connect(ws)

    await hub.broadcast({"type": "bid", "auction_id": "a1"})

    for ws in watchers:
        assert ws.accepted
        assert [json.loads(m) for m in ws.sent] == [{"type": "bid", "auction_id": "a1"}]


@pytest.mark.asyncio
async def test_disconnected_watcher_stops_receiving_updates():
    hub = AuctionHub()
    staying, leaving = FakeWebSocket(), FakeWebSocket()
    await hub.connect(staying)
    await hub.connect(leaving)
    await hub.disconnect(leaving)

    await hub.broadcast({"type": "created"})

    assert len(staying.sent) == 1
    assert leaving.sent == []


@pytest.mark.asyncio
async def test_broken_watcher_does_not_block_the_others_and_is_dropped():
    hub = AuctionHub()
    broken, healthy = FakeWebSocket(broken=True), FakeWebSocket()
    await hub.connect(broken)
    await hub.connect(healthy)

    await hub.broadcast({"type": "bid"})
    broken.broken = False
    await hub.broadcast({"type": "bid"})

    assert len(healthy.sent) == 2
    assert broken.sent == []
