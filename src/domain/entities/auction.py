from dataclasses import dataclass, field
from datetime import datetime
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.entities.item import Item
    from src.domain.entities.bid import Bid

@dataclass
class Auction():
    name: str
    item: 'Item'
    start_date: datetime
    end_date: datetime
    id: str = field(default=str(uuid.uuid4()))
    bids: list['Bid'] = field(default_factory=list)
