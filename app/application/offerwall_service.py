from typing import Optional, Sequence
from litestar.exceptions import NotFoundException

from app.domain.entities import OfferWall
from app.domain.ports.offerwall_repository import OfferWallRepository
from app.models import OfferChoices  # источник имён (инфраструктурная константа)

class OfferWallService:
    def __init__(self, repo: OfferWallRepository) -> None:
        self.repo = repo

    async def list_offerwalls(self, name: Optional[str], url: Optional[str], page: int, page_size: int) -> Sequence[OfferWall]:
        return await self.repo.list(name=name, url=url, page=page, page_size=page_size)

    async def get_offerwall(self, token: str) -> OfferWall:
        offerwall = await self.repo.get_by_token(token=token)
        if not offerwall:
            raise NotFoundException("Not found.")
        return offerwall

    async def get_offerwall_by_url(self, url: str) -> OfferWall:
        offerwall = await self.repo.get_by_url(url=url)
        if not offerwall:
            raise NotFoundException("Not found.")
        return offerwall

    def get_offer_names(self) -> list[str]:
        # Используем первый элемент кортежа (как в оригинальном DRF: offer_name[0])
        choices = getattr(OfferChoices, "choices", [])
        return [offer_name[0] for offer_name in choices]