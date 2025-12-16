from dataclasses import dataclass
from src.domain.entities.user import User

@dataclass
class Item():
    id: int
    name: str
    quantity:int
    price:int
    owner: User