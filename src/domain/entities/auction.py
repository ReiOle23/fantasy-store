from dataclasses import dataclass, field
from datetime import datetime
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.entities.item import Item
    from src.domain.entities.bid import Bid
    from src.domain.entities.user import User

@dataclass
class Auction():
    item: 'Item'
    user: 'User'
    start_date: datetime
    end_date: datetime
    highest_bid: int = 0
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    bids: list['Bid'] = field(default_factory=list)
    highest_bidder: str = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Auction':
        """Reconstruct Auction from MongoDB document"""
        from src.domain.entities.bid import Bid
        from src.domain.entities.item import Item
        from src.domain.entities.user import User
        
        # Reconstruct bids
        if 'bids' in data and data['bids']:
            data['bids'] = [
                Bid.from_dict(bid) if isinstance(bid, dict) else bid 
                for bid in data['bids']
            ]
        
        # Reconstruct item (if needed)
        if 'item' in data and isinstance(data['item'], dict):
            data['item'] = Item.from_dict(data['item'])
        
        # Reconstruct user (if needed)
        if 'user' in data and isinstance(data['user'], dict):
            data['user'] = User.from_dict(data['user'])
        
        return cls(**data)
    