# Buy fantasy items store in an auction
from dataclasses import dataclass
import pytest
from pytest import fixture

@dataclass
class User():
    id: int
    nickname: str

@dataclass
class Item():
    id: int
    name: str
    owner: User
    buyable: bool


class Auction():
    
    def __init__(self):
        self.item_bag = {}
        
    def add_item(self, item: Item):
        self.item_bag[item.id] = item
        
    def get_item(self, id:int) -> Item:
        return self.item_bag[id]
    
    def buy_item(self, id:int, user:User) -> Item:
        self.item_bag[id].owner = user
        return self.item_bag.pop(id, None)
        
        
@fixture
def user_1():
    return User(1,"Reiole")

@fixture
def user_2():
    return User(2,"Julia")

@fixture
def user_3():
    return User(3,"Toshiva")

@fixture
def auction():
    return Auction()

def test_auction_add_item(auction, user_1):
    item1 = Item(1,"Espada del Norte", user_1, True)
    auction.add_item(item1)
    assert auction.get_item(item1.id).name == item1.name

def test_user_buy_item(auction, user_1, user_2):
    item1 = Item(1,"Espada del Norte", user_1, True)
    auction.add_item(item1)
    item_bought = auction.buy_item(item1.id,user_2)
    assert item_bought.id == item1.id 
    assert item_bought.owner == user_2

def test_auction_buy_item(auction, user_1, user_2):
    item1 = Item(1,"Espada del Norte", user_1, True)
    auction.add_item(item1)
    assert len(auction.item_bag) == 1
    auction.buy_item(item1.id,user_2)
    assert len(auction.item_bag) == 0
        
@pytest.mark.asyncio
async def test_auction_two_users_buy_items(auction, user_1, user_2, user_3):
    item1 = Item(1, "Espada del Norte", user_1, True)
    item2 = Item(2, "Armadura dorada", user_1, True)
    auction.add_item(item1)
    auction.add_item(item2)
    result1 = await auction.buy_item(item1.id,user_2)
    result2 = await auction.buy_item(item1.id,user_3)
    assert result1.owner == user_2
    assert result2.owner == user_3
    
# @pytest.mark.asyncio
# async def test_auction_two_users_buy_same_item(auction, user_1, user_2, user_3):
#     item1 = Item(1,"Espada del Norte", user_1, True)
#     auction.add_item(item1)
#     result1 = await auction.buy_item(item1.id,user_2)
#     result2 = await auction.buy_item(item1.id,user_3)
    
#     # result = await async_func()
#     # assert result == 42


aa = {
    "id": 12,
    "name": 12,
}

aa["id"] = 2