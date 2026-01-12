# In a separate module (e.g., __init__.py or schemas/__init__.py)
from src.infrastructure.adapters.schemas.user import UserResponse
from src.infrastructure.adapters.schemas.item import ItemObject
from src.infrastructure.adapters.schemas.auction import AuctionObject

# Rebuild all models that have forward references
UserResponse.model_rebuild()
ItemObject.model_rebuild()
AuctionObject.model_rebuild()