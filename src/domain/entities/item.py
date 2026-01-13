from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING
import uuid

@dataclass
class Item():
    name: str
    quantity:int
    price:int
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    owner: Optional[str] = None
    properties: dict = field(default_factory=lambda: {})
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Item':
        return cls(**data)