from dataclasses import dataclass, field
from typing import List, TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from src.domain.entities.item import Item

@dataclass
class User:
    name: str
    password: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    token: str = field(default_factory=lambda: str(uuid.uuid4()))
    items: List['Item'] = field(default_factory=list)
    money: int = field(default=0)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Reconstruct User from MongoDB document"""
        from src.domain.entities.item import Item
        
        if 'items' in data and data['items']:
            data['items'] = [
                Item.from_dict(item) if isinstance(item, dict) else item
                for item in data['items']
            ]
        else:
            data['items'] = []
        
        return cls(**data)
    
    def has_item(self, item_name: str) -> bool:
        return any(item.name == item_name for item in self.items)
    
    def get_item(self, item_id: str) -> 'Item':
        for item in self.items:
            if item.id == item_id:
                return item
        return None

    def add_item(self, item: 'Item'):
        item.owner = self.id
        self.items.append(item)
        
    def remove_item(self, item_id: str) -> bool:
        for i, item in enumerate(self.items):
            if item.id == item_id:
                del self.items[i]
                return True
        return False