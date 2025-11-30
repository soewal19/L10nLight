import asyncio
from typing import Optional, Sequence

from litestar.exceptions import NotFoundException

from app.application.offerwall_service import OfferWallService
from app.domain.entities import (
    Offer,
    OfferWall,
    OfferWallOffer,
    OfferWallPopupOffer,
)
from app.domain.ports.offerwall_repository import OfferWallRepository


class FakeRepo(OfferWallRepository):
    def __init__(self, items: dict[str, OfferWall]) -> None:
        self.items = items

    async def list(
        self,
        name: Optional[str],
        url: Optional[str],
        page: int,
        page_size: int,
    ) -> Sequence[OfferWall]:
        values = list(self.items.values())
        # Псевдо-фильтрация как в реальном репозитории
        if name:
            values = [v for v in values if name.lower() in v.name.lower()]
        if url:
            values = [v for v in values if url.lower() in v.url.lower()]
        start = (page - 1) * page_size
        end = start + page_size
        return values[start:end]

    async def get_by_token(self, token: str) -> Optional[OfferWall]:
        return self.items.get(token)


def make_sample_data() -> dict[str, OfferWall]:
    offer1 = Offer(
        uuid="uuid-1",
        id=1,
        url="https://ex.com/1",
        is_active=True,
        name="Loanplus",
        sum_to=None,
        term_to=None,
        percent_rate=None,
    )
    offer2 = Offer(
        uuid="uuid-2",
        id=2,
        url="https://ex.com/2",
        is_active=True,
        name="Suncredit",
        sum_to=None,
        term_to=None,
        percent_rate=None,
    )
    ow1 = OfferWall(
        token="token-1",
        name="Wall One",
        url="https://wall.one",
        description="desc",
        offer_assignments=[OfferWallOffer(offer=offer1)],
        popup_assignments=[OfferWallPopupOffer(offer=offer2)],
    )
    ow2 = OfferWall(
        token="token-2",
        name="Second Wall",
        url="https://second.wall",
        description=None,
        offer_assignments=[OfferWallOffer(offer=offer2)],
        popup_assignments=[],
    )
    return {ow1.token: ow1, ow2.token: ow2}


def test_service_list_returns_items():
    repo = FakeRepo(make_sample_data())
    service = OfferWallService(repo)

    result = asyncio.run(service.list_offerwalls(name=None, url=None, page=1, page_size=10))

    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(x, OfferWall) for x in result)
    assert result[0].offer_assignments and result[0].popup_assignments


def test_service_list_filters_by_name():
    repo = FakeRepo(make_sample_data())
    service = OfferWallService(repo)

    result = asyncio.run(service.list_offerwalls(name="Second", url=None, page=1, page_size=10))

    assert len(result) == 1
    assert result[0].name == "Second Wall"


def test_service_get_by_token_success():
    repo = FakeRepo(make_sample_data())
    service = OfferWallService(repo)

    result = asyncio.run(service.get_offerwall("token-1"))

    assert isinstance(result, OfferWall)
    assert result.token == "token-1"
    assert len(result.offer_assignments) == 1
    assert len(result.popup_assignments) == 1


def test_service_get_by_token_not_found_raises():
    repo = FakeRepo(make_sample_data())
    service = OfferWallService(repo)

    try:
        asyncio.run(service.get_offerwall("missing"))
        assert False, "Expected NotFoundException"
    except NotFoundException as exc:
        assert "Not found" in str(exc)


def test_service_get_offer_names_non_empty():
    repo = FakeRepo(make_sample_data())
    service = OfferWallService(repo)

    names = service.get_offer_names()

    assert isinstance(names, list)
    assert all(isinstance(n, str) for n in names)
    assert len(names) > 0