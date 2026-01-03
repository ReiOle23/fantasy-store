from dataclasses import dataclass, field
import uuid
from src.domain.entities.item import Item

@dataclass
class User:
    name: str
    password: str
    id: str = field(default=str(uuid.uuid4()))
    token: str = field(default=str(uuid.uuid4()))
    items: list[Item] = field(default_factory=list)
    