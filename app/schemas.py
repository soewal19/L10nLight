from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List


class Offer(BaseModel):
    """Модель предложения"""
    model_config = ConfigDict(from_attributes=True)
    
    uuid: str = Field(..., description="Уникальный идентификатор предложения (UUID)")
    id: int = Field(..., description="ID предложения")
    url: str = Field(..., description="URL предложения")
    is_active: bool = Field(..., description="Активность предложения")
    name: str = Field(..., description="Название предложения")
    sum_to: Optional[str] = Field(None, description="Максимальная сумма")
    term_to: Optional[int] = Field(None, description="Максимальный срок в днях")
    percent_rate: Optional[int] = Field(None, description="Процентная ставка")


class OfferWallOffer(BaseModel):
    """Модель предложения в офферволле"""
    model_config = ConfigDict(from_attributes=True)
    offer: Offer = Field(..., description="Информация о предложении")


class OfferWallPopupOffer(BaseModel):
    """Модель popup предложения в офферволле"""
    model_config = ConfigDict(from_attributes=True)
    offer: Offer = Field(..., description="Информация о предложении")


class OfferWall(BaseModel):
    """Модель офферволла"""
    model_config = ConfigDict(from_attributes=True)
    
    token: str = Field(..., description="Уникальный токен офферволла")
    name: str = Field(..., description="Название офферволла")
    url: str = Field(..., description="URL офферволла")
    description: Optional[str] = Field(None, description="Описание офферволла")
    offer_assignments: List[OfferWallOffer] = Field(default_factory=list, description="Список предложений")
    popup_assignments: List[OfferWallPopupOffer] = Field(default_factory=list, description="Список popup предложений")


class OfferNames(BaseModel):
    """Модель списка названий предложений"""
    offer_names: List[str] = Field(..., description="Список названий предложений")
