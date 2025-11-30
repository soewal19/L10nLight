from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Offer:
    uuid: str
    id: int
    url: str
    is_active: bool
    name: str
    sum_to: Optional[str] = None
    term_to: Optional[int] = None
    percent_rate: Optional[int] = None

@dataclass
class OfferWallOffer:
    offer: Offer

@dataclass
class OfferWallPopupOffer:
    offer: Offer

@dataclass
class OfferWall:
    token: str
    name: str
    url: str
    description: Optional[str] = None
    offer_assignments: List[OfferWallOffer] = None
    popup_assignments: List[OfferWallPopupOffer] = None

    def __post_init__(self):
        if self.offer_assignments is None:
            self.offer_assignments = []
        if self.popup_assignments is None:
            self.popup_assignments = []