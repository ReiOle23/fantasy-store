from dataclasses import dataclass, field
from typing import Optional
import uuid

WEAPON = "weapon"
ARMOR = "armor"
MATERIAL = "material"
ITEM_TYPES = (WEAPON, ARMOR, MATERIAL)

ITEM_CATEGORIES = ("normal", "rare", "legendary")
WEAPON_TYPES = ("bow", "crossbow", "lance", "lance_shield", "large_sword", "two_sword")
ARMOR_TYPES = ("helmet", "shoulders", "chest", "pants", "boots", "amulet")
MATERIAL_SPECIALIZATIONS = ("market", "alchemy", "blacksmith", "mining", "herboristery", "fishing", "hunt", "all")
MATERIAL_USE_TYPES = ("food", "refinery")


def default_weapon_attributes() -> dict:
    return {
        'damage': 0,
        'critical': 0,
        'true_damage': 0,
        'on_hero_damage': 0,
        'on_dungeon_damage': 0,
        'on_hero_true_damage': 0,
        'on_dungeon_true_damage': 0,
        'fire_damage': 0,
        'stun_damage': 0,
        'frozen_damage': 0,
        'disoriented_damage': 0,
        'distance_damage': 0,
        'close_damage': 0,
        'dodge': 0,
        'agility': 0,
    }


def default_armor_attributes() -> dict:
    return {
        'health': 0,
        'defence': 0,
        'ignore_stun': 0,
        'on_hero_battle_health': 0,
        'on_dungeon_battle_health': 0,
        'on_hero_battle_defence': 0,
        'on_dungeon_battle_defence': 0,
        'fire_protection': 0,
        'frozen_protection': 0,
        'disoriented_protection': 0,
        'distance_protection': 0,
        'close_protection': 0,
        'dodge': 0,
        'agility': 0,
        'mission_time_reduce': 0,
    }


@dataclass
class Item():
    name: str
    quantity: int
    price: int
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    owner: Optional[str] = None
    item_type: Optional[str] = None
    properties: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict) -> 'Item':
        return cls(**data)

    @classmethod
    def weapon(cls, name: str, price: int, quantity: int = 1, level: str = '1',
               category: str = 'normal', type: str = 'large_sword', durability: int = 100,
               upgrades: int = 0, battle_attributes: Optional[dict] = None,
               upgrade_materials: Optional[list] = None) -> 'Item':
        attributes = default_weapon_attributes()
        if battle_attributes:
            attributes.update(battle_attributes)
        return cls(
            name=name,
            price=price,
            quantity=quantity,
            item_type=WEAPON,
            properties={
                'level': level,
                'category': category,
                'type': type,
                'durability': durability,
                'upgrades': upgrades,
                'battle_attributes': attributes,
                'upgrade_materials': upgrade_materials or [],
            },
        )

    @classmethod
    def armor(cls, name: str, price: int, quantity: int = 1, level: str = '1',
              category: str = 'normal', type: str = 'chest', durability: int = 100,
              upgrades: int = 0, battle_attributes: Optional[dict] = None,
              upgrade_materials: Optional[list] = None) -> 'Item':
        attributes = default_armor_attributes()
        if battle_attributes:
            attributes.update(battle_attributes)
        return cls(
            name=name,
            price=price,
            quantity=quantity,
            item_type=ARMOR,
            properties={
                'level': level,
                'category': category,
                'type': type,
                'durability': durability,
                'upgrades': upgrades,
                'battle_attributes': attributes,
                'upgrade_materials': upgrade_materials or [],
            },
        )

    @classmethod
    def material(cls, name: str, price: int, quantity: int = 1, description: str = '',
                 specialization_type: str = 'market', use_type: str = 'refinery',
                 conditions_reward: int = 0) -> 'Item':
        return cls(
            name=name,
            price=price,
            quantity=quantity,
            item_type=MATERIAL,
            properties={
                'description': description,
                'specialization_type': specialization_type,
                'use_type': use_type,
                'conditions_reward': conditions_reward,
            },
        )

    def is_auctionable(self) -> bool:
        return self.item_type in ITEM_TYPES and self.quantity > 0
