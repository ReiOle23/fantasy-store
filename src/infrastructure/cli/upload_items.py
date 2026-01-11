from src.infrastructure.database import MongoDB
from src.domain.entities.item import Item
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def upload_items(item_data: dict):
    try:
        item = Item(
            name=item_data["name"],
            quantity=item_data["quantity"],
            price=item_data["price"]
        )
        await MongoDB.save_obj(item)
        logger.info(f"✓ Uploaded: {item.name}")
    except Exception as e:
        logger.error(f"✗ Failed to upload {item_data.get('name', 'Unknown')}: {e}")
        raise

async def main():
    item_names = [
        {
            "name": "Flamebrand Longsword",
            "quantity": 2,
            "price": 1000
        },
        {
            "name": "Cloak of Elvenkind",
            "quantity": 3,
            "price": 2000
        },
        {
            "name": "Bag of Holding",
            "quantity": 2,
            "price": 1500
        },
        {
            "name": "Potion of Greater Healing",
            "quantity": 1,
            "price": 1800
        },
        {
            "name": "Staff of the Magi",
            "quantity": 1,
            "price": 1200
        },
        ]
    await asyncio.gather(*[
        upload_items(item) for item in item_names
    ])
    
if __name__ == "__main__":
    asyncio.run(main())