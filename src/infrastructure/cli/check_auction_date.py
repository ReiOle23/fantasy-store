import asyncio
import logging
from src.application.adapters.auction_service import AuctionService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    auction_service = AuctionService()
    auctions = await auction_service.get_auctions()
    [await auction_service.finish_auction(auct) for auct in auctions]
    
if __name__ == "__main__":
    asyncio.run(main())