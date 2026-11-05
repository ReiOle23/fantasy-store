import pytest
from src.domain.entities.item import Item

@pytest.mark.asyncio
async def test_create_item_weapon():
    weapon = Item(
        name="Gandalf staff",
        quantity=1,
        price=250,
        properties={
            'level':2,
            'category':'legendary',
            'attack':20.0,
            'critical':20.6,
            'agility':5,
            'type':'bow',
            'durability':100,
        }
    )
    assert 'attack' in weapon.properties

@pytest.mark.asyncio
async def test_create_item_armor():
    armor = Item(
        name="Gandalf staff",
        quantity=1,
        price=250,
        properties={
            'level':2,
            'category':'legendary',
            'defence':20.0,
            'health':20.6,
            'agility':5,
            'type':'shoulder',
            'durability':100,
        }
    )
    assert 'type' in armor.properties

@pytest.mark.asyncio
async def test_create_item_material():
    material = Item(
        name="Gandalf staff",
        quantity=1,
        price=250,
        properties={
            'description':'',
            'specialization_type':'market',
            'quantity':23,
            'conditions_reward':5,
            'use_type':'food',
        }
    )
    assert 'use_type' in material.properties

@pytest.mark.asyncio
async def test_create_item_potion():
    potion = Item(
        name="Gandalf staff",
        quantity=1,
        price=250,
        properties={

            'category':'rare',
            'description':'',
            'attack':12,
            'defence':23,
            'health':19,
            'critical':2,
            'type':'natural',
        }
    )
    assert 'description' in potion.properties
