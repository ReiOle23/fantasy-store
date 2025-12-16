from typing import Optional, Protocol

class UserRepository(Protocol):
    async def add(self, user: dict) -> None:
        ...

    async def find_by_name(self, name: str) -> Optional[dict]:
        ...
