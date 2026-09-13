from datetime import date, time
from typing import TYPE_CHECKING

from sqlalchemy import Date, Float, ForeignKey, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


if TYPE_CHECKING:
    from app.models.centre import Centre
    from app.models.crop import Crop
    from app.models.farmer import Farmer


class Booking(TimestampMixin, Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    farmer_id: Mapped[int] = mapped_column(
        ForeignKey("farmers.id"),
        nullable=False,
    )

    centre_id: Mapped[int] = mapped_column(
        ForeignKey("centres.id"),
        nullable=False,
    )

    crop_id: Mapped[int] = mapped_column(
        ForeignKey("crops.id"),
        nullable=False,
    )

    booking_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    slot_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    quantity: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="BOOKED",
    )

    farmer: Mapped["Farmer"] = relationship(
        "Farmer",
        back_populates="bookings",
    )

    centre: Mapped["Centre"] = relationship(
        "Centre",
    )

    crop: Mapped["Crop"] = relationship(
        "Crop",
    )