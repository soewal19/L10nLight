import pytest
import pytest_asyncio
from sqlalchemy import select, delete
from app.db import SessionLocal, engine
from app.models import OfferWall, Offer, OfferAssignment, PopupAssignment, OfferChoices, Base

@pytest_asyncio.fixture(autouse=True)
async def cleanup_db():
    """Очистка БД перед и после каждого теста"""
    # Очистка перед тестом
    async with SessionLocal() as session:
        await session.execute(delete(OfferAssignment))
        await session.execute(delete(PopupAssignment))
        await session.execute(delete(OfferWall))
        await session.execute(delete(Offer))
        await session.commit()
    yield
    # Очистка после теста
    async with SessionLocal() as session:
        await session.execute(delete(OfferAssignment))
        await session.execute(delete(PopupAssignment))
        await session.execute(delete(OfferWall))
        await session.execute(delete(Offer))
        await session.commit()

@pytest.mark.asyncio
async def test_get_offer_names(client):
    resp = await client.get("/api/offerwalls/get_offer_names")
    assert resp.status_code == 200
    data = resp.json()
    # Используем первый элемент кортежа (как в оригинальном DRF)
    expected = [offer_name[0] for offer_name in OfferChoices.choices]
    assert data == {"offer_names": expected}

@pytest.mark.asyncio
async def test_get_offerwall_not_found(client):
    resp = await client.get("/api/offerwalls/non-existent-token")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Not found."}

@pytest.mark.asyncio
async def test_get_offerwall_ok(client):
    # Prepare data
    async with SessionLocal() as session:
        # Используем уникальные имена для избежания конфликтов
        import uuid as uuid_lib
        unique_token = f"t-{uuid_lib.uuid4().hex[:8]}"
        unique_offer_uuid = f"u-{uuid_lib.uuid4().hex[:8]}"
        unique_offer_name = f"TestOffer_{uuid_lib.uuid4().hex[:8]}"
        
        ow = OfferWall(token=unique_token, name="Wall", url="https://wall", description="desc")
        offer = Offer(
            uuid=unique_offer_uuid,
            id=1,
            url="https://offer",
            is_active=True,
            name=unique_offer_name,
            sum_to=None,
            term_to=None,
            percent_rate=None,
        )
        session.add_all([ow, offer])
        await session.flush()

        assign = OfferAssignment(offer_wall_token=ow.token, offer_uuid=offer.uuid, order=1)
        popup = PopupAssignment(offer_wall_token=ow.token, offer_uuid=offer.uuid, order=1)
        session.add_all([assign, popup])
        await session.commit()

    # Request
    resp = await client.get(f"/api/offerwalls/{unique_token}")
    assert resp.status_code == 200
    data = resp.json()

    assert data["token"] == unique_token
    assert data["name"] == "Wall"
    assert data["url"] == "https://wall"
    assert "offer_assignments" in data and len(data["offer_assignments"]) == 1
    assert "popup_assignments" in data and len(data["popup_assignments"]) == 1

    offer_data = data["offer_assignments"][0]["offer"]
    assert offer_data["uuid"] == unique_offer_uuid
    assert offer_data["name"] == unique_offer_name