from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass
class Bid():
    user: str
    price: int
    created_at: datetime = field(default_factory=lambda: datetime.now())
    updated_at: datetime = field(default_factory=lambda: datetime.now())
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    @classmethod
    def from_dict(cls, data: dict) -> 'Bid':
        return cls(**data)