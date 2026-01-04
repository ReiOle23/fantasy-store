from dataclasses import dataclass, field
from datetime import datetime
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.entities.user import User

@dataclass
class Bid():
    user: 'User'
    price: float
    created_at: datetime = field(default_factory=lambda: datetime.now())
    updated_at: datetime = field(default_factory=lambda: datetime.now())
    id: str = field(default=str(uuid.uuid4()))
