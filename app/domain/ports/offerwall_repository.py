from typing import Optional, Sequence, Protocol, runtime_checkable
from app.domain.entities import OfferWall

@runtime_checkable
class OfferWallRepository(Protocol):
    async def list(self, name: Optional[str], url: Optional[str], page: int, page_size: int) -> Sequence[OfferWall]:
        ...

    async def get_by_token(self, token: str) -> Optional[OfferWall]:
        ...

    async def get_by_url(self, url: str) -> Optional[OfferWall]:
        ...