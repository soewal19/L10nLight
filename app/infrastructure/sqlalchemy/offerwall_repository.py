from typing import Optional, Sequence, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.entities import OfferWall as DomainOfferWall, Offer as DomainOffer, OfferWallOffer, OfferWallPopupOffer
from app.domain.ports.offerwall_repository import OfferWallRepository
from app.models import OfferWall, OfferAssignment, PopupAssignment, Offer

class SqlAlchemyOfferWallRepository(OfferWallRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def _base_query(self):
        return (
            select(OfferWall)
            .options(
                selectinload(OfferWall.offer_assignments).selectinload(OfferAssignment.offer),
                selectinload(OfferWall.popup_assignments).selectinload(PopupAssignment.offer),
            )
        )

    @staticmethod
    def _to_domain_offer(orm_offer: Offer) -> DomainOffer:
        return DomainOffer(
            uuid=orm_offer.uuid,
            id=orm_offer.id,
            url=orm_offer.url,
            is_active=orm_offer.is_active,
            name=orm_offer.name,
            sum_to=orm_offer.sum_to,
            term_to=orm_offer.term_to,
            percent_rate=orm_offer.percent_rate,
        )

    @staticmethod
    def _to_domain(orm_ow: OfferWall) -> DomainOfferWall:
        offers: List[OfferWallOffer] = [
            OfferWallOffer(offer=SqlAlchemyOfferWallRepository._to_domain_offer(a.offer))
            for a in orm_ow.offer_assignments
            if a.offer is not None
        ]
        popups: List[OfferWallPopupOffer] = [
            OfferWallPopupOffer(offer=SqlAlchemyOfferWallRepository._to_domain_offer(p.offer))
            for p in orm_ow.popup_assignments
            if p.offer is not None
        ]
        return DomainOfferWall(
            token=orm_ow.token,
            name=orm_ow.name,
            url=orm_ow.url,
            description=orm_ow.description,
            offer_assignments=offers,
            popup_assignments=popups,
        )

    async def list(self, name: Optional[str], url: Optional[str], page: int, page_size: int) -> Sequence[DomainOfferWall]:
        stmt = self._base_query()
        if name:
            stmt = stmt.where(OfferWall.name.ilike(f"%{name}%"))
        if url:
            stmt = stmt.where(OfferWall.url.ilike(f"%{url}%"))
        stmt = stmt.offset((page - 1) * page_size).limit(page_size)
        result = await self.session.execute(stmt)
        orm_items = result.scalars().unique().all()
        return [self._to_domain(ow) for ow in orm_items]

    async def get_by_token(self, token: str) -> Optional[DomainOfferWall]:
        stmt = self._base_query().where(OfferWall.token == token)
        result = await self.session.execute(stmt)
        orm_item = result.scalar_one_or_none()
        return self._to_domain(orm_item) if orm_item else None

    async def get_by_url(self, url: str) -> Optional[DomainOfferWall]:
        stmt = self._base_query().where(OfferWall.url == url)
        result = await self.session.execute(stmt)
        orm_item = result.scalar_one_or_none()
        return self._to_domain(orm_item) if orm_item else None