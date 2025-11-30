from typing import Optional

from litestar import Controller, get
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import OfferWall, OfferChoices, OfferAssignment, PopupAssignment
from app.schemas import OfferWall as OfferWallSchema, OfferNames
from app.application.offerwall_service import OfferWallService


class OfferWallController(Controller):
    path = "/offerwalls"
    tags = ["offerwalls"]

    @get(
        "",
        summary="Получить список офферволлов",
        description="Возвращает список всех офферволлов с возможностью фильтрации по имени и URL",
        responses={
            200: {
                "description": "Список офферволлов успешно получен",
                "content": {
                    "application/json": {
                        "schema": {"type": "array", "items": {"$ref": "#/components/schemas/OfferWall"}}
                    }
                }
            }
        }
    )
    async def list_offerwalls(
        self,
        service: OfferWallService,
        name: Optional[str] = None,
        url: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> list[OfferWallSchema]:
        """Получить список офферволлов с фильтрацией.
        
        Args:
            service: Сервис для работы с офферволлами
            name: Фильтр по имени офферволла (опционально)
            url: Фильтр по URL офферволла (опционально)
            page: Номер страницы для пагинации (по умолчанию 1)
            page_size: Количество элементов на странице (по умолчанию 20)
            
        Returns:
            Список офферволлов
        """
        offerwalls = await service.list_offerwalls(name=name, url=url, page=page, page_size=page_size)
        return [OfferWallSchema.model_validate(ow) for ow in offerwalls]

    @get(
        "/{token:str}",
        summary="Получить офферволл по токену",
        description="Возвращает детали конкретного офферволла по его уникальному токену",
        responses={
            200: {
                "description": "Офферволл успешно найден",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/OfferWall"}
                    }
                }
            },
            404: {
                "description": "Офферволл не найден"
            }
        }
    )
    async def get_offerwall(self, service: OfferWallService, token: str) -> OfferWallSchema:
        """Получить офферволл по токену.
        
        Args:
            service: Сервис для работы с офферволлами
            token: Уникальный токен офферволла
            
        Returns:
            Детали офферволла
            
        Raises:
            NotFoundException: Если офферволл не найден
        """
        offerwall = await service.get_offerwall(token=token)
        return OfferWallSchema.model_validate(offerwall)

    @get(
        "/by_url/{url:str}",
        summary="Получить офферволл по URL",
        description="Возвращает детали конкретного офферволла по его URL",
        responses={
            200: {
                "description": "Офферволл успешно найден",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/OfferWall"}
                    }
                }
            },
            404: {
                "description": "Офферволл не найден"
            }
        }
    )
    async def get_offerwall_by_url(self, service: OfferWallService, url: str) -> OfferWallSchema:
        """Получить офферволл по URL.
        
        Args:
            service: Сервис для работы с офферволлами
            url: URL офферволла
            
        Returns:
            Детали офферволла
            
        Raises:
            NotFoundException: Если офферволл не найден
        """
        offerwall = await service.get_offerwall_by_url(url=url)
        return OfferWallSchema.model_validate(offerwall)

    @get(
        "/get_offer_names",
        summary="Получить список названий предложений",
        description="Возвращает список всех доступных названий предложений из OfferChoices",
        responses={
            200: {
                "description": "Список названий предложений успешно получен",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/OfferNames"}
                    }
                }
            }
        }
    )
    async def get_offer_names(self, service: OfferWallService) -> OfferNames:
        """Получить список названий предложений.
        
        Args:
            service: Сервис для работы с офферволлами
            
        Returns:
            Список названий предложений
        """
        names = service.get_offer_names()
        return OfferNames(offer_names=names)