from dataclasses import dataclass, field
import uuid
from src.domain.entities.user import User

@dataclass
class Item():
    name: str
    quantity:int
    price:int
    owner: User
    id: str = field(default=str(uuid.uuid4()))
    