from dataclasses import dataclass
from src.domain.entities.item import Item

@dataclass
class Store():
    id: int
    name: str
    items: list[Item]
