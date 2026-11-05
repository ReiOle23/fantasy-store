"""Business rule 15: heroes sell weapons, armour and materials to each other at the auction house."""
import pytest
from src.domain.entities.item import Item


@pytest.mark.parametrize("item", [
    Item.weapon(name="Bow", price=10),
    Item.armor(name="Chest", price=10),
    Item.material(name="Iron", price=10, quantity=5),
])
def test_weapons_armour_and_materials_can_be_auctioned(item):
    assert item.is_auctionable() is True


@pytest.mark.parametrize("item_type", [None, "potion", "skin", "mount"])
def test_other_item_types_cannot_be_auctioned(item_type):
    item = Item(name="Thing", quantity=1, price=10, item_type=item_type)
    assert item.is_auctionable() is False


def test_item_with_no_quantity_cannot_be_auctioned():
    item = Item.material(name="Iron", price=10, quantity=0)
    assert item.is_auctionable() is False
