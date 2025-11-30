from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.sqlalchemy.offerwall_repository import SqlAlchemyOfferWallRepository
from app.application.offerwall_service import OfferWallService
from app.domain.ports.offerwall_repository import OfferWallRepository

def provide_offerwall_repository(db_session: AsyncSession) -> OfferWallRepository:
    return SqlAlchemyOfferWallRepository(db_session)

def provide_offerwall_service(repo: OfferWallRepository) -> OfferWallService:
    return OfferWallService(repo)