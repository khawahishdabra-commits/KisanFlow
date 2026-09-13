from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


if TYPE_CHECKING:
    from app.models.centre import Centre
    from app.models.crop import Crop


class Price(TimestampMixin, Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    centre_id: Mapped[int] = mapped_column(
        ForeignKey("centres.id"),
        nullable=False,
    )

    crop_id: Mapped[int] = mapped_column(
        ForeignKey("crops.id"),
        nullable=False,
    )

    buy_price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    sell_price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    effective_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    centre: Mapped["Centre"] = relationship(
        "Centre",
    )

    crop: Mapped["Crop"] = relationship(
        "Crop",
    )