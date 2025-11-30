from sqlalchemy import ForeignKey, String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base

class OfferChoices:
    choices = [
        ("Loanplus", "Loanplus"),
        ("SgroshiCPA2", "SgroshiCPA2"),
        ("Novikredyty", "Novikredyty"),
        ("TurboGroshi", "TurboGroshi"),
        ("Crypsee", "Crypsee"),
        ("Suncredit", "Suncredit"),
        ("Lehko", "Lehko"),
        ("Monto", "Monto"),
        ("Limon", "Limon"),
        ("Amigo", "Amigo"),
        ("FirstCredit", "FirstCredit"),
        ("Finsfera", "Finsfera"),
        ("Pango", "Pango"),
        ("Treba", "Treba"),
        ("StarFin", "StarFin"),
        ("BitCapital", "BitCapital"),
        ("SgroshiCPL", "SgroshiCPL"),
        ("LoviLave", "LoviLave"),
        ("Prostocredit", "Prostocredit"),
        ("Sloncredit", "Sloncredit"),
        ("Clickcredit", "Clickcredit"),
        ("Credos", "Credos"),
        ("Dodam", "Dodam"),
        ("SelfieCredit", "SelfieCredit"),
        ("Egroshi", "Egroshi"),
        ("Alexcredit", "Alexcredit"),
        ("SgroshiCPA1", "SgroshiCPA1"),
        ("Tengo", "Tengo"),
        ("Credit7", "Credit7"),
        ("Tpozyka", "Tpozyka"),
        ("Creditkasa", "Creditkasa"),
        ("Moneyveo", "Moneyveo"),
        ("MyCredit", "MyCredit"),
        ("CreditPlus", "CreditPlus"),
        ("Miloan", "Miloan"),
        ("AvansCredit", "AvansCredit"),
    ]

class Offer(Base):
    __tablename__ = "offers"
    uuid: Mapped[str] = mapped_column(String(36), primary_key=True)
    id: Mapped[int] = mapped_column(Integer)
    url: Mapped[str] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    sum_to: Mapped[str | None] = mapped_column(String(255), nullable=True)
    term_to: Mapped[int | None] = mapped_column(Integer, nullable=True)
    percent_rate: Mapped[int | None] = mapped_column(Integer, nullable=True)

    offer_assignments: Mapped[list["OfferAssignment"]] = relationship(
        back_populates="offer", cascade="all, delete-orphan"
    )
    popup_assignments: Mapped[list["PopupAssignment"]] = relationship(
        back_populates="offer", cascade="all, delete-orphan"
    )

class OfferWall(Base):
    __tablename__ = "offerwalls"
    token: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    url: Mapped[str] = mapped_column(String(500))
    description: Mapped[str | None] = mapped_column(String(2000), nullable=True)

    offer_assignments: Mapped[list["OfferAssignment"]] = relationship(
        back_populates="offer_wall",
        cascade="all, delete-orphan",
        order_by=lambda: OfferAssignment.order,
    )
    popup_assignments: Mapped[list["PopupAssignment"]] = relationship(
        back_populates="offer_wall",
        cascade="all, delete-orphan",
        order_by=lambda: PopupAssignment.order,
    )

class OfferAssignment(Base):
    __tablename__ = "offer_wall_offers"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    offer_wall_token: Mapped[str] = mapped_column(ForeignKey("offerwalls.token", ondelete="CASCADE"))
    offer_uuid: Mapped[str] = mapped_column(ForeignKey("offers.uuid", ondelete="CASCADE"))
    order: Mapped[int] = mapped_column(Integer, default=0)

    offer_wall: Mapped[OfferWall] = relationship(back_populates="offer_assignments")
    offer: Mapped[Offer] = relationship(back_populates="offer_assignments")

class PopupAssignment(Base):
    __tablename__ = "offer_wall_popup_offers"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    offer_wall_token: Mapped[str] = mapped_column(ForeignKey("offerwalls.token", ondelete="CASCADE"))
    offer_uuid: Mapped[str] = mapped_column(ForeignKey("offers.uuid", ondelete="CASCADE"))
    order: Mapped[int] = mapped_column(Integer, default=0)

    offer_wall: Mapped[OfferWall] = relationship(back_populates="popup_assignments")
    offer: Mapped[Offer] = relationship(back_populates="popup_assignments")
