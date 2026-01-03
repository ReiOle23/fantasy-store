from dataclasses import dataclass, field
import uuid

@dataclass
class User:
    name: str
    password: str
    id: str = field(default=str(uuid.uuid4()))
    token: str = field(default=str(uuid.uuid4()))
        
