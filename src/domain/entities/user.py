from dataclasses import dataclass, field
from typing import List, TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from src.domain.entities.item import Item

@dataclass
class User:
    name: str
    password: str
    id: str = field(default=str(uuid.uuid4()))
    token: str = field(default=str(uuid.uuid4()))
    items: List['Item'] = field(default_factory=list)
    money: int = field(default=0)
    
    def has_item(self, item_name: str) -> bool:
        return any(item.get('name') == item_name for item in self.items)

    def add_item(self, item: 'Item'):
        item.owner = self.id
        self.items.append(item)
        