from src.infrastructure.database import MongoDB
from src.domain.entities.item import Item
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def upload_items(item: Item):
    try:
        await MongoDB.save_obj(item)
        logger.info(f"✓ Uploaded: {item.name}")
    except Exception as e:
        logger.error(f"✗ Failed to upload {item.name}: {e}")
        raise

async def main():
    items = [
        Item.weapon(
            name="Flamebrand Longsword",
            price=1000,
            quantity=2,
            level="5",
            category="legendary",
            type="large_sword",
            battle_attributes={"damage": 120, "critical": 15, "fire_damage": 30},
        ),
        Item.armor(
            name="Cloak of Elvenkind",
            price=2000,
            quantity=3,
            level="4",
            category="rare",
            type="chest",
            battle_attributes={"defence": 80, "dodge": 25, "agility": 10},
        ),
        Item.material(
            name="Mithril Ore",
            price=1500,
            quantity=10,
            description="Rare ore used by blacksmiths to forge legendary gear.",
            specialization_type="blacksmith",
            use_type="refinery",
        ),
    ]
    await asyncio.gather(*[
        upload_items(item) for item in items
    ])
    
if __name__ == "__main__":
    asyncio.run(main())