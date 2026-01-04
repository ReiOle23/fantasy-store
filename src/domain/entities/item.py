from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING
import uuid

@dataclass
class Item():
    name: str
    quantity:int
    price:int
    id: str = field(default=str(uuid.uuid4()))
    owner: Optional[str] = None
    