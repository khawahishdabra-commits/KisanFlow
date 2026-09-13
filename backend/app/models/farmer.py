from typing import List

from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import TimestampMixin
from app.core.database import Base


class Farmer(TimestampMixin, Base):
    __tablename__ = "farmers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    phone: Mapped[str] = mapped_column(
        String(15),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    language: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="en",
    )

    latitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    longitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    bookings: Mapped[List["Booking"]] = relationship(
        back_populates="farmer",
    )